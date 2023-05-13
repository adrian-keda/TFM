import pandas as pd
import numpy as np


base = pd.read_csv(snakemake.input['tables'][0], sep = '\t', header = 0)
base = base.rename(columns = {'Number_variants' : snakemake.input['tables'][0].split('/')[-1].split('.')[0]})


for df in snakemake.input['tables'][1:]:
    to_merge = pd.read_csv(df, sep = '\t', header = 0)
    base = base.merge(to_merge, on = 'Index')
    base.rename(columns = {'Number_variants' : df.split('/')[2].split('.')[0]}, inplace = True)

base.fillna(0, inplace = True)
base['Total_variants'] = base[base.columns[2:]].sum(axis=1)


save_df = base[['Index', 'Total_variants']]
save_df['Frequency'] = save_df['Total_variants'] / 21617807

save_df.to_csv(snakemake.output['combined'], sep = '\t', index = False)