import pandas as pd
from Levenshtein import distance

df = pd.read_csv(r"C:\Users\Admin\Downloads\tweets_with_ai.csv")
texts = df["text"].tolist()
ids = df["id"].tolist()

edges = []
for i in range(len(texts)):
    for j in range(i+1, min(i+50, len(texts))):
        d = distance(str(texts[i])[:100], str(texts[j])[:100])
        maxlen = max(len(str(texts[i])), len(str(texts[j])), 1)
        similarity = 1 - (d / maxlen)
        if similarity > 0.6:
            edges.append({"source": ids[i], "target": ids[j], "similarity": similarity})

edges_df = pd.DataFrame(edges)
edges_df.to_csv(r"C:\Users\Admin\Downloads\mutation_edges.csv", index=False)
print("Done!")
print("Mutation pairs found: " + str(len(edges_df)))