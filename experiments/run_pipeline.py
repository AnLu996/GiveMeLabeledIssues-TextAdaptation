import json
import pandas as pd
from preprocessing.clean_text import clean_text

with open("data/raw/issues.json", "r", encoding="utf-8") as f:
    issues = json.load(f)

rows = []
for issue in issues:
    text = issue["title"] + " " + issue["body"]
    rows.append({
        "id": issue["id"],
        "text": clean_text(text)
    })

df = pd.DataFrame(rows)
df.to_csv("data/processed/dataset.csv", index=False)
