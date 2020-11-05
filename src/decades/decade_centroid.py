import os
import heapq
import pickle
from shutil import copy2

import pandas as pd
import numpy as np

l = pickle.load(open("data/img_vecs.p", "rb"))
X, filenames = l[0], l[1]
X = np.asarray([np.asarray(e) for e in X])


def most_similar(pvector, fnames):
    indices = [filenames.index(e) for e in fnames if e in filenames]
    Xhat = np.asarray([X[i] for i in indices])
    sims = list(Xhat.dot(pvector))
    most_similar_values = heapq.nlargest(1, sims)
    most_similar_indices = [sims.index(e) for e in list(most_similar_values)]
    most_similar_imgs = [fnames[e] for e in most_similar_indices]
    return most_similar_imgs[0]


in_path = "data/images"
out_path = "data/centroid_imgs"
df = pd.read_csv("data/image_data_with_clusters.tsv", sep="\t")
df = df.fillna(0)
df = df[(df["Correct decade"] != "nan") & (df["Correct decade"] != 0)]
df["Correct decade"] = df["Correct decade"].astype(int)
decades = set(df["Correct decade"])
decade_range = range(min(decades), max(decades)+1, 10)
for d in decade_range:
    df_decade = df[df["Correct decade"] == d]
    decade_files = list(df_decade["File"])
    if len(decade_files) > 1:
        indices = [filenames.index(f) for f in filenames if f in filenames]
        vectors = np.asarray([X[i] for i in indices])
        mean_vector = np.mean(vectors, axis=0)
        centroid_img = most_similar(mean_vector, decade_files)
        fname = str(d) + "_" + centroid_img
        copy2(os.path.join(in_path, centroid_img), os.path.join(out_path, fname))
