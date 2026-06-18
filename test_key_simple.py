import os
import requests
import time

def load_api_key():
    env_path = os.path.expanduser("~/.hermes/.env")
    if not os.path.exists(env_path):
        return None
    with open(env_path) as f:
        for line in f:
            if line.startswith("GEMINI_API_KEY=") and not line.startswith("#"):
                return line.strip().split("=", 1)[1]
            if line.startswith("GOOGLE_API_KEY=") and not line.startswith("#"):
                return line.strip().split("=", 1)[1]
    return None

key = load_api_key()
if key:
    print(f"Key found (first 5 chars): {key[:5]}...")
    # Test small call
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={key}"
    payload = {
        "contents": [{"parts": [{"text": "Say hello"}]}],
        "generationConfig": {"maxOutputTokens": десять}
    }
    try:
        resp = requests.post(url, json=payload, timeout=30)
        print(f"Status: {resp.status_code}")
        if resp.status_code == 200:
            print("API works")
        else:
            print(f"Error: {resp.text[:200]}")
    except Exception as e:
        print(f"Exception: {e}")
else:
    print("No key found")