import os
from shutil import copy2

import pandas as pd

df = pd.read_csv("data/image_data_with_clusters.tsv", sep="\t")
file_cluster = dict(zip(df["File"], df["Cluster"]))

in_path = "data/images"
out_path = "data/gmm_clusters"

for fname, cluster in file_cluster.items():
    if cluster > -1:
        copy2(os.path.join(in_path, fname), os.path.join(out_path, str(cluster), fname))
    else:
        print(cluster)
