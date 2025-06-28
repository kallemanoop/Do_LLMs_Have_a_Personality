import json
import os
from datetime import datetime
import requests
from prompt_generator import generate_compliance_prompt, load_scenarios

MODEL_NAME = "meta-llama/Llama-3-70b-chat-hf" 

API_URL = f"https://api.together.xyz/v1/chat/completions"
from dotenv import load_dotenv  
load_dotenv("../../.env")
API_KEY = os.getenv("TOGETHER_API_KEY")

HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}
OUTPUT_PATH = "../results/compliance_raw_responses.jsonl"
SCENARIO_PATH = "../../data/compliance_questions.json"


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


def parse_decision(text):
    if not text:
        return None
    text = text.strip().lower()
    if "obedient" in text:
        return "obedient_action"
    elif "disobedient" in text:
        return "disobedient_action"
    elif text == "1":
        return "obedient_action"
    elif text == "2":
        return "disobedient_action"
    return None



def run_compliance_test():
    print("Running compliance test...")

    os.makedirs("../results", exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8") as out_file:
        scenarios = load_scenarios(SCENARIO_PATH)

        for s in scenarios:
            prompt = generate_compliance_prompt(s)

            try:
                response = query_together(prompt)
                decision = parse_decision(response)

                result = {
                    "timestamp": datetime.now().isoformat(),
                    "model": MODEL_NAME,
                    "scenario_id": s["id"],
                    "pressure": s["pressure"],
                    "context": s["context"],
                    "obedient_action": s["obedient_action"],
                    "disobedient_action": s["disobedient_action"],
                    "moral_violation": s["moral_violation"],
                    "expected_preference": s["expected_preference"],
                    "prompt": prompt,
                    "response": response,
                    "model_decision": decision
                }

                print(f"Q{s['id']:03}: [{decision}] {response}")
                out_file.write(json.dumps(result) + "\n")

            except Exception as e:
                print(f"Error in Q{s['id']}: {e}")

    print("Compliance test completed. Results saved.")


if __name__ == "__main__":
    run_compliance_test()
