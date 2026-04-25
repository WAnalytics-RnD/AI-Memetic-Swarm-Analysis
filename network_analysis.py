import pandas as pd
import networkx as nx

nodes = pd.read_csv(r"C:\Users\Admin\Downloads\tweets_with_ai.csv")
edges = pd.read_csv(r"C:\Users\Admin\Downloads\mutation_edges.csv")

G = nx.DiGraph()

for _, row in nodes.iterrows():
    G.add_node(row["id"], ai_generated=row["ai_generated"])

for _, row in edges.iterrows():
    G.add_edge(row["source"], row["target"], weight=row["similarity"])

degree = dict(G.degree())
clustering = nx.clustering(G.to_undirected())

nodes["degree"] = nodes["id"].map(degree)
nodes["clustering"] = nodes["id"].map(clustering)
nodes["virality_score"] = nodes["degree"]

nodes.to_csv(r"C:\Users\Admin\Downloads\tweets_final.csv", index=False)
nx.write_edgelist(G, r"C:\Users\Admin\Downloads\network_edgelist.txt")

print("Done!")
print("Nodes: " + str(G.number_of_nodes()))
print("Edges: " + str(G.number_of_edges()))
print("Density: " + str(round(nx.density(G), 6)))