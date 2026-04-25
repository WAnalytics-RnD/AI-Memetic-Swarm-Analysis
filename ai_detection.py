import pandas as pd
from transformers import pipeline

df = pd.read_csv(r"C:\Users\Admin\Downloads\tweets_clean.csv")

print(f"Loaded {len(df)} tweets")
print("Running AI detection... this will take 20-40 minutes")

detector = pipeline("text-classification", model="roberta-base-openai-detector")

def classify(text):
    try:
        result = detector(str(text)[:512])[0]
        return result['label'], result['score']
    except:
        return "UNKNOWN", 0.0

df[['ai_label', 'ai_score']] = df['text'].apply(
    lambda x: pd.Series(classify(x))
)

df['ai_generated'] = df['ai_label'].apply(lambda x: 1 if 'AI' in x.upper() else 0)

df.to_csv(r"C:\Users\Admin\Downloads\tweets_with_ai.csv", index=False)

print(f"Done! AI memes: {df['ai_generated'].sum()}")
print(f"Human memes: {(df['ai_generated'] == 0).sum()}")