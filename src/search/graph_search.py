import networkx as nx

G = nx.read_graphml("data/graphs/backbone_7_with_centralities.graphml")
print(len(G.nodes), len(G.edges))


def get_path(source, target, weights=False):
    try:
        if weights:
            ll = nx.shortest_path(G, source=source, target=target, weight="weight")
            if len(ll) == 2:
                return "Neighbors"
            else:
                return [e for e in ll if e != source and e != target]
        else:
            ll = nx.shortest_path(G, source=source, target=target)
            if len(ll) == 2:
                return "Neighbors"
            else:
                return [e for e in ll if e != source and e != target]
    except Exception as e:
        return []


def get_reachable_nodes(source, weights=False):
    try:
        if weights:
            ll = list(nx.shortest_path(G, source=source, weight="weight").values())
            return set([item for sublist in ll for item in sublist if item != source])
        else:
            ll = list(nx.shortest_path(G, source=source).values())
            return set([item for sublist in ll for item in sublist if item != source])
    except Exception as e:
        return []


nodes = list(G.nodes)
print(get_path(nodes[11], "6cb711a74948d7e9903696409583c23c.jpg", weights=True))
print(get_reachable_nodes(nodes[11]))
