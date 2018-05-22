# Resolving the complex *Bordetella pertussis* genome using barcoded nanopore sequencing
**Natalie Ring, Jonathan Abrahams, Andrew Preston \& Stefan Bagby**

Department of Biology and Biochemistry, University of Bath

### Abstract
*Bordetella pertussis*, the pathogen responsible for whooping cough, has a complex genome with high GC content and hundreds of repetitive sections, each longer than 1kb. While short-read sequencing has been unable to resolve the structure of the genome, long-read sequencing could enable accurate single-contig *B. pertussis* assembly.  


We have used barcoded MinION sequencing to resolve genome structures of five UK *B. pertussis* strains with a single flow cell. Extensive testing of available data analysis tools revealed that our optimal long-read-only assembly pipeline includes Canu read correction, Flye assembly and Nanopolish polishing, and can produce single-contig assemblies approaching 99.6% identity.
Although *B. pertussis* is a monomorphic organism at base level, our single-contig assemblies reveal genome-level arrangement differences. Our long-read-based pipeline to assemble *B. pertussis* genomes consistently into single contigs could therefore help to explain phenotypes which otherwise have no obvious genotypic cause.


This page is currently a work-in-progress (mostly due to data upload speed!), but will include:
- [ ] our full methodology, including any homemade code and commands used for community-built tools, plus a shell script to run either of our final pipelines
- [ ] links to our data repository, including raw and processed reads, and genome assembly tests
- [ ] extended results and links to full metadata/supplementary files
- [ ] references and other recommended reading


[Raw Albacore + Porechop reads](https://figshare.com/s/4a2a376c8d4d130b3ecb)
