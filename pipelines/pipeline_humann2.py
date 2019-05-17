"""
Pipeline to run Humann2 on a folder of fastq files
"""

#load modules
from ruffus import *
import re, sys

from pipeline_humann2 import PipelineHumann2

###################################################
###################################################
###################################################
# Pipeline configuration
###################################################
# load options from the config file
import cgatcore.pipeline as P
P.get_parameters(
       ["%s/pipeline.yml" % __file__[:-len(".py")],
       "../pipeline.yml",
       "pipeline.yml" ] )
PARAMS = P.PARAMS


#get all files within the directory to process
SEQUENCEFILES = ("*.fasta", "*.fasta.gz", "*.fasta.1.gz", "*.fasta.1",
                 "*.fna", "*.fna.gz", "*.fna.1.gz", "*.fna.1",
                 "*.fa", "*.fa.gz", "*.fa.1.gz", "*.fa.1", 
                 "*.fastq", "*.fastq.gz", "*.fastq.1.gz","*.fastq.1")

SEQUENCEFILES_REGEX = regex(PipelineHumann2.seqpat)

#merge paired ends if PE files
@follows(mkdir("cat_files.dir"))
@transform(SEQUENCEFILES,SEQUENCEFILES_REGEX,r"cat_files.dir/\1.{}".format(PipelineHumann2.fileForm()))
def catPairs(infile,outfile):
    seqdat=PipelineAssembly.SequencingData(infile)
    if seqdat.paired == False:
        statement = "ln -s {} {}".format(infile,outfile)
    else:
        statement = "cat {} {} > {}".format(infile,seqdat.pairedname,outfile)
    P.run(statement)

#run Humann2
@follows(catPairs)
@follows(mkdir("humann2_out.dir"))
@transform(catPairs,regex(r"cat_files.dir/"+PipelineHumann2.seqpat),r"humann2_out.dir/\1_pathabundance.tsv")
def runHumann2(infile, outfile):
    job_threads = int(PARAMS["Humann2_threads"])
    job_memory = PARAMS["Humann2_memory"]+"G"
    statement = PipelineHumann2.humann2Call(infile,PARAMS)
    P.run(statement)

#merge the tables
merged_tables=["merged_unnorm.dir/{}".format(x) for x in ["merged_genefamilies.tsv","merged_pathabundance.tsv","merged_pathcoverage.tsv"]]
@follows(runHumann2)
@follows(mkdir("merged_unnorm.dir"))
@originate(merged_tables)
def mergeTables(outfile):
    statement=PipelineHumann2.humann2Merge(outfile,PARAMS)
    P.run(statement)

#generate normalised tables
@follows(mergeTables)
@follows(mkdir("merged_norm.dir"))
@transform(mergeTables,regex(r"merged_unnorm.dir/(\S+).tsv"),r"merged_norm.dir/\1_norm.tsv")
def normTables(infile,outfile):
    if re.search("coverage",infile):
        statement="ln -s ../{} {}".format(infile,outfile)
    else:
        statement=PipelineHumann2.humann2Norm(infile,outfile,PARAMS)
    P.run(statement)

@follows(normTables)
def full():
    pass

    
if __name__ == "__main__":
    if sys.argv[1] == "plot":
        pipeline_printout_graph("test.pdf", "pdf", [full], no_key_legend=True,
                                size=(4, 4),
                                user_colour_scheme = {"colour_scheme_index": 1})
    else:
        sys.exit(P.main(sys.argv))
