import pandas as pd
import networkx as nx

nodes = pd.read_csv(r"C:\Users\Admin\Downloads\tweets_final.csv")
edges = pd.read_csv(r"C:\Users\Admin\Downloads\mutation_edges.csv")

G = nx.DiGraph()
for _, row in nodes.iterrows():
    G.add_node(row["id"], ai_generated=row["ai_generated"])
for _, row in edges.iterrows():
    G.add_edge(row["source"], row["target"])

ai_nodes = [n for n, d in G.nodes(data=True) if d.get("ai_generated") == 1]
human_nodes = [n for n, d in G.nodes(data=True) if d.get("ai_generated") == 0]

AI = G.subgraph(ai_nodes)
HU = G.subgraph(human_nodes)

ai_u = AI.to_undirected()
hu_u = HU.to_undirected()

print("=== AI Subnetwork ===")
print("Nodes: " + str(AI.number_of_nodes()))
print("Edges: " + str(AI.number_of_edges()))
print("Density: " + str(round(nx.density(AI), 6)))
print("Avg Clustering: " + str(round(nx.average_clustering(ai_u), 6)))

print("")
print("=== Human Subnetwork ===")
print("Nodes: " + str(HU.number_of_nodes()))
print("Edges: " + str(HU.number_of_edges()))
print("Density: " + str(round(nx.density(HU), 6)))
print("Avg Clustering: " + str(round(nx.average_clustering(hu_u), 6)))

print("")
print("=== Ratios (AI / Human) ===")
print("Density ratio: " + str(round(nx.density(AI) / nx.density(HU), 3)))
print("Clustering ratio: " + str(round(nx.average_clustering(ai_u) / nx.average_clustering(hu_u), 3)))