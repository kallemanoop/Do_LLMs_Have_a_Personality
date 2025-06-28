import json
import pandas as pd

INPUT_FILE = "../results/dtraw_responses.jsonl"  # Update path if needed
OUTPUT_CSV = "../results/dtscored_traits.csv"

data = []

with open(INPUT_FILE, "r", encoding="utf-8") as f:
    for line in f:
        item = json.loads(line)
        if item["score"] is not None:
            score = int(item["score"])
            if item["reversed"]:
                score = 6 - score  # reverse scoring
            data.append({
                "trait": item["trait"],
                "score": score
            })

df = pd.DataFrame(data)
summary = df.groupby("trait")["score"].agg(["count", "mean"]).reset_index()
summary.columns = ["trait", "num_items", "average_score"]

print("Dark Triad Personality Profile:")
print(summary.to_string(index=False))

summary.to_csv(OUTPUT_CSV, index=False)
print(f"\nScores saved to: {OUTPUT_CSV}")
