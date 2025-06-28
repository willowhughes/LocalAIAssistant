import requests
import atexit
import subprocess
import time
import json
import os
import signal
from ConversationState import ConversationState

session = requests.Session()
# other model names: dolphin-mistral, llama3:8b-instruct-q4_0"

# Load configuration from JSON file
with open("config.json", "r") as f:
    config = json.load(f)


MODEL_NAME = config["MODEL_NAME"]
GEN_URL = config["GEN_URL"]
SYSTEM_CONFIG = config["SYSTEM_CONFIG"]

def is_ollama_running():
    try:
        r = requests.get("http://localhost:11434")
        return r.status_code == 200
    except Exception:
        return False

def start_ollama():
    global ollama_process
    if not is_ollama_running():
        print("Starting Ollama...")
        ollama_process = subprocess.Popen(
            ["ollama", "serve"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            creationflags=subprocess.CREATE_NEW_PROCESS_GROUP  # windows-specific
        )
        # give it a few seconds to spin up
        for _ in range(10):
            if is_ollama_running():
                break
            time.sleep(1)
    else:
        print("Ollama is already running.")

def stop_ollama():
    global ollama_process
    if ollama_process:
        print("Shutting down Ollama...")
        ollama_process.send_signal(signal.CTRL_BREAK_EVENT)
        ollama_process.wait(timeout=10)

# stop Ollama at script exit
atexit.register(stop_ollama)

def get_model_response(prompt, history):
    full_prompt = "\n".join(history + [prompt])
    payload = {
        "model": MODEL_NAME,
        "prompt": full_prompt,
        "stream": False
    }
    response = session.post(GEN_URL, json=payload)
    return response.json()["response"]


if __name__ == "__main__":
    start_ollama()

    convo = ConversationState(SYSTEM_CONFIG)

    # init convo
    model_response = get_model_response("greet me like a friend", convo.get_history())
    print(f"{model_response}")
    convo.append_response(model_response)

    # the conversation
    while True:
        user_prompt = input("\n> ")
        if user_prompt.lower() in ["/exit", "bye"]:
            break
        elif user_prompt.lower() in ["/debugconvo"]:
            print(convo.get_history())
            continue

        reply = get_model_response(user_prompt, convo.get_history())
        print(f"\n{reply}")
        convo.append_prompt(user_prompt)
        convo.append_response(reply)