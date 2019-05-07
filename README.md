# Resolving the complex *Bordetella pertussis* genome using barcoded nanopore sequencing

This repository supports our paper, which is now published in Microbial Genomics: https://mgen.microbiologyresearch.org/content/journal/mgen/10.1099/mgen.0.000234 

**Posters related to this work:**

[London Calling (annual Nanopore meeting), London, May 2018](https://github.com/nataliering/Resolving-the-complex-Bordetella-pertussis-genome-using-barcoded-nanopore-sequencing/blob/master/Poster_London_Calling_May2018.pdf)

[International Bordetella Symposium, Brussels, April 2019](https://github.com/nataliering/Resolving-the-complex-Bordetella-pertussis-genome-using-barcoded-nanopore-sequencing/blob/master/Poster_International_Bordetella_Symposium_April2019.pdf)


Content includes:
- homemade code and commands used for community-built tools
- links to our data repository, including raw and processed reads (fastq), and genome assembler test intermediates and final assemblies
- supplementary results and links to full metadata/supplementary files

A shell script to run either of our final pipelines (hybrid or long-read-only) could be made available; let us know if this is something you would use!




## Abstract
The genome of *Bordetella pertussis* is complex, with high GC content and many repeats, each longer than 1,000 bp. Short-read DNA sequencing is unable to resolve the structure of the genome; however, long-read sequencing offers the opportunity to produce single-contig *B. pertussis* assemblies using sequencing reads which are longer than the repetitive sections. We used an R9.4 MinION flow cell and barcoding to sequence five *B. pertussis* strains in a single sequencing run. We then trialled combinations of the many nanopore-user-community-built long-read analysis tools to establish the current optimal assembly pipeline for *B. pertussis* genome sequences. Our best long-read-only assemblies were produced by Canu read correction followed by assembly with Flye and polishing with Nanopolish, whilst the best hybrids (using nanopore and Illumina reads together) were produced by Canu correction followed by Unicycler. This pipeline produced closed genome sequences for four strains, revealing inter-strain genomic rearrangement. However, read mapping to the Tohama I reference genome suggests that the remaining strain contains an ultra-long duplicated region (over 100 kbp), which was not resolved by our pipeline. We have therefore demonstrated the ability to resolve the structure of several *B. pertussis* strains per single barcoded nanopore flow cell, but the genomes with highest complexity (e.g. very large duplicated regions) remain only partially resolved using the standard library preparation and will require an alternative library preparation method. For full strain characterisation, we recommend hybrid assembly of long and short reads together; for comparison of genome arrangement, assembly using long reads alone is sufficient.

## Commands for tools mentioned in manuscript
Each of the tools we used can be further optimised; we tended to use the default settings in most cases, often exactly as recommended in the tool's README.
### Preparing Illumina reads and assembling Illumina-only references
**[fastq-dump (download of reads from SRA)](https://ncbi.github.io/sra-tools/fastq-dump.html)**  
`fastq-dump ACCESSION_NUMBER --split-files --gzip`

**[Trimmomatic](http://www.usadellab.org/cms/?page=trimmomatic)**  
`java -jar trimmomatic.jar PE input_1.fastq input_2.fastq output_1_PE.fastq output_1_SE.fastq output_2_PE.fastq output_2_SE.fastq HEADCROP:10 SLIDINGWINDOW:4:32`

**[ABySS](https://github.com/bcgsc/abyss)**  
`abyss-pe name=output_name k=63 in='input_1_PE.fastq input_2_PE.fastq' t=8` 

### Preparing Nanopore reads
**[Albacore](https://community.nanoporetech.com/protocols/albacore-offline-basecalli/v/abec_2003_v1_revan_29nov2016/linux)** (Nanopore community account needed)  
`read_fast5_basecaller.py --flowcell FLO-MIN106 --kit SQK-LSK108 --barcoding --output_format fast5,fastq --input directory_of_fast5_files --save_path directory_for_output --worker_threads 8`

**[Porechop](https://github.com/rrwick/Porechop)**  
`porechop -i input_directory -b output-directory --threads 8`

**[Filtlong (100x coverage)](https://github.com/rrwick/Filtlong)**  
`filtlong --target_bases 400000000 input_reads.fastq > filtered_100.fasta`

**[Filtlong (40x coverage)](https://github.com/rrwick/Filtlong)**  
`filtlong --target_bases 160000000 input_reads.fastq > filtered_40.fasta`

**[Canu correct (40x coverage)](https://github.com/marbl/canu)**  
`canu -correct -p output_prefix -d output_directory genomeSize=4.1m -nanopore-raw input_reads.fastq`

### Nanopore-only assembly
**[ABruijn/Flye](https://github.com/fenderglass/Flye)**  
`flye --nano-corr corrected_reads.fasta --genome-size 4.1m --out-dir output_directory --threads 8` 

OR

`abruijn -t 8 -p nano corrected_reads.fasta out_directory 40`

**[Canu](https://github.com/marbl/canu)**  
`canu -p output_prefix -d output_directory genomeSize=4.1m -nanopore-raw input_reads.fastq`

**[Miniasm (with Minimap)](https://github.com/lh3/miniasm)**  
`minimap2 -x ava-ont -t8 corrected_reads.fasta corrected_reads.fasta | gzip -1 > reads.paf.gz`

`miniasm -f corrected_reads.fasta reads.paf.gz > output.gfa`

The output gfa graph file was converted to fasta using [gfa2fasta](https://github.com/nataliering/Resolving-the-complex-Bordetella-pertussis-genome-using-barcoded-nanopore-sequencing/blob/master/gfa2fasta)  
`gfa2fasta output.gfa output.fasta`

**[Unicycler (long reads only)](https://github.com/rrwick/Unicycler)**  
`unicycler -l corrected_reads.fasta -o output_directory -t 8`

### Hybrid assembly
**[SPAdes](http://cab.spbu.ru/software/spades/)**  
`spades.py -1 output_1_pe.fastq -2 output_2_pe.fastq --nanopore corrected_reads.fasta --threads 8 -o output_directory`

**[Unicycler (hybrid mode)](https://github.com/rrwick/Unicycler)**  
`unicycler unicycler -1 output_1_pe.fastq -2 output_2_pe.fastq -l corrected_reads.fasta -o output_directory -t 8`


### Polishing (long and short reads)
**[Racon](https://github.com/isovic/racon)**  
We used Minimap to map the Nanopore (or Illumina) reads to each draft, then used the alignment file to run Racon. [racon_runner](https://github.com/nataliering/Resolving-the-complex-Bordetella-pertussis-genome-using-barcoded-nanopore-sequencing/blob/master/racon_runner) automatically carries out the required steps.

**[Nanopolish](https://github.com/jts/nanopolish)**  
We included Nanopolish in our Nanopore-only pipeline. Nanopolish requires access to the raw fast5 files, and ideally the "sequencing_summary.txt" file produced during Albacore basecalling (this makes the previously very slow nanopolish index step much faster!). The raw fast5 files were too large to share on figshare, but assuming you have access to the required files, [nanopolish_runner](https://github.com/nataliering/Resolving-the-complex-Bordetella-pertussis-genome-using-barcoded-nanopore-sequencing/blob/master/nanopolish_runner) will carry out all the required steps (N.B. major changes to the way Nanopolish runs mean that nanopolish_runner won't work for version 0.10.1 onwards of Nanopolish. However, Nanopolish has thorough documentation which explains how to use the newer versions).

**[Pilon](https://github.com/broadinstitute/pilon)**  
We used bwa mem to produce map the Illumina reads to each draft, processed the output alignment using samtools, then used the processed alignment file to run Pilon. [pilon_runner](https://github.com/nataliering/Resolving-the-complex-Bordetella-pertussis-genome-using-barcoded-nanopore-sequencing/blob/master/pilon_runner) automatically carries out the required steps.

### Assessing assembly quality
**[Quast](http://quast.sourceforge.net/quast)**  
`quast.py assembly1.fasta assembly2.fasta (etc) --output-dir output_directory --threads 8 -R reference_genome.fasta -G reference_genes.gff`

**[BUSCO](https://busco.ezlab.org/)**  
`BUSCO.py -i assembly.fasta -o output_name -l path/to/bacteria_db -m geno`

### Draft annotation
**[Prokka](https://github.com/tseemann/prokka)**  
`prokka --prefix prefix --addgenes --centre centre_name --compliant --genus Bordetella --species pertussis --kingdom Bacteria --usegenus --proteins reference_proteins.faa --evalue 1e-10 --rfam --cpus 8  assembly.fasta --force`

## Dependencies for our scripts
Our scripts/tool runners require the following tools to be available in your PATH:  

**assembly_identity:** [chop_up_assembly.py](https://github.com/rrwick/Basecalling-comparison/blob/master/chop_up_assembly.py), [minimap2](https://github.com/lh3/minimap2), [python3](https://www.python.org/download/releases/3.0/), [read_length_identity.py](https://github.com/rrwick/Basecalling-comparison/blob/master/read_length_identity.py)  

**gidA_blast:** [blast](https://blast.ncbi.nlm.nih.gov/Blast.cgi?CMD=Web&PAGE_TYPE=BlastDocs&DOC_TYPE=Download)  

**nanopolish_runner:** [nanopolish](https://github.com/jts/nanopolish)(including nanopolish index, nanopolish_makerange.py, nanopolish variants and nanopolish_merge.py), [GNU parallel](https://www.gnu.org/software/parallel/), [bwa](https://github.com/lh3/bwa), [samtools](https://github.com/samtools/)  

**pilon_runner:** [bwa](https://github.com/lh3/bwa), [samtools](https://github.com/samtools/), [Pilon](https://github.com/broadinstitute/pilon)  

**racon_runner:** [minimap2](https://github.com/lh3/minimap2), [Racon](https://github.com/isovic/racon)

**raw_error:** [bwa](https://github.com/lh3/bwa), [samtools](https://github.com/samtools/)

**reverse_complement:**  [python](https://www.python.org/)

**summary_stats:** [seq_length.py](https://github.com/nataliering/Resolving-the-complex-Bordetella-pertussis-genome-using-barcoded-nanopore-sequencing/blob/master/seq_length.py), [python](https://www.python.org/), [all_stats](https://github.com/nataliering/Resolving-the-complex-Bordetella-pertussis-genome-using-barcoded-nanopore-sequencing/blob/master/all_stats)

**tblastn_runner:** [blast](https://blast.ncbi.nlm.nih.gov/Blast.cgi?CMD=Web&PAGE_TYPE=BlastDocs&DOC_TYPE=Download)  


## Supplementary results
### Flow cell trials        
We ran five different MinION flow cell trials between 2015 and 2017, using both R7 and R9/R9.4 flow cells (see table 1). Having established that the yield of a single R9.4 flow cell would enable the sequencing of multiple strains per flow cell with the use of barcodes, we took forward highest quality barcoded read set (in terms of yield, % identity, etc.) to the assembly tests described in our manuscript.

**Table 1: Flow cell trials**

|Date|Flow cell chemistry|Library Prep|*B. pertussis* strain(s)|Basecaller|
|----|-------------------|------------|------------------------|----------|
|July 2015|R7|2D Genomic DNA (deprecated)| UK48, UK76|Metrichor|
|March 2017|R9|1D Genomic DNA by ligation (SQK-LSK108)| UK76|Albacore (early version)|
|June 2017|R9.4|1D Low input genomic DNA with PCR (SQK-LSK108)| 18323|MinKNOW v.Jun17|
|June 2017|R9.4|1D Low input genomic DNA by PCR barcoding (SQK-LWB001)| UK36, UK38, UK39, UK48, UK76|MinKNOW v.Jun17|
|June 2017|R9.4|1D Native barcoding genomic DNA (EXP-NBD103 and SQK-LSK108) (half of each sample underwent end-repair)| UK36, UK38, UK39, UK48, UK76|MinKNOW v.Jun17|

The graph below shows the progress in yield per flow cell between 2015 and 2017, with a large increase in yield corresponding to the switch from R7 to R9 flow cell chemistry in early 2017. The yields we produced using the library prep kits which involved PCR (low input) were more variable than those which did not.

![alt text](https://github.com/nataliering/Resolving-the-complex-Bordetella-pertussis-genome-using-barcoded-nanopore-sequencing/blob/master/Github_fig1.png)



## Data repository links:
### Raw read sets
[Raw MinKNOW + Porechop reads](https://doi.org/10.6084/m9.figshare.6323099.v2)                     
[Raw Albacore only reads](https://doi.org/10.6084/m9.figshare.6302042.v1)                             
[Raw Albacore + Porechop reads](https://doi.org/10.6084/m9.figshare.6294791.v2)                      

### Processed read sets
[Trimmed Illumina reads](https://doi.org/10.6084/m9.figshare.6833492.v1)                   
[Canu-corrected reads](https://doi.org/10.6084/m9.figshare.6932795)                    
[Filtlong 40X reads](https://doi.org/10.6084/m9.figshare.6932882)                      
[Filtlong 100X reads](https://doi.org/10.6084/m9.figshare.6934307) 

### [Reference sequences (i.e. Illumina-only contigs, IS element sequences, etc.)](https://doi.org/10.6084/m9.figshare.6462446.v2 )


### Draft assemblies
[UK36 Nanopore-only assemblies](https://doi.org/10.6084/m9.figshare.6462767.v1)               
[UK36 Hybrid assemblies](https://doi.org/10.6084/m9.figshare.6462773.v3)

### Final assemblies
[Long-read-only assemblies](https://doi.org/10.6084/m9.figshare.6670721.v1)               
[Hybrid assemblies](https://doi.org/10.6084/m9.figshare.6670454.v3)

