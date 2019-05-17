"""
Pipeline to run Metaphlan2 on a folder of input files
"""

#load modules
from ruffus import *
import sys

from pipeline_metaphlan2 import PipelineMetaphlan2


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

SEQUENCEFILES_REGEX = regex(
    r"(\S+).(fasta$|fasta.gz|fasta.1.gz|fasta.1|fna$|fna.gz|fna.1.gz|fna.1|fa$|fa.gz|fa.1.gz|fa.1|fastq$|fastq.gz|fastq.1.gz|fastq.1)")

###################################
# Run Metaphlan2
##################################
@follows(mkdir("metaphlan2_out.dir"))
@transform(SEQUENCEFILES,SEQUENCEFILES_REGEX,r"metaphlan2_out.dir/\1.tsv")
def runMetaphlan2(infile,outfile):
    job_memory = PARAMS["Metaphlan2_memory"]+"G"
    job_threads = int(PARAMS["Metaphlan2_threads"])
    statement=PipelineMetaphlan2.callMetaphlan2(infile,outfile,PARAMS)
    P.run(statement)

####################################
# Merge outputs
####################################
@follows(mkdir("merged_out.dir"))
@merge(runMetaphlan2,"merged_out.dir/all_taxa.tsv")
def mergeOut(infiles,outfile):
    statement = "{} metaphlan2_out.dir/*.tsv > {}".format(PARAMS["Merge_script"],outfile)
    P.run(statement)

##################################
# Generate taxa filtered tables
###################################
@follows(mergeOut)
@originate(["merged_out.dir/{}.tsv".format(x) for x in PARAMS["Filter_taxa"].split(",")])
def splitTaxa(outfile):
    statement = PipelineMetaphlan2.filterTaxa("merged_out.dir/all_taxa.tsv",outfile)
    P.run(statement)


@follows(splitTaxa)
def full():
    pass


if __name__ == "__main__":
    if sys.argv[1] == "plot":
        pipeline_printout_graph("test.pdf", "pdf", [full], no_key_legend=True,
                                size=(4, 4),
                                user_colour_scheme = {"colour_scheme_index": 1})
    else:
        sys.exit(P.main(sys.argv))
