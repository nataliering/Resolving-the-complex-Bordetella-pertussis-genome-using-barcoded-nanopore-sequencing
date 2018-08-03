# Resolving the complex *Bordetella pertussis* genome using barcoded nanopore sequencing

This repository is currently an almost-complete work-in-progress to support our paper. Content will include:
- [ ] our full methodology, including any homemade code and commands used for community-built tools, plus a shell script to run either of our final pipelines (hybrid or long-read-only)
- [ ] links to our data repository, including raw and processed reads (fastq), and genome assembler test intermediates and final assemblies
- [ ] extended results (where applicable) and links to full metadata/supplementary files




## Abstract
The genome of *Bordetella pertussis* is complex, with high GC content and many repeats, each longer than 1,000 bp. Short-read DNA sequencing is unable to resolve the structure of the genome; however, long-read sequencing offers the opportunity to produce single-contig *B. pertussis* assemblies using sequencing reads which are longer than the repetitive sections. We used an R9.4 MinION flow cell and barcoding to sequence five *B. pertussis* strains in a single sequencing run. We then trialled combinations of the many nanopore-user-community-built long-read analysis tools to establish the current optimal assembly pipeline for *B. pertussis* genome sequences. Our best long-read-only assemblies were produced by Canu read correction followed by assembly with Flye and polishing with Nanopolish, whilst the best hybrids (using nanopore and Illumina reads together) were produced by Canu correction followed by Unicycler. This pipeline produced closed genome sequences for four strains, revealing inter-strain genomic rearrangement. However, read mapping to the Tohama I reference genome suggests that the remaining strain contains an ultra-long duplicated region (over 100 kbp), which was not resolved by our pipeline. We have therefore demonstrated the ability to resolve the structure of several *B. pertussis* strains per single barcoded nanopore flow cell, but the genomes with highest complexity (e.g. very large duplicated regions) remain only partially resolved using the standard library preparation and will require an alternative library preparation method. For full strain characterisation, we recommend hybrid assembly of long and short reads together; for comparison of genome arrangement, assembly using long reads alone is sufficient.

## Commands for tools mentioned in manuscript
Each of the tools we used can be further optimised; we tended to use the default settings in most cases, often exactly as recommended in the tool's README.
### Preparing Illumina reads and assembling Illumina-only references
**[fastq-dump (download of reads from SRA)](https://ncbi.github.io/sra-tools/fastq-dump.html)**  
`fastq-dump ACCESSION_NUMBER --gzip`

**[Trimmomatic](http://www.usadellab.org/cms/?page=trimmomatic)**  
`java -jar trimmomatic.jar PE input_1.fastq input_2.fastq output_1_PE.fastq output_1_SE.fastq output_2_PE.fastq output_2_SE.fastq HEADCROP:10 SLIDING WINDOW:4:32`

**[ABySS](https://github.com/bcgsc/abyss)**  
`abyss-pe name=output_name k=63 in='input_1_PE.fastq input_2_PE.fastq' t=8` 

### Preparing Nanopore reads
**[Albacore](https://community.nanoporetech.com/protocols/albacore-offline-basecalli/v/abec_2003_v1_revan_29nov2016/linux)** (Nanopore community account needed)  
`read_fast5_basecaller.py --flowcell FLO-MIN106 --kit SQK-LSK108 --barcoding --output_format fast5,fastq --input directory_of_fast5_files --save_path directory_for_output --worker_threads 8`

**[Porechop](https://github.com/rrwick/Porechop)**  
`porechop -i input_directory -b output-directory --threads 8`

**[Filtlong (100x coverage)](https://github.com/rrwick/Filtlong)**  
`filtlong --target_bases 400000000 input_reads.fastq > filtered_100.fastq`

**[Filtlong (40x coverage)](https://github.com/rrwick/Filtlong)**  
`filtlong --target_bases 160000000 input_reads.fastq > filtered_40.fastq`

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
`minimap -x ava-ont -t8 corrected_reads.fasta corrected_reads.fasta | gzip -1 > reads.paf.gz`

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
**Assembly_identity:** [chop_up_assembly.py](https://github.com/rrwick/Basecalling-comparison/blob/master/chop_up_assembly.py), [minimap2](https://github.com/lh3/minimap2), [python3](https://www.python.org/download/releases/3.0/)  

**gidA_blast:** [blast](https://blast.ncbi.nlm.nih.gov/Blast.cgi?CMD=Web&PAGE_TYPE=BlastDocs&DOC_TYPE=Download)  

**nanopolish_runner:** [nanopolish](https://github.com/jts/nanopolish)(including nanopolish index, nanopolish_makerange.py, nanopolish variants and nanopolish_merge.py), [GNU parallel](https://www.gnu.org/software/parallel/), [bwa](https://github.com/lh3/bwa), [samtools](https://github.com/samtools/)  

**pilon_runner:** [bwa](https://github.com/lh3/bwa), [samtools](https://github.com/samtools/), [Pilon](https://github.com/broadinstitute/pilon)  





## Supplemtary results
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


## Results

Full results from all assembler combinations for both MinKNOW and Albacore basecalled reads can be viewed/downloaded [here](https://figshare.com/s/8cab70ab692ef95ce794).

## Data repository links:
### Raw read sets
[Raw MinKNOW + Porechop reads](https://figshare.com/s/5e9cfe31ee97a3591f8c)                     
[Raw Albacore only reads](https://figshare.com/s/c72019ace881bfa69593)                             
[Raw Albacore + Porechop reads](https://figshare.com/s/4a2a376c8d4d130b3ecb)                      

### Processed read sets
[MinKNOW Canu-corrected reads]()                     
[Albacore + Porechop Canu-corrected reads]()                    
[MinKNOW Filtlong 40X reads]()                      
[MinKNOW Filtlong 100X reads]()                              

### Draft assemblies
[UK36 MinKNOW assemblies]()               
[UK36 Albacore assemblies]()

### Final assemblies
[Long-read-only assemblies]()               
[Hybrid assemblies]()

## References
1. [Sealey KL, Harris SR, Fry NK, Hurst LD, Gorringe AR et al. Genomic analysis of isolates from the United Kingdom 2012 pertussis outbreak reveals that vaccine antigen genes are unusually fast evolving. The Journal of infectious diseases 2015;212(2):294-301](https://academic.oup.com/jid/article/212/2/294/890134])
2. [Wick RR, Judd LM, Holt KE. Comparison of Oxford Nanopore basecalling tools. 2017.](https://github.com/rrwick/Basecalling-comparison)
