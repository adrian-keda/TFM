import pandas as pd


# Read annotation file
annotation = pd.read_csv(snakemake.input['annot'], sep = '\t', header = 0, compression = 'gzip')



### Keep rare variants
### Apply filter to variants with no information for gnomAD
dots = annotation[annotation['gnomad_AF'] == '.']
dots_rare = dots[dots['AF'] < 0.01]

### Apply filter to variants with information in gnomAD
no_dots = annotation[annotation['gnomad_AF'] != '.']

# Changing . in gnomad_AF columns
no_dots[['gnomad_AF', 'gnomad_AF_nfe', 'gnomad_AF_afr', 'gnomad_AF_amr', 'gnomad_AF_eas', 'gnomad_AF_sas']] = no_dots[['gnomad_AF', 'gnomad_AF_nfe', 'gnomad_AF_afr', 'gnomad_AF_amr', 'gnomad_AF_eas', 'gnomad_AF_sas']].replace('.','0')

# Changing type from str to float
no_dots = no_dots.astype({'gnomad_AF':'float','gnomad_AF_nfe':'float','gnomad_AF_afr':'float','gnomad_AF_amr':'float','gnomad_AF_eas':'float','gnomad_AF_sas':'float'})

# Filter
no_dots_rare = no_dots[(no_dots['gnomad_AF'] < 0.001) & (no_dots['gnomad_AF_nfe'] < 0.001) & (no_dots['gnomad_AF_afr'] < 0.001) & (no_dots['gnomad_AF_amr'] < 0.001) & (no_dots['gnomad_AF_eas'] < 0.001) & (no_dots['gnomad_AF_sas'] < 0.001) & (no_dots['AF'] < 0.01)]

# Combine both
rare = pd.concat([dots_rare, no_dots_rare])



### Keep pathogenic variants
# Keep PTVs
ptvs = annotation[annotation['ExonicFunc.ensGene'].isin(['frameshift substitution','.','startloss','stopgain','stoploss'])]

# Keep ClinVar
ClinVar = annotation[(annotation['CLNREVSTAT'].isin(['criteria_provided,_multiple_submitters,_no_conflicts','practice_guideline','reviewed_by_expert_panel'])
                    & annotation['CLNSIG'].isin(['Pathogenic', 'Likely_pathogenic', 'Pathogenic/Likely_pathogenic', 'risk_factor',
                                                 'Pathogenic|_risk_factor', 'Likely_pathogenic|_risk_factor', 'Pathogenic/Likely_pathogenic|_risk_factor']))]

# Concat PTVs and ClinVar. Then remove duplicates
pathogenic = pd.concat([ptvs, ClinVar]).drop_duplicates()



### Add rare and pathogenic information to the annotation file
annotation['is_rare'] = annotation['ID'].isin(rare['ID'].tolist())
annotation['is_pathogenic'] = annotation['ID'].isin(pathogenic['ID'].tolist())



### Save table
annotation.drop_duplicates().to_csv(snakemake.output['filters'], sep = '\t', index = None, compression = 'gzip')