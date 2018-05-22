# Resolving the complex *Bordetella pertussis* genome using barcoded nanopore sequencing

**Natalie Ring, Jonathan Abrahams, Andrew Preston \& Stefan Bagby**      
*Department of Biology and Biochemistry, University of Bath*

This repository is currently a work-in-progress (mostly due to data upload speed!), but will support both our paper (once submitted) and poster presentation at London Calling 2018. Content will include:
- [ ] our full methodology, including any homemade code and commands used for community-built tools, plus a shell script to run either of our final pipelines
- [ ] links to our data repository, including raw and processed reads (fastq), and genome assembler test intermediates and final assemblies
- [ ] extended results and links to full metadata/supplementary files
- [ ] references and other recommended reading

## Abstract
*Bordetella pertussis*, the pathogen responsible for whooping cough, has a complex genome with high GC content and hundreds of repetitive sections, each longer than 1kb. While short-read sequencing has been unable to resolve the structure of the genome, long-read sequencing could enable accurate single-contig *B. pertussis* assembly.  

We have used barcoded MinION sequencing to resolve genome structures of five UK *B. pertussis* strains with a single flow cell. Extensive testing of available data analysis tools revealed that our optimal long-read-only assembly pipeline includes Canu read correction, Flye assembly and Nanopolish polishing, and can produce single-contig assemblies approaching 99.6% identity.
Although *B. pertussis* is a monomorphic organism at base level, our single-contig assemblies reveal genome-level arrangement differences. Our long-read-based pipeline to assemble *B. pertussis* genomes consistently into single contigs could therefore help to explain phenotypes which otherwise have no obvious genotypic cause.

## Method
We ran five different flow cell trials between 2015 and 2017, using both R7 and R9/R9.4 flow cells:
- July 2015, R7, 2D Genomic DNA (deprecated): *B. pertussis* UK48 and UK76
- April 2017, R9, 1D Genomic DNA by ligation (SQK-LSK108): *B. pertussis* UK76
- June 2017, R9.4, 1D Low input genomic DNA with PCR (SQK-LSK108): *B. pertussis* 18323
- June 2017, R9.4, 1D Low input genomic DNA by PCR barcoding (SQK-LWB001): *B. pertussis* UK36, UK38, UK39, UK48 and UK76 
- June 2017, R9.4, 1D Native barcoding genomic DNA (with EXP-NBD103 and SQK-LSK108):  *B. pertussis* UK36, UK38, UK39, UK48 and UK76

|Date|Flow cell chemistry|Library Prep|*B. pertussis* strain(s)|
|----|-------------------|------------|------------------------|
|July 2015|R7|2D Genomic DNA (deprecated)| UK48, UK76|
|March 2017|R9|1D Genomic DNA by ligation (SQK-LSK108)| UK76|
|June 2017|R9.4|1D Low input genomic DNA with PCR (SQK-LSK108)| 18323|
|June 2017|R9.4|1D Low input genomic DNA by PCR barcoding (SQK-LWB001)| UK36, UK38, UK39, UK48, UK76|
|June 2017|R9.4|1D Native barcoding genomic DNA (EXP-NBD103 and SQK-LSK108)| UK36, UK38, UK39, UK48, UK76|






[Raw Albacore + Porechop reads](https://figshare.com/s/4a2a376c8d4d130b3ecb)
