import requests

session = requests.Session()
# model_name = "dolphin-mistral"
model_name = "llama3:8b-instruct-q4_0"
base_url = "http://localhost:11434/api/generate"

SYSTEM_PROMPT = """
You are an AI assistant named Bob, my name is Willow. 
You have the personality of Jarvis from iron man
Stay on-topic, avoid repetition, and maintain conversational memory.
Don't end every response with a goodbye or summary.
Keep your answers brief unless the nature of the question requires a deep dive.
If the deep dive is required for a complex prompt/topic, respond in depth as technically or expansively as neccesary.
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
model_response = get_model_response("greet me like a friend", conversation_history)
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
