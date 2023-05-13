import pandas as pd
import numpy as np


df = pd.read_csv(snakemake.input['annotation'], sep = '\t', header = 0, compression = 'gzip')
max_vars = len(df['ID'].unique())


# Filter variants by their consequence
list_consequence_interest = ['downstream_gene_variant', 'intergenic_variant', 'intron_variant','intron_variant,NMD_transcript_variant',
                             'intron_variant,non_coding_transcript_variant', 'mature_miRNA_variant', 'non_coding_transcript_exon_variant',
                             'non_coding_transcript_variant', 'upstream_gene_variant']


consequence = df['Consequence'].tolist()
bool_list = [False if i in list_consequence_interest else True for i in consequence] # Boolean list to pick rows later
df = df.loc[bool_list]
consequence_vars = len(df['ID'].unique())


# Filter variants which affect the canonical isotope
df = df[df['CANONICAL'] == 'YES']
canonical_vars = len(df['ID'].unique())


df.to_csv(snakemake.output['result'], compression = 'gzip', sep = '\t', index = False)
count = pd.DataFrame({'Index' : ['Input_variants', 'Consequence_variants', 'Canonical_variants'], 'Number_variants' : [max_vars, consequence_vars, canonical_vars]})
count.to_csv(snakemake.output['table'], sep = '\t', index = False)
