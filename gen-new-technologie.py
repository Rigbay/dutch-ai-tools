#!/usr/bin/env python3
"""
Generate 3 new technology comparison articles for Dutch AI Tools.
Uses Gemini API to generate content.
"""
import os
import json
import re
import time
import requests
from pathlib import Path

def load_api_key():
    env_path = Path.home() / ".hermes/.env"
    if not env_path.exists():
        return None
    with open(env_path) as f:
        for line in f:
            if line.startswith("GEMINI_API_KEY=") and not line.startswith("#"):
                return line.strip().split("=", 1)[1]
            if line.startswith("GOOGLE_API_KEY=") and not line.startswith("#"):
                return line.strip().split("=", 1)[1]
    return None

GEMINI_API_KEY = load_api_key()
if not GEMINI_API_KEY:
    print("ERROR: No Gemini API key found")
    exit(1)

print(f"API key found (first 5 chars): {GEMINI_API_KEY[:5]}...")

ARTICLES_DIR = Path("/workspace/dutch-ai-tools/src/content/articles")

# Topics for "technologie" category
TOPICS = [
    {
        "title": "Beste AI tools voor slimme steden en IoT 2026",
        "slug": "ai-tools-slimme-steden-iot-2026",
        "description": "Vergelijk AI tools voor slimme steden, IoT-platforms en data-analyse in 2026. Nederlandse gemeenten en projectontwikkelaars.",
        "tools": [
            {"name": "CitiIQ", "desc": "AI-platform voor stedelijke data-analyse en voorspellingen"},
            {"name": "Siemens City Performance Tool", "desc": "Simulatie van stedelijke infrastructuren en duurzaamheid"},
            {"name": "IBM Watson IoT", "desc": "AI-analyse van IoT-data voor slimme stadsprojecten"},
            {"name": "Microsoft Azure Digital Twins", "desc": "Digitale tweelingplatform voor stedelijke planning"},
            {"name": "Google Environmental Insights Explorer", "desc": "AI voor klimaatimpact en energie-efficiëntie"}
        ]
    },
    {
        "title": "Beste AI tools voor robotica en autonome systemen 2026",
        "slug": "ai-tools-robotica-autonoom-2026",
        "description": "Vergelijk AI tools voor robotica, autonome voertuigen en industriële automatisering in 2026. Nederlandse bedrijven en onderzoek.",
        "tools": [
            {"name": "NVIDIA Isaac", "desc": "AI-platform voor robotica-ontwikkeling en simulatie"},
            {"name": "ROS 2 (Robot Operating System)", "desc": "Open-source framework voor robotsoftware"},
            {"name": "AWS RoboMaker", "desc": "Cloud-service voor robotica-simulatie en -ontwikkeling"},
            {"name": "Microsoft Autonomous Systems", "desc": "AI-tools voor autonome systemen en edge computing"},
            {"name": "Google Cloud Robotics", "desc": "AI-services voor robotlearning en cloud-robotics"}
        ]
    },
    {
        "title": "Beste AI tools voor cybersecurity en threat detection 2026",
        "slug": "ai-tools-cybersecurity-threat-detection-2026",
        "description": "Vergelijk AI tools voor cybersecurity, bedreigingsdetectie en netwerkbeveiliging in 2026. Nederlandse bedrijven en IT-beveiliging.",
        "tools": [
            {"name": "Darktrace", "desc": "AI-gestuurde threat detection en autonome response"},
            {"name": "CrowdStrike Falcon", "desc": "Endpoint protection met machine learning voor malware detectie"},
            {"name": "Vectra AI", "desc": "Network detection and response (NDR) met AI-analyse"},
            {"name": "SentinelOne", "desc": "AI-powered endpoint security en behavioral monitoring"},
            {"name": "Microsoft Defender for Endpoint", "desc": "AI-gestuurde endpoint protection en threat intelligence"}
        ]
    }
]

def generate_article(topic):
    """Generate article content using Gemini API."""
    tools_text = "\n".join([f"- {t['name']}: {t['desc']}" for t in topic["tools"]])
    
    prompt = f"""Schrijf een Nederlands artikel voor een AI tools vergelijkingswebsite.

Titel: {topic['title']}
Slug: {topic['slug']}
Beschrijving: {topic['description']}
Categorie: technologie

Deze tools moeten besproken worden:
{tools_text}

Schrijf een compleet artikel in Markdown formaat met de volgende structuur:
1. Frontmatter YAML (tussen ---) met: title, slug, description, category: technologie, rating: 4.2-4.8, priceRange: "€0-500 per maand", pros (3-5 punten), cons (3-5 punten), affiliateLinks (gebruik dezelfde affiliate links als andere artikelen op de site: beehiiv, taskade, writesonic, rytr, synthesia, make, frase), date: 2026-06-19, modelYear: 2026, featuredTool: "{topic['tools'][0]['name']}", readingTime: "8 min", tools (lijst van 5 tools met name, verdict, priceRange, bestFor, rating: 4.0-4.9, affiliateLink), faq (3-5 vragen met antwoorden), related (3-5 gerelateerde artikelen slugs)
2. Na het frontmatter: Inleiding, Vergelijkingstabel, Gedetailleerde reviews van elke tool, FAQ, Conclusie
3. Schrijf in professioneel maar toegankelijk Nederlands voor Nederlandse lezers
4. Gebruik interne links naar andere artikelen waar relevant
5. Geef praktisch advies voor Nederlandse gebruikers
6. Vermeld zowel voordelen als beperkingen van elke tool

Begin direct met de frontmatter, gevolgd door de inhoud."""
    
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={GEMINI_API_KEY}"
    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {
            "maxOutputTokens": 4000,
            "temperature": 0.7
        }
    }
    
    try:
        response = requests.post(url, json=payload, timeout=120)
        if response.status_code == 200:
            data = response.json()
            text = data["candidates"][0]["content"]["parts"][0]["text"]
            return text
        else:
            print(f"API error: {response.status_code} - {response.text[:200]}")
            return None
    except Exception as e:
        print(f"Request error: {e}")
        return None

def main():
    print(f"Generating {len(TOPICS)} new technology articles...")
    
    generated = []
    for i, topic in enumerate(TOPICS):
        print(f"\n[{i+1}/{len(TOPICS)}] Generating: {topic['slug']}")
        
        # Check if file already exists
        file_path = ARTICLES_DIR / f"{topic['slug']}.md"
        if file_path.exists():
            print(f"  Skipping - file already exists")
            continue
        
        content = generate_article(topic)
        if not content:
            print(f"  Failed to generate content")
            continue
        
        # Ensure frontmatter starts properly
        if not content.strip().startswith('---'):
            content = '---\n' + content
        
        # Save file
        file_path.write_text(content, encoding='utf-8')
        print(f"  Saved to {file_path}")
        generated.append(topic['slug'])
        
        # Rate limiting
        if i < len(TOPICS) - 1:
            time.sleep(2)
    
    print(f"\nGenerated {len(generated)} new articles:")
    for slug in generated:
        print(f"  - {slug}")
    
    if generated:
        # Build site to check for errors
        print("\nBuilding site to check for errors...")
        os.chdir("/workspace/dutch-ai-tools")
        result = os.system("npm run build 2>&1 | tail -30")
        if result != 0:
            print("Build had errors")
        else:
            print("Build successful")
    else:
        print("No new articles generated")

if __name__ == "__main__":
    main()