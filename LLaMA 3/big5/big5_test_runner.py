import json
import os
import requests
from datetime import datetime
from prompt_generator import load_questions, generate_prompt


MODEL_NAME = "meta-llama/Llama-3-70b-chat-hf" 

API_URL = f"https://api.together.xyz/v1/chat/completions"
API_KEY = "b4279b181c6584d4adc267ffa0c28f37ffed0a2bcd52f155afdff4e7c3efbac7" 
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
    for i in range(1, 6):
        if f"[{i}]" in text or text.strip() == str(i):
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
