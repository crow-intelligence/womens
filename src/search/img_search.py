import heapq
import os
import pickle
from shutil import copy2, rmtree


import numpy as np

l = pickle.load(open("data/img_vecs.p", "rb"))
X, filenames = l[0], l[1]
X = np.asarray([np.asarray(e) for e in X])


def most_similar(pic, n):
    idx = filenames.index(pic)
    pvector = X[idx]
    sims = list(X.dot(pvector))
    most_similar_values = heapq.nlargest(n+1, sims)
    most_similar_indices = [sims.index(e) for e
                            in list(most_similar_values)]
    most_similar_imgs = [filenames[e] for e in most_similar_indices
                         if filenames[e] != pic]
    return most_similar_imgs


def query_imgs(pic, n, folder):
    sim_imgs = most_similar(pic, n)
    out_path = os.path.join("data/queries", folder)
    in_path = "data/images"
    if os.path.isdir(out_path):
        rmtree(out_path)
    os.mkdir(out_path)
    for img in sim_imgs:
        copy2(os.path.join(in_path, img), os.path.join(out_path, img))
    copy2(os.path.join(in_path, pic), os.path.join(out_path, "00_query_" + pic))


query_imgs(filenames[25], 20, "test")
