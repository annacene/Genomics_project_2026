# Genomics_project_2026

Rare genetic disorders present a significant clinical challenge due to their extreme heterogeneity and the need for rapid and accurate molecular diagnosis. In this study, we analysed a cohort of 10 family trios, simulated from exome sequencing data, suspected of harbouring Mendelian disorders to identify the causative genomic variants. We focused our analysis on chromosome 20, exploring three primary inheritance models: autosomal recessive, autosomal inherited dominant, and autosomal de novo dominant.  

The aim of this study is to bridge the gap between complex genomic row data and a definitive clinical diagnosis, with a computational framework. Our analysis successfully identified several high-impact mutations linked to severe disorders. 

We developed a Python-based pipeline to aggregate all the steps of the transition from raw FASTQ files to filtered variants, to isolate the possible pathogenic ones from background noise. We utilised Bowtie2 for alignment to the GRCh38 reference genome and Freebayes for joint variant calling, finally, variants were annotated and prioritized using Ensembl’s Variant Effect Predictor (VEP). 
