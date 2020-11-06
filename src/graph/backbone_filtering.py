import networkx as nx

from src.graph.disparity import calc_alpha_ptile, cut_graph, disparity_filter

G = nx.read_graphml("data/graphs/raw_similarity_graph.graphml")
print(len(G.nodes), len(G.edges))
imgs = dict(G.nodes(data=True))
img_dict = {k: v["label"] for (k, v) in imgs.items()}

nx.set_node_attributes(G, img_dict, "image")

alpha_measures = disparity_filter(G)
quantiles, num_quant = calc_alpha_ptile(alpha_measures)
alpha_cutoff = quantiles[5]

cut_graph(G, alpha_cutoff, 7)

nx.write_graphml(G, "data/graphs/backbone_7.graphml")
print(len(G.nodes), len(G.edges))
