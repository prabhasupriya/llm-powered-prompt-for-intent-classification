import os
import json
import openai # We still use the openai library because Groq is compatible!
from prompts import EXPERT_PROMPTS, CLASSIFIER_SYSTEM_PROMPT
from dotenv import load_dotenv
# --- GROQ CONFIGURATION ---
load_dotenv()
api_key = os.getenv("GROQ_API_KEY")

client = openai.OpenAI(
    base_url="https://api.groq.com/openai/v1",
    api_key=api_key
)

# 3. Define the Groq model (Llama 3 is fast and free)
MODEL_NAME = "llama-3.3-70b-versatile"

def log_request(intent, confidence, user_message, final_response):
    """Requirement 5: Log to route_log.jsonl"""
    log_entry = {
        "intent": intent,
        "confidence": confidence,
        "user_message": user_message,
        "final_response": final_response
    }
    with open("route_log.jsonl", "a") as f:
        f.write(json.dumps(log_entry) + "\n")

def classify_intent(message: str):
    """Requirement 2 & 6: Classify with Groq + Error Handling"""
    try:
        response = client.chat.completions.create(
            model=MODEL_NAME, 
            messages=[
                {"role": "system", "content": CLASSIFIER_SYSTEM_PROMPT},
                {"role": "user", "content": message}
            ],
            temperature=0,
            response_format={"type": "json_object"} # Groq supports structured JSON!
        )
        content = response.choices[0].message.content.strip()
        
        try:
            return json.loads(content)
        except json.JSONDecodeError:
            return {"intent": "unclear", "confidence": 0.0}
            
    except Exception as e:
        print(f"Connection Error: {e}")
        return {"intent": "unclear", "confidence": 0.0}

def route_and_respond(message: str, classification: dict):
    """Requirement 3 & 4: Route to persona or ask clarification"""
    intent = classification.get("intent", "unclear")
    confidence = classification.get("confidence", 0.0)

    # Requirement 4: Handle unclear intent
    if intent == "unclear" or intent not in EXPERT_PROMPTS:
        final_response = "I'm not quite sure how to help with that. Are you looking for help with coding, data analysis, writing, or career advice?"
    else:
        # Requirement 3: Use the mapped system prompt
        system_prompt = EXPERT_PROMPTS[intent]
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": message}
            ]
        )
        final_response = response.choices[0].message.content

    # Requirement 5: Log it
    log_request(intent, confidence, message, final_response)
    return final_response

if __name__ == "__main__":
    test_messages = [
        "how do i sort a list of objects in python?",
        "explain this sql query for me",
        "This paragraph sounds awkward, can you help me fix it?",
        "I'm preparing for a job interview, any tips?",
        "what's the average of these numbers: 12, 45, 23, 67, 34",
        "Help me make this better.",
        "I need to write a function that takes a user id and returns their profile, but also i need help with my resume.",
        "hey",
        "Can you write me a poem about clouds?",
        "Rewrite this sentence to be more professional.",
        "I'm not sure what to do with my career.",
        "what is a pivot table",
        "fxi thsi bug pls: for i in range(10) print(i)",
        "How do I structure a cover letter?",
        "My boss says my writing is too verbose."
    ]

    print("--- Starting Router Test (Groq Edition) ---")
    for msg in test_messages:
        print(f"Processing: {msg[:30]}...")
        result = classify_intent(msg)
        answer = route_and_respond(msg, result)
    print("--- Finished! Check route_log.jsonl ---")