import pandas as pd
import os

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DATA_DIR = os.path.join(BASE_DIR, "data")

top_hits = pd.read_csv(os.path.join(DATA_DIR, "top50_songs.csv"))
non_hits = pd.read_csv(os.path.join(DATA_DIR, "non_hit_songs.csv"))

df = pd.concat([top_hits, non_hits], ignore_index=True)
df = df.drop(columns=["id", "name", "artist"])
df = df.dropna()
df = df.sample(frac=1, random_state=42).reset_index(drop=True)

df.to_csv(os.path.join(DATA_DIR, "cleaned_songs.csv"), index=False)
