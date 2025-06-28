from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
import torch
import json
import os
from datetime import datetime
from dt_prompt_generator import load_questions, generate_dark_prompt
import requests


MODEL_NAME = "arcee-ai/AFM-4.5B-Preview"
#MODEL_NAME2 = "HuggingFaceH4/zephyr-7b-alpha"
API_URL = f"https://api.together.xyz/v1/chat/completions"
from dotenv import load_dotenv
load_dotenv("../../.env")
API_KEY = os.getenv("TOGETHER_API_KEY")

headers = {
    "Authorization": f"Bearer {API_KEY}"
}
#print(f"Loading model {MODEL_NAME}...")

def query_together(prompt):
    payload = {
        "model": MODEL_NAME,
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "max_tokens": 30,
        "temperature": 0.7,
        "top_p": 0.9
    }

    response = requests.post(API_URL, headers=headers, json=payload)
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


def run_dt_test():
    print("Starting test via Together AI API...")

    questions = load_questions("../../data/dark_triad_questions.json")
    os.makedirs("../results", exist_ok=True)
    out_file = open("../results/dtraw_responses.jsonl", "w", encoding="utf-8")

    for q in questions:
        prompt = generate_dark_prompt(q)

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
    run_dt_test()
