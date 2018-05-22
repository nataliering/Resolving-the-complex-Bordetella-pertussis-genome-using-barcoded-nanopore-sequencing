# Resolving the complex *Bordetella pertussis* genome using barcoded nanopore sequencing

**Natalie Ring, Jonathan Abrahams, Andrew Preston \& Stefan Bagby**      
*Department of Biology and Biochemistry, University of Bath*

This repository is currently a work-in-progress (mostly due to data upload speed!), but will support both our paper (once submitted) and poster presentation at London Calling 2018. Content will include:
- [ ] our full methodology, including any homemade code and commands used for community-built tools, plus a shell script to run either of our final pipelines (hybrid or long-read-only)
- [ ] links to our data repository, including raw and processed reads (fastq), and genome assembler test intermediates and final assemblies
- [ ] extended results and links to full metadata/supplementary files
- [ ] references and other recommended reading

N.B. not all hyperlinks are functional as yet

## Abstract
*Bordetella pertussis*, the pathogen responsible for whooping cough, has a complex genome with high GC content and hundreds of repetitive sections, each longer than 1kb. While short-read sequencing has been unable to resolve the structure of the genome, long-read sequencing could enable accurate single-contig *B. pertussis* assembly.  

We have used barcoded MinION sequencing to resolve genome structures of five UK *B. pertussis* strains with a single flow cell. Extensive testing of available data analysis tools revealed that our optimal long-read-only assembly pipeline includes Canu read correction, Flye assembly and Nanopolish polishing, and can produce single-contig assemblies approaching 99.6% identity.
Although *B. pertussis* is a monomorphic organism at base level, our single-contig assemblies reveal genome-level arrangement differences. Our long-read-based pipeline to assemble *B. pertussis* genomes consistently into single contigs could therefore help to explain phenotypes which otherwise have no obvious genotypic cause.

## Method
### Flow cell trials        
We ran five different MinION flow cell trials between 2015 and 2017, using both R7 and R9/R9.4 flow cells (see table 1). Having established that the yield of a single R9.4 flow cell would enable the sequencing of multiple strains per flow cell with the use of barcodes, we took forward highest quality barcoded read set (in terms of yield, % identity, etc.) to assembly tests.

**Table 1: Flow cell trials**

|Date|Flow cell chemistry|Library Prep|*B. pertussis* strain(s)|Basecaller|
|----|-------------------|------------|------------------------|----------|
|July 2015|R7|2D Genomic DNA (deprecated)| UK48, UK76|Metrichor|
|March 2017|R9|1D Genomic DNA by ligation (SQK-LSK108)| UK76|Albacore (early version)|
|June 2017|R9.4|1D Low input genomic DNA with PCR (SQK-LSK108)| 18323|MinKNOW v.Jun17|
|June 2017|R9.4|1D Low input genomic DNA by PCR barcoding (SQK-LWB001)| UK36, UK38, UK39, UK48, UK76|MinKNOW v.Jun17|
|June 2017|R9.4|1D Native barcoding genomic DNA (EXP-NBD103 and SQK-LSK108) (half of each sample underwent end-repair)| UK36, UK38, UK39, UK48, UK76|MinKNOW v.Jun17|


### Assembler testing - long-read-only                 
We used concurrent basecalling by MinKNOW to produce fastq files from the raw fast5s throughout our native barcoded sequencing run. The raw fastq files were then demultiplexed using [Porechop v.0.2.1](https://github.com/rrwick/Porechop). For the natively barcoded run, we had subjected half of each strain's sample to the optional end-repair step. This meant that each strain was represented by two different barcodes: one for the end-repaired reads, and one for the non-end-repaired reads. As our results showed little difference between the two samples for each strain, we pooled the end-repaired and non-end-repaired reads for further processing.

The reads for one of our barcoded strains, UK36, were used to identify the best assembly strategy for our *B. pertussis* data.
We identified the most widely used/recommended community-built *de novo* assembly tools suitable for long reads as:
- [ABruijn (now called Flye)](https://github.com/fenderglass/Flye)
- [Canu](https://github.com/marbl/canu)
- [Miniasm with Minimap](https://github.com/lh3/miniasm)
- [Unicycler](https://github.com/rrwick/Unicycler)

Alongside this variety of assembly tools, we also tested:
- pre-assembly read correction with Canu vs no pre-assembly read correction
- read filtering from the ~400x coverage generated down to the best 40x coverage with [Filtlong](https://github.com/rrwick/Filtlong)
- read filtering from the ~400x coverage generated down to the best 100x coverage with Filtlong
- polishing with 1 to 5 rounds of [Racon](https://github.com/isovic/racon) and/or a single round of [Nanopolish](https://github.com/jts/nanopolish)

We exhaustively tested every possible combination of the above options. Assemblies can continue to improve with multiple rounds of Racon polishes, so for the first few trials we continued to polish each assembly until no further improvement was seen. After these first few trials, it was apparent that most assemblies had peaked by the fitfth round of Racon polishing; for all subsequent trials we performed 5 rounds of Racon polishing. This meant that for each assembly tool option, we produced 28 draft assemblies (see table 2).

**Table 2: exhaustively testing all possible combinations of assembly tool, read correction, read filtering, Racon polishing and Nanopolishing**

|#|Pre-correction|Read filtering|Assembly|Racon|Nanopolish|
|-|--------------|--------------|--------|-----|----------|
|1|No|No|Yes|No|No|
|2|No|No|Yes|1|No|
|3|No|No|Yes|2|No|
|4|No|No|Yes|3|No|
|5|No|No|Yes|4|No|
|6|No|No|Yes|5|No|
|7|No|No|Yes|Best|Yes|
|8|Yes|No|Yes|No|No|
|9|Yes|No|Yes|1|No|
|10|Yes|No|Yes|2|No|
|11|Yes|No|Yes|3|No|
|12|Yes|No|Yes|4|No|
|13|Yes|No|Yes|5|No|
|14|Yes|No|Yes|Best|Yes|
|15|No|40x|Yes|No|No|
|16|No|40x|Yes|1|No|
|17|No|40x|Yes|2|No|
|18|No|40x|Yes|3|No|
|19|No|40x|Yes|4|No|
|20|No|40x|Yes|5|No|
|21|No|40x|Yes|Best|Yes|
|22|No|100x|Yes|No|No|
|23|No|100x|Yes|1|No|
|24|No|100x|Yes|2|No|
|25|No|100x|Yes|3|No|
|26|No|100x|Yes|4|No|
|27|No|100x|Yes|5|No|
|28|No|100x|Yes|Best|Yes|

### Assembler testing - hybrid
If they are available, including highly-accurate Illumina short reads should improve the accuracy of a long read assembly. For the five strains we sequenced, previously published Illumina reads were available from the NCBI's [SRA](https://www.ncbi.nlm.nih.gov/sra) (table 3) [1]. There are three potential ways to produce a hybrid assembly:
1. Assemble with short reads, scaffold with long reads (e.g. [SPAdes](http://cab.spbu.ru/software/spades/))
2. Assemble with long reads, polish with short reads (e.g. Canu + [Pilon](https://github.com/broadinstitute/pilon))
3. A combination of 1 and 2 (e.g. Unicycler, which combines Illumina contigs produced with SPAdes with Nanopore long reads and re-assembles them all using Miniasm, followed by long-read-polishing with Racon, then short-read-polishing with Pilon).

Again, we tested all possible combinations of these options, using the best option for each assembler from the long-read-only tests. Like Racon, we found from the first few tests that assembly accuracy peaked before the fifth Pilon round. This produced another 18 draft assemblies (table 4). 

**Table 3: SRA IDs of Illumina reads generated in 2012/13**

|*B. pertussis* strain|SRA ID|
|---------------------|------|
|UK36| ERR212376|
|UK38| ERR212378|
|UK39| ERR212379|
|UK48| ERR212388|
|UK76| ERR316415|



**Table 4:  hybrid combinations trialled. N.B. The results of the first SPAdes trial were so poor that no further polishing was attempted**

|#|Pre-correction|Read filtering|Assembler|Short reads|Racon|Nanopolish|Pilon|
|-|--------------|--------------|---------|-----------|-----|----------|-----|
|1|No|No|Canu|No|Best|Yes|1|
|2|No|No|Canu|No|Best|Yes|2|
|3|No|No|Canu|No|Best|Yes|3|
|4|No|No|Canu|No|Best|Yes|4|
|5|No|No|Canu|No|Best|Yes|5|
|6|Yes|No|Flye|No|No|Yes|1|
|7|Yes|No|Flye|No|No|Yes|2|
|8|Yes|No|Flye|No|No|Yes|3|
|9|Yes|No|Flye|No|No|Yes|4|
|10|Yes|No|Flye|No|No|Yes|5|
|11|Yes|No|Miniasm + Minimap|No|Best|Yes|1|
|12|Yes|No|Miniasm + Minimap|No|Best|Yes|2|
|13|Yes|No|Miniasm + Minimap|No|Best|Yes|3|
|14|Yes|No|Miniasm + Minimap|No|Best|Yes|4|
|15|Yes|No|Miniasm + Minimap|No|Best|Yes|5|
|16|Yes|No|Unicycler|Yes|No|No|No|
|17|Yes|No|Unicycler|Yes|No|Yes|No|
|18|Yes|No|SPAdes|Yes|No|No|No|


N.B. The latest Racon release also facilitates polishing with short reads. We compared multiple rounds of Racon short-read-polishing with the respective Pilon short-read-polishing rounds for several of our draft assemblies, and found minimal difference. Consequently, we did not add a "Racon short-read" polishing option to our hybrid tests.

### Basecaller comparison
Whilst we were conducting our assembler comparisons, it became apparent that alternative basecallers may produce significantly more accurate data that the intrinsic MinKNOW basecalling [2]. Consequently, we returned to our raw fast5 files, and re-basecalled them using Albacore v2.1.3. This version of Albacore is capable of demultiplexing barcoded samples; we also re-demultiplexed the Albacore fastq reads using Porechop, only keeping those reads which were placed into the same barcode bins by both demultiplexing tools. This should have minimised barcode contamination between our samples.

Having determined that the Albacore + Porechop reads had a lower raw error rate than the MinKNOW + Porechop reads, we re-conducted all assembler testing detailed above, in case the more accurate raw reads were better processed by a different tool.

### Assessing raw read accuracy
We compared our raw nanopore reads to the *B. pertussis* reference strain, Tohama I, and an Illumina-only assembly for each strain respectively. The Illumina-only assembly was generated using [ABySS](https://github.com/bcgsc/abyss) and the previously downloaded reads from the SRA, whilst the reference genome was downloaded from the [NCBI](https://www.ncbi.nlm.nih.gov/genome/1008?genome_assembly_id=170243) (RefSeq accession: NC_002929.2). 

Each set of reads was compared first to the Tohama I genome using BWA MEM followed by Samtools Stats to generate an "error rate", then to the ABySS genome using the same process.



### Results

Full results from all assembler combinations for both MinKNOW and Albacore basecalled reads can be viewed/downloaded [here](https://figshare.com/s/8cab70ab692ef95ce794).


### Raw read sets
[Raw MinKNOW + Porechop reads]()                     
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

### References
1. [Sealey KL, Harris SR, Fry NK, Hurst LD, Gorringe AR et al. Genomic analysis of isolates from the United Kingdom 2012 pertussis outbreak reveals that vaccine antigen genes are unusually fast evolving. The Journal of infectious diseases 2015;212(2):294-301](https://academic.oup.com/jid/article/212/2/294/890134])
2. [Wick RR, Judd LM, Holt KE. Comparison of Oxford Nanopore basecalling tools. 2017.](https://github.com/rrwick/Basecalling-comparison)
