"""
Functions for pipeline_metaphlan2.py
"""

import sys,re

#dir of the MetaSequencing pipeline PipelineAssembly script
sys.path.append("/gfs/devel/majackson/Pipelines/MetaSequencing/pipelines")

from pipeline_assembly import PipelineAssembly

#add virtual env call if necessary
def checkVenv(params):
    if params["Metaphlan2_venv"] != "false":
        return("source activate {} && ".format(params["Metaphlan2_venv"]))
    else:
        return("")


#build the call to Metaphlan2
def callMetaphlan2(infile,outfile,params):
    #check format and pairedness of input
    indat=PipelineAssembly.SequencingData(infile)
    inputf=infile
    inputt=indat.fileformat
    if indat.paired == True:
        inputf+=",{}".format(indat.pairedname)
        inputt="multi"+inputt
    mcall=[checkVenv(params)]
    mcall.append("metaphlan2.py {} --input_type {} -t {} --tax_lev {} -o {}".format(inputf,inputt,params["Metaphlan2_t"],params["Metaphlan2_tax_lev"],outfile))
    if params["Metaphlan2_bowtie2db"] != "false":
        mcall.append("--bowtie2db {}".format(params["Metaphlan2_bowtie2db"]))
    if params["Metaphlan2_index"] != "false":
        mcall.append("--index {}".format(params["Metaphlan2_index"]))
    if params["Metaphlan2_bt2_ps"] != "false":
        mcall.append("--bt2_ps {}".format(params["Metaphlan2_bt2_ps"]))
    if params["Metaphlan2_bowtie2_exe"] != "false":
        mcall.append("--bowtie2_exe {}".format(params["Metaphlan2_bowtie2_exe"]))
    if params["Metaphlan2_bowtie2_build"] != "false":
        mcall.append("--bowtie2_build {}".format(params["Metaphlan2_bowtie2_build"]))
    if params["Metaphlan2_save_bowtie"] == "false":
        mcall.append("--no_map")
    else:
        mcall.append("--bowtie2out {}".format(outfile+".bowtie.out"))
    if params["Metaphlan2_min_cu_len"] != "false":
        mcall.append("--min_cu_len {}".format(params["Metaphlan2_min_cu_len"]))
    if params["Metaphlan2_min_alignment_len"] != "false":
        mcall.append("--min_alignment_len {}".format(params["Metaphlan2_min_alignment_len"]))
    if params["Metaphlan2_ignore_viruses"] != "false":
        mcall.append("--ignore_viruses")
    if params["Metaphlan2_ignore_eukaryotes"] != "false":
        mcall.append("--ignore_eukaryotes")
    if params["Metaphlan2_ignore_bacteria"] != "false":
        mcall.append("--ignore_bacteria")
    if params["Metaphlan2_ignore_archaea"] != "false":
        mcall.append("--ignore_archaea")
    if params["Metaphlan2_ignore_viruses"] != "false":
        mcall.append("--ignore_viruses")
    if params["Metaphlan2_stat_q"] != "false":
        mcall.append("--stat_q {}".format(params["Metaphlan2_stat_q"]))
    if params["Metaphlan2_ignore_markers"] != "false":
        mcall.append("--ignore_markers {}".format(params["Metaphlan2_ignore_markers"]))
    if params["Metaphlan2_avoid_disqm"] != "false":
        mcall.append("--avoid_disqm")
    if params["Metaphlan2_stat"] != "false":
        mcall.append("--stat {}".format(params["Metaphlan2_stat"]))
    mcall.append(params["Metaphlan2_other"])
    if params["Metaphlan2_tmp_dir"] != "false":
        mcall.append("--tmp_dir {}".format(params["Metaphlan2_tmp_dir"]))
    mcall.append("--sample_id {}".format(indat.cleanname))
    if params["Metaphlan2_threads"] != "false":
        mcall.append("--nproc {}".format(params["Metaphlan2_threads"]))
    mstat=" ".join(mcall)
    return(mstat)


#filter the mrged table using grep to find lines with the required taxonomy but no finer
def filterTaxa(infile,outfile):
    if re.search("species",outfile):
        target="s"
        avoid="t"
    elif re.search("genera",outfile):
        target="g"
        avoid="s"
    elif re.search("families",outfile):
        target="f"
        avoid="g"
    elif re.search("orders",outfile):
        target="o"
        avoid="f"
    elif re.search("classes",outfile):
        target="c"
        avoid="o"
    elif re.search("phyla",outfile):
        target="p"
        avoid="c"
    elif re.search("kingdom",outfile):
        target="k"
        avoid="p"
    call="grep -E \"({}__)|(^ID)\" {} | grep -v \"{}__\" > {}".format(target,infile,avoid,outfile)
    return(call)
