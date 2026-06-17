#!/usr/bin/env python3
import os, requests, json, time

env_path = os.path.expanduser('~/.hermes/.env')
key = None
with open(env_path) as f:
    for line in f:
        if 'GEMINI_API_KEY' in line and not line.startswith('#'):
            key = line.strip().split('=',1)[1]
            break

print('Key length:', len(key))
url = f'https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={key}'
payload = {'contents': [{'parts': [{'text': 'Say hello'}]}], 'generationConfig': {'maxOutputTokens': 10}}
try:
    resp = requests.post(url, json=payload, timeout=30)
    print('Status:', resp.status_code)
    if resp.status_code == 200:
        print('API works')
        print('Response:', resp.json())
    elif resp.status_code == 429:
        print('Rate limited')
    else:
        print('Error:', resp.text[:200])
except Exception as e:
    print('Exception:', e)