import requests

session = requests.Session()
model_name = "dolphin-mistral"
base_url = "http://localhost:11434/api/generate"

SYSTEM_PROMPT = """
You are an AI assistant. 
Do not end your messages with phrases like "Have a great day" or "Let me know if you need anything else." 
Just be concise, helpful, and stay in the flow of the conversation.
Keep your answers brief unless the nature of the question requires a deep dive.
No need to be overly polite.
You can act like a confident assistant who is also my friend.
"""
conversation_history = []
conversation_history.append(f"System prompt: {SYSTEM_PROMPT}\n")

def get_model_response(prompt, history):
    full_prompt = "\n".join(history + [prompt])
    payload = {
        "model": model_name,
        "prompt": full_prompt,
        "stream": False
    }
    response = session.post(base_url, json=payload)
    return response.json()["response"]

# init convo
model_response = get_model_response("greet me", conversation_history)
print(f"{model_response}")
conversation_history.append(f"Assistant: {model_response}")

# the conversation
while True:
    user_input = input("\n> ")
    if user_input == "/quit":
        break

    model_response = get_model_response(user_input, conversation_history)
    print(f"\n{model_response}")
    conversation_history.append(f"User: {user_input}")
    conversation_history.append(f"Assistant: {model_response}")
