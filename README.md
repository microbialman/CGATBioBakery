# CGATBioBakery
A series of pipelines for running tools (currently MetaPhlAn2 and HUMAnN2) from the **[bioBakery](https://bitbucket.org/biobakery/biobakery/wiki/Home)** collection developed by the Huttenhower lab within the  **[CGAT](https://github.com/cgat-developers/cgat-core)** framework.

## Installation

Requires installation of **[MetaSequencing](https://github.com/microbialman/MetaSequencing)** and **[CGATCore](https://github.com/cgat-developers/cgat-core)**. The latter is a framework for running bioinformatics pipelines built around the **[Ruffus](http://www.ruffus.org.uk/)** library that automatically handles job submission on HPC clusters. CGAT installation instructions can be found [here](https://github.com/cgat-developers/cgat-core).

It also requires installtion of the various BioBakery tools, which should be available in the PATH. Additionally these tools can be installed to a virtual envrionment that will be initiated before references to their commands.

## Running the pipelines

Pipelines are run from the working directory containing the files to be analysed.
First a config file *pipeline.yml* must be generate in the directory using the *config* command.
The pipeline can then be run using *make full*

## Example commands

An example run for Humann2 is shown below:

```sh

#make an analysis folder and symlink the starting reads
mkdir Humann2_Run
cd Humann2_Run
ln -s path_to_reads/*.gz ./
#generate the pipeline configuration file (this will need to be edited to set parameters) 
python CGATBioBakery/pipelines/pipeline_humann2.py config
#run the full humann2 run (this will also merge and normalise the output tables)
python CGATBioBakery/pipelines/pipeline_humann2.py make full

```



