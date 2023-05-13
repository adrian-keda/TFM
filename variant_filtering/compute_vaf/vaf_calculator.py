import pandas as pd
import numpy as np


df = pd.read_csv(snakemake.input['tab'], sep = '\t', header = 0)


ad = df['AD']
dp = df['DP']
rd = df['RD']

vaf = []
l = len(ad)

for i in range(l):
    aa = ad[i].split(',')
    if len(aa) == 2:
        vaf.append( int(aa[1]) / (int(aa[0]) + int(aa[1])))
    else:
        if ad[i] == '.':
            vaf.append('.')
        else:
            vaf.append( int(ad[i]) / (int(rd[i]) + int(ad[i])))


df['VAF'] = vaf

df.to_csv(snakemake.output['vaf'], sep = '\t', index = False)