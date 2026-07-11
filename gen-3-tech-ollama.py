#!/usr/bin/env python3
"""
Generate 3 new technology comparison articles for Dutch AI Tools using Ollama.
"""
import os
import json
import re
import time
import requests
from pathlib import Path

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "gemma4:latest"
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

def generate_with_ollama(prompt):
    """Generate content using Ollama."""
    payload = {
        "model": MODEL,
        "prompt": prompt,
        "stream": False,
        "options": {
            "temperature": 0.7,
            "num_predict": 4000
        }
    }
    
    try:
        response = requests.post(OLLAMA_URL, json=payload, timeout=300)
        if response.status_code == 200:
            data = response.json()
            text = data.get("response", "")
            return text
        else:
            print(f"Ollama error: {response.status_code} - {response.text[:200]}")
            return None
    except Exception as e:
        print(f"Request error: {e}")
        return None

def generate_article(topic):
    """Generate article content."""
    tools_text = "\n".join([f"- {t['name']}: {t['desc']}" for t in topic["tools"]])
    
    # Get existing article slugs for related links
    existing_slugs = [f.stem for f in ARTICLES_DIR.glob("*.md") if f.stem not in [t["slug"] for t in TOPICS]]
    related = existing_slugs[:3] if existing_slugs else ["ai-trends-2026-nederland", "aws-vs-azure-vs-google-cloud-2026", "beste-ai-3d-modellering-tools-2026"]
    
    prompt = f"""Schrijf een Nederlands artikel voor een AI tools vergelijkingswebsite.

TITEL: {topic['title']}
SLUG: {topic['slug']}
BESCHRIJVING: {topic['description']}
CATEGORIE: technologie

DEZE TOOLS MOETEN BESPROKEN WORDEN:
{tools_text}

SCHRIJF EEN COMPLEET ARTIKEL IN MARKDOWN FORMAAT MET DE VOLGENDE STRUCTUUR:

1. YAML FRONTMATTER (tussen drie streepjes ---) met:
   title: '{topic['title']}'
   slug: {topic['slug']}
   description: '{topic['description']}'
   category: technologie
   rating: 4.5
   priceRange: "€0-500 per maand"
   pros:
     - "Pro punt 1"
     - "Pro punt 2"
     - "Pro punt 3"
   cons:
     - "Nadeel 1"
     - "Nadeel 2"
     - "Nadeel 3"
   affiliateLinks:
     - https://www.beehiiv.com/
     - https://taskade.com/?via=55nfr2
     - https://writesonic.com/?via=aitoolsnl
     - https://rytr.me?via=hermes-affiliates
     - https://www.synthesia.io?via=hermes
     - https://www.make.com/en/register?pc=hermesai
     - https://www.frase.io/?via=hermes10
   date: 2026-06-19
   modelYear: 2026
   featuredTool: "{topic['tools'][0]['name']}"
   readingTime: "8 min"
   tools:
     - name: "{topic['tools'][0]['name']}"
       verdict: "Korte beschrijving van waarom deze tool goed is"
       priceRange: "€0-200/mnd"
       bestFor: "Nederlandse gemeenten"
       rating: 4.7
       affiliateLink: "https://voorbeeld.com"
     - name: "{topic['tools'][1]['name']}"
       verdict: "Korte beschrijving"
       priceRange: "€50-300/mnd"
       bestFor: "Projectontwikkelaars"
       rating: 4.5
       affiliateLink: "https://voorbeeld.com"
     - ... en zo verder voor alle 5 tools ...
   related:
     - {related[0]}
     - {related[1]}
     - {related[2]}
   faq:
     - q: "Veelgestelde vraag 1"
       a: "Antwoord op vraag 1"
     - q: "Veelgestelde vraag 2"
       a: "Antwoord op vraag 2"
     - q: "Veelgestelde vraag 3"
       a: "Antwoord op vraag 3"

2. NA HET FRONTMATTER: artikel inhoud met:
   - Inleiding (waarom dit onderwerp belangrijk is voor Nederlandse professionals)
   - Vergelijkingstabel (optioneel)
   - Gedetailleerde reviews van elke tool
   - Conclusie (welke tool wanneer te gebruiken)
   - Praktische tips voor implementatie in Nederland

3. SCHRIJFSTIJL:
   - Professioneel maar toegankelijk Nederlands
   - Gericht op Nederlandse lezers
   - Gebruik praktische voorbeelden uit de Nederlandse context
   - Noem zowel voordelen als beperkingen van elke tool
   - Sluit af met een duidelijke aanbeveling per gebruiksscenario

Begin direct met de frontmatter, gevolgd door de inhoud."""
    
    return generate_with_ollama(prompt)

def main():
    print(f"Generating {len(TOPICS)} new technology articles using Ollama...")
    
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
            time.sleep(3)
    
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
        
        # Stage and commit
        print("\nStaging files...")
        os.system(f"git add src/content/articles/{generated[0]}.md")
        if len(generated) > 1:
            os.system(f"git add src/content/articles/{generated[1]}.md")
        if len(generated) > 2:
            os.system(f"git add src/content/articles/{generated[2]}.md")
        
        os.system(f"git commit -m 'cron: add {len(generated)} new technology articles via Ollama'")
        print("Committed")
    else:
        print("No new articles generated")

if __name__ == "__main__":
    main()