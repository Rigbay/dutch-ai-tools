#!/usr/bin/env python3
"""Test Ollama generation for Dutch AI Tools."""

import os, json, subprocess, sys

model = "llama3.2:latest"
prompt = """Je bent een Nederlandse tech-journalist gespecialiseerd in slimme technologie voor thuis. Schrijf een korte paragraaf (max 100 woorden) over waarom slimme thermostaten energie kunnen besparen.

Antwoord in Nederlands."""

cmd = ["ollama", "run", model, prompt]
try:
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
    if result.returncode == 0:
        print("Ollama response:")
        print(result.stdout[:500])
        sys.exit(0)
    else:
        print("Ollama error:", result.stderr)
        sys.exit(1)
except FileNotFoundError:
    print("ollama command not found")
    sys.exit(1)