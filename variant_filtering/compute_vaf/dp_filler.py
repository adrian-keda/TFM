import pandas as pd
import numpy as np


df = pd.read_csv(snakemake.input['vaf'], sep = '\t', header = 0)


ad = df['AD'].tolist()
gt = df['GT'].tolist()
dp = df['DP'].tolist()
rd = df['RD'].tolist()

dp_corr = []

l = len(dp)

for i in range (l):
    if dp[i] == '.':
        aa = ad[i].split(',')
        if gt[i] == '0/1':
            if len(aa) == 2:
                dp_corr.append(int(aa[0]) + int(aa[1]))
            else:
                try:
                    dp_corr.append(int(aa) + int(rd[i]))
                except:
                    dp_corr.append('.')
        else:
            if len(aa) == 2:
                dp_corr.append(int(aa[0]) + int(aa[1]))
            else:
                try:
                    dp_corr.append(int(ad[i]))
                except:
                    dp_corr.append('.')
    else:
        dp_corr.append(dp[i])

df['DP']= dp_corr
df.to_csv(snakemake.output['dp'], sep = '\t', index = False)