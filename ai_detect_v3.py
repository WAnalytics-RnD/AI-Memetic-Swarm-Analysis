import pandas as pd
import numpy as np
import re

df = pd.read_csv(r"C:\Users\Admin\Downloads\tweets_with_ai.csv")
df["date"] = pd.to_datetime(df["date"], utc=True)
df = df.sort_values(["username", "date"]).reset_index(drop=True)

print("Running temporal burst detection...")

# For each user, calculate seconds between consecutive tweets
def burst_features(group):
    group = group.sort_values("date")
    timestamps = group["date"].tolist()
    if len(timestamps) < 2:
        group["min_gap_seconds"] = 9999
        group["burst_count"] = 0
    else:
        gaps = []
        for i in range(1, len(timestamps)):
            gap = (timestamps[i] - timestamps[i-1]).total_seconds()
            gaps.append(abs(gap))
        min_gap = min(gaps)
        burst_count = sum(1 for g in gaps if g < 10)
        group["min_gap_seconds"] = min_gap
        group["burst_count"] = burst_count
    return group

df = df.groupby("username", group_keys=False).apply(burst_features)

# Burst signal: posts within 10 seconds of another post from same account
df["temporal_ai"] = ((df["min_gap_seconds"] < 10) | (df["burst_count"] >= 2)).astype(int)

print("Running linguistic feature detection...")

def linguistic_score(text):
    text = str(text)
    score = 0

    # Very short text unlikely to be AI
    if len(text) < 30:
        return 0

    # Hashtag spam (more than 4 hashtags = likely automated)
    hashtags = len(re.findall(r'#\w+', text))
    if hashtags > 4:
        score += 2

    # No punctuation variation (AI tends to be uniform)
    punct = len(re.findall(r'[.!?]', text))
    if punct == 0 and len(text) > 80:
        score += 1

    # Repetitive sentence length (AI writes very uniform sentences)
    sentences = re.split(r'[.!?]+', text)
    sentences = [s.strip() for s in sentences if len(s.strip()) > 10]
    if len(sentences) >= 2:
        lengths = [len(s) for s in sentences]
        variance = np.var(lengths)
        if variance < 20:
            score += 1

    # No typos or informal language markers
    informal = len(re.findall(r'\b(lol|omg|wtf|gonna|wanna|gotta|tbh|imo|ngl)\b', text.lower()))
    if informal == 0 and len(text) > 100:
        score += 1

    # All caps words (human emotional expression)
    caps_words = len(re.findall(r'\b[A-Z]{3,}\b', text))
    if caps_words > 0:
        score -= 1

    return max(score, 0)

df["linguistic_score"] = df["text"].apply(linguistic_score)
df["linguistic_ai"] = (df["linguistic_score"] >= 2).astype(int)

# Composite: count how many signals fire
df["signal_count"] = (
    df["ai_generated"] +        # frequency signal
    df["temporal_ai"] +          # temporal burst signal
    df["linguistic_ai"]          # linguistic signal
)

# Classification tiers
def classify(row):
    if row["signal_count"] >= 2:
        return 2  # High confidence AI
    elif row["signal_count"] == 1:
        return 1  # Medium confidence
    else:
        return 0  # Human

df["composite_ai"] = df.apply(classify, axis=1)

df.to_csv(r"C:\Users\Admin\Downloads\tweets_v3.csv", index=False)

print("\n=== Composite Classification Results ===")
print(f"Total tweets: {len(df)}")
print(f"High confidence AI (2+ signals): {(df['composite_ai'] == 2).sum()}")
print(f"Medium confidence AI (1 signal): {(df['composite_ai'] == 1).sum()}")
print(f"Human (0 signals):               {(df['composite_ai'] == 0).sum()}")
print(f"\nSignal breakdown:")
print(f"  Frequency signal:  {df['ai_generated'].sum()}")
print(f"  Temporal signal:   {df['temporal_ai'].sum()}")
print(f"  Linguistic signal: {df['linguistic_ai'].sum()}")
print("\nSaved to tweets_v3.csv")