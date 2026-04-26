import pandas as pd
df = pd.read_csv(r"C:\Users\Admin\Downloads\tweets_with_ai.csv")
tweet_counts = df.groupby("username")["id"].count().reset_index()
tweet_counts.columns = ["username", "tweet_count"]
df = df.merge(tweet_counts, on="username")
df["ai_generated"] = (df["tweet_count"] > 5).astype(int)
df.to_csv(r"C:\Users\Admin\Downloads\tweets_with_ai.csv", index=False)
print("Done!")
print("AI/automated: " + str(df["ai_generated"].sum()))
print("Human: " + str((df["ai_generated"]==0).sum()))
