import json
import pandas as pd
from collections import defaultdict

RAW_FILE="../results/big5raw_responses.jsonl"
OUTPUT_CSV="../results/big5scored_traits.csv"

data=[]
with open(RAW_FILE, "r", encoding="utf-8") as f:
    for line in f:
        entry=json.loads(line.strip())
        data.append(entry)

trait_scores = defaultdict(list)

for entry in data:
    score = entry.get("score")
    if score is None:
        continue  #skip unanswered

    #reverse if needed
    if entry["reversed"]:
        score = 6 - score

    trait_scores[entry["trait"]].append(score)

final_scores = []
for trait, scores in trait_scores.items():
    avg = round(sum(scores) / len(scores), 3)
    final_scores.append({
        "trait": trait,
        "num_items": len(scores),
        "average_score": avg
    })


df = pd.DataFrame(final_scores)
df = df.sort_values(by="trait")
df.to_csv(OUTPUT_CSV, index=False)

print("Big Five Personality Profile:")
print(df.to_string(index=False))
print("Scores saved to: {OUTPUT_CSV}")