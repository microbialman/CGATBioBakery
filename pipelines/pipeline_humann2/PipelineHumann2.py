"""
Functions for pipeline_humann2.py
"""

import sys,glob,re

#dir of the MetaSequencing pipeline PipelineAssembly script
sys.path.append("/gfs/devel/majackson/Pipelines/MetaSequencing/pipelines")

from pipeline_assembly import PipelineAssembly

#pattern to find files in directory
seqpat=r"(\S+).(fasta$|fasta.gz|fasta.1.gz|fasta.1|fna$|fna.gz|fna.1.gz|fna.1|fa$|fa.gz|fa.1.gz|fa.1|fastq$|fastq.gz|fastq.1.gz|fastq.1)"

def checkVenv(params):
    if params["Humann2_venv"] != "false":
        return("source activate {} && ".format(params["Humann2_venv"]))
    else:
        return("")
               
#get file format from first file
def fileForm():
    matching=[x for x in glob.glob("./*") if re.search(seqpat,x)]
    seqdat=PipelineAssembly.SequencingData(matching[0])
    ext=seqdat.fileformat
    if seqdat.compressed == True:
        ext+=".gz"
    return(ext)

#make call to humann2
def humann2Call(infile,params):
    hcall=checkVenv(params)
    hcall+="humann2 --input {} --output humann2_out.dir --threads {} {}".format(infile,params["Humann2_threads"],params["Humann2_commands"])
    return(hcall)

    
#call to merge humann2 tables
def humann2Merge(outfile,params):
    mcall=checkVenv(params)
    filename=re.search("merged_unnorm.dir/merged_(\S+).tsv",outfile).group(1)
    mcall+="humann2_join_tables -i humann2_out.dir -o {} --file_name {}".format(outfile,filename)
    return(mcall)

#call to normalise humann2 tables
def humann2Norm(infile,outfile,params):
    ncall=checkVenv(params)
    ncall+="humann2_renorm_table -i {} -o {} --units {}".format(infile,outfile,params["Normalisation_units"])
    return(ncall)
