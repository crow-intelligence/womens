import networkx as nx

G = nx.read_graphml("data/graphs/backbone_7.graphml")
print(len(G.nodes), len(G.edges))

# eigen_centrality = nx.eigenvector_centrality(G, weight="weight")
pr = nx.pagerank(G, weight="weight", alpha=0.75)
# btw = nx.betweenness_centrality(G, weight="weight")
ebtw = nx.edge_betweenness(G, weight="weight")
vr = nx.voterank(G)
voting = dict(zip(vr,list(range(len(vr)+5, 5, -1))))
for node in G.nodes:
    if node not in voting:
        voting[node] = 1
loadcentrality = nx.load_centrality(G, weight="weight")

nx.set_node_attributes(G, pr, "PageRank")
nx.set_edge_attributes(G, ebtw, "EdgeBetweenness")
nx.set_node_attributes(G, voting, "VoteRank")
nx.set_node_attributes(G, loadcentrality, "LoadCentrality")
nx.set_node_attributes(G, dict(G.degree(weight="weight")), "WeightedDegree")

nx.write_graphml(G, "data/graphs/backbone_7_with_centralities.graphml")
