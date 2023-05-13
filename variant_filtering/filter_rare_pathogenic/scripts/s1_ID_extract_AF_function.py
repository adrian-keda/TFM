import pandas as pd
import numpy as np


longfile = pd.read_csv(snakemake.input['longfile'], sep = '\t',usecols = ['ID', 'AF'])
longfile.drop_duplicates(inplace = True)

big_list =[]
for annotation in snakemake.input['annotation'][0:]:
    annot = pd.read_csv(annotation, compression = 'gzip', sep = '\t', header = 0, 
                        usecols = ['ID', 'CLNSIG', 'CLNREVSTAT', 'MetaLR_pred', 'AAChange.ensGene', 'ExonicFunc.ensGene' ,'gnomad_AF', 'gnomad_AF_popmax',
                                   'gnomad_AF_afr', 'gnomad_AF_sas', 'gnomad_AF_amr', 'gnomad_AF_eas', 'gnomad_AF_nfe', 'gnomad_AF_fin', 'gnomad_AF_asj','gnomad_AF_oth',
                                   'Feature', 'Protein_position']).drop_duplicates()
    big_list.append(annot)


big_list = pd.concat(big_list)
# Columns --> ID, FILTER, GNOMAD, ClNREVSTAT, CLNSIG


# Cleaning 'AAChange.ensGene' column
big_list['AAChange.ensGene'] = big_list['AAChange.ensGene'].apply(lambda x: x.split(';'))
big_list = big_list.explode('AAChange.ensGene').drop_duplicates()

# Split Ensembl's AAChange into a list
big_list['AAChange.ensGene'] = big_list['AAChange.ensGene'].apply(lambda x: x.split(','))

# EXPLODE the dataframe by 'AAChange.ensGene' (creates N identical rows but splitting the info in the specified field, 'AAChange.ensGene' in this case)
big_list = big_list.explode('AAChange.ensGene')

# Split 'AAChange.ensGene' column
big_list[['ens_gene', 'ens_transcript', 'ens_exon', 'ens_cDNA', 'ens_aa_change']] = big_list['AAChange.ensGene'].str.split(':', 0, expand = True)
#big_list.to_csv('/storage/scratch01/users/amaqueda/TEST_PATATA/out/A.tsv.gz', sep = '\t', index = False, compression = 'gzip')

# Clean transcripts IDs
clean_transcripts = []
for i in big_list['ens_transcript'].tolist():
    try:
        clean_transcripts.append(i.split('.')[0])
    except:
        clean_transcripts.append('PLACEHOLDER')

big_list['ens_clean_transcript'] = clean_transcripts

# Take rows in which 'Feature' == 'ens_clean_transcripts'
big_list = big_list[big_list['Feature'] == big_list['ens_clean_transcript']]



merged = longfile.merge(big_list, how = 'inner', on = ['ID'])
merged.to_csv(snakemake.output['DATAS'], sep = '\t', index = False, compression = 'gzip')