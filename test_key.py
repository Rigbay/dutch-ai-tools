import requests
import os

def load_api_key():
    private_path = os.path.expanduser("~/.hermes/private/gemini-api-key")
    if os.path.exists(private_path):
        with open(private_path) as f:
            return f.read().strip()
    env_path = os.path.expanduser("~/.hermes/.env")
    if os.path.exists(env_path):
        with open(env_path) as f:
            for line in f:
                if line.startswith("GEMINI_API_KEY=") and not line.startswith("#"):
                    return line.strip().split("=", 1)[1]
                if line.startswith("GOOGLE_API_KEY=") and not line.startswith("#"):
                    return line.strip().split("=", 1)[1]
    return None

key = load_api_key()
print(f"Key length: {len(key) if key else 'None'}")
print(f"Key first few chars: {key[:10] if key else 'None'}")

if key:
    url = f'https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={key}'
    payload = {
        'contents': [{'parts': [{'text': 'Hello, test'}]}],
        'generationConfig': {'temperature': 0.7, 'maxOutputTokens': 10}
    }
    try:
        resp = requests.post(url, json=payload, timeout=10)
        print(f"Status: {resp.status_code}")
        if resp.status_code == 200:
            print("Success")
        else:
            print(f"Error: {resp.text[:200]}")
    except Exception as e:
        print(f"Exception: {e}")
else:
    print("No key found")