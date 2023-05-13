import pandas as pd
import numpy as np


# Load tables
anno = pd.read_csv(snakemake.input["anno"], sep = '\t', header = 0)
vep = pd.read_csv(snakemake.input["vep"], sep = '\t', header = 0)


# Rename Uploaded_variation column to 'Otherinfo1'
vep.rename(columns = {'Uploaded_variation':'Otherinfo1'}, inplace = True)


# Merging by Otherinfo1, renaming it to ID
merged_df = anno.merge(vep, on = 'Otherinfo1', how = 'inner')
merged_df.insert(0, "ID", merged_df.pop("Otherinfo1"))


# Save dataframe in tsv format
merged_df.to_csv(path_or_buf = snakemake.output["output"], sep = '\t', compression = 'gzip', index = False)