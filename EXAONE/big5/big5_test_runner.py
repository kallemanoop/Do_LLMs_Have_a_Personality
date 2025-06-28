import json
import os
import requests
from datetime import datetime
from prompt_generator import load_questions, generate_prompt


MODEL_NAME = "lgai/exaone-3-5-32b-instruct" 

API_URL = f"https://api.together.xyz/v1/chat/completions"
from dotenv import load_dotenv  
load_dotenv("../../.env")
API_KEY = os.getenv("TOGETHER_API_KEY")
HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

def query_together(prompt):
    payload = {
        "model": MODEL_NAME,
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "max_tokens": 20,
        "temperature": 0.7,
        "top_p": 0.9,
    }

    response = requests.post(API_URL, headers=HEADERS, json=payload)
    response.raise_for_status()
    result = response.json()

    return result["choices"][0]["message"]["content"].strip()

def parse_response(text):
    if not text:
        return None

    text = text.strip().lower()

    # Try strict match first
    if text in ["1", "2", "3", "4", "5"]:
        return int(text)

    # Look for [n] pattern
    for i in range(1, 6):
        if f"[{i}]" in text:
            return i

    # Loose fallback
    for i in range(1, 6):
        if f"{i}" in text:
            return i

    return None

def run_big5_test():
    print("Starting test via Together AI API...")

    questions = load_questions("../../data/big5_questions.json")
    os.makedirs("../results", exist_ok=True)
    out_file = open("../results/big5raw_responses.jsonl", "w", encoding="utf-8")

    for q in questions:
        prompt = generate_prompt(q)

        try:
            output = query_together(prompt)
            reply = output.replace(prompt, "").strip().split("\n")[0]
            score = parse_response(reply)

            result = {
                "timestamp": datetime.now().isoformat(),
                "model": MODEL_NAME,
                "trait": q['trait'],
                "question_id": q['id'],
                "question_text": q['text'],
                "reversed": q['reversed'],
                "prompt": prompt,
                "response": reply,
                "score": score
            }

            print(f"Q{q['id']:03}: [{score}] {reply}")
            out_file.write(json.dumps(result) + "\n")
            out_file.flush()

        except Exception as e:
            print(f"Error at Q{q['id']}: {e}")

    out_file.close()
    print("Test complete. Results saved.")

if __name__ == "__main__":
    run_big5_test()