import json

def load_questions(path=r"C:\Users\kalle\Desktop\Anoop-Projects\Do_LLMs_Have_a_Personality\data\big5_questions.json"):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def generate_prompt(question):
    return (
        f"You are participating in a psychological study. Respond only with a number between 1 and 5.\n\n"
        f"How much do you agree with the following statement:\n\n"
        f"\"{question['text']}\"\n\n"
        f"[1] Strongly Disagree\n"
        f"[2] Disagree\n"
        f"[3] Neutral\n"
        f"[4] Agree\n"
        f"[5] Strongly Agree\n\n"
        f"Your response (just the number):"
    )
