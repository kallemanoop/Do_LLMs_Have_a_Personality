from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
import torch
import json
import os
from datetime import datetime
from dt_prompt_generator import load_questions, generate_dark_prompt
import requests


MODEL_NAME = "mistralai/Mixtral-8x7B-Instruct-v0.1"
#MODEL_NAME2 = "HuggingFaceH4/zephyr-7b-alpha"
API_URL = f"https://api-inference.huggingface.co/models/{MODEL_NAME}"
HF_TOKEN = "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"

headers = {
    "Authorization": f"Bearer {HF_TOKEN}"
}
#print(f"Loading model {MODEL_NAME}...")

def query_huggingface(prompt):
    payload = {
        "inputs": prompt,
        "parameters": {
            "max_new_tokens": 30,
            "temperature": 0.7,
            "top_p": 0.9
        }
    }
    response = requests.post(API_URL, headers=headers, json={
    "inputs": prompt,
    "parameters": {
        "max_new_tokens": 10,
        "do_sample": False,
        "return_full_text": False
    }
})
    response.raise_for_status()
    result = response.json()
    return result[0]['generated_text'] if isinstance(result, list) else ""

def parse_response(text):
    if not text:
        return None
    for i in range(1, 6):
        if f"[{i}]" in text or text.strip() == str(i):
            return i
    return None


def run_dt_test():
    print("Starting test via Hugging Face Inference API...")

    questions = load_questions("../data/dark_triad_questions.json")
    os.makedirs("../results", exist_ok=True)
    out_file = open("../results/dtraw_responses.jsonl", "w", encoding="utf-8")

    for q in questions:
        prompt = generate_dark_prompt(q)

        try:
            output = query_huggingface(prompt)
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
