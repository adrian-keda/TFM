import pandas as pd
import numpy as np


df = pd.read_csv(snakemake.input['tab'], sep = '\t', header = 0)


ad = df['AD']
rd = df['RD']


vaf = []
l = len(ad) # df.shape[0]

for i in range(l):
    aa = ad[i].split(',')
    if len(aa) == 2:
        vaf.append(np.round(int(aa[1]) / (int(aa[0]) + int(aa[1])), 2))
    else:
        if ad[i] == '.':
            vaf.append('.')
        else:
            vaf.append(np.round(int(ad[i]) / (int(rd[i]) + int(ad[i])), 2))


df['VAF'] = vaf
df.to_csv(snakemake.output['vaf'], sep = '\t', index = False, compression = 'gzip')