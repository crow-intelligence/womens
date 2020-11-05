import os
import heapq
import pickle
from shutil import copy2

import pandas as pd
import networkx as nx
import numpy as np
from sklearn.neighbors import NearestNeighbors

l = pickle.load(open("data/img_vecs.p", "rb"))
X, filenames = l[0], l[1]
X = np.asarray([np.asarray(e) for e in X])

nbrs = NearestNeighbors(n_neighbors=6, algorithm='ball_tree').fit(X)
distances, indices = nbrs.kneighbors(X)


edges = {}
for i in range(len(distances)):
    node_name = filenames[i]
    neighbors = [filenames[e] for e in indices[i]][1:]
    weights = list(distances[i])[1:]
    weights = [1/(e+1) for e in weights]
    for j in range(len(neighbors)):
        names_sorted = sorted([node_name, neighbors[j]])
        t = (names_sorted[0], names_sorted[1])
        if t in edges:
            edges[t] = (edges[t] + weights[j]) / 2
        else:
            edges[t] = weights[j]

G = nx.Graph()

for filename in filenames:
    G.add_node(filename, label=filename)

for k,v in edges.items():
    G.add_edge(k[0], k[1], weight=v)

nx.write_graphml(G, "data/graphs/raw_similarity_graph.graphml")
