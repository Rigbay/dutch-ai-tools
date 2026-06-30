#!/usr/bin/env python3
"""
Fix incomplete articles by generating missing content with a simpler prompt.
"""

import os
import requests
from pathlib import Path

def load_api_key():
    env_path = os.path.expanduser("~/.hermes/.env")
    if not os.path.exists(env_path):
        return None
    with open(env_path) as f:
        for line in f:
            line = line.strip()
            if line.startswith("GEMINI_API_KEY=") and not line.startswith("#"):
                return line.split("=", 1)[1]
            if line.startswith("GOOGLE_API_KEY=") and not line.startswith("#"):
                return line.split("=", 1)[1]
    return None

GEMINI_API_KEY = load_api_key()
if not GEMINI_API_KEY:
    print("Error: No Gemini API key found")
    exit(1)

GEMINI_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={GEMINI_API_KEY}"

def generate_article_content(title, description, providers):
    """Generate article content for a given topic."""
    prompt = f"""Schrijf een Nederlands artikel van ongeveer 800-1000 woorden over: "{title}"

Beschrijving: {description}

Tools om te vergelijken: {providers}

Schrijf een complete artikel met:
1. Inleiding waarom dit relevant is voor Nederlandse consumenten
2. Een vergelijkingstabel van de tools met kolommen: Tool, Beste voor (bijv. Beginner, Gevorderde, Expert), Prijsrange in euro's, Rating (bijv. 4.2/5), Korte beschrijving
3. Voor elke tool een alinea met voordelen en aandachtspunten voor Nederlandse gebruikers
4. Praktische tips voor het kiezen van de juiste tool in Nederland
5. Conclusie met aanbevelingen voor verschillende gebruikersgroepen
6. FAQ met 3 vragen over AVG-compliance, Nederlandstalige support en integratie met Nederlandse systemen

Schrijf in natuurlijk Nederlands, informeel maar professioneel.
Focus op praktische toepassingen voor Nederlandse gebruikers.
Noem waar relevant AVG-compliance en Nederlandstalige ondersteuning.
Gebruik euro's voor prijzen en geef ratings op een schaal van 1-5.

Artikel moet alleen markdown zijn, geen YAML frontmatter."""

    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {
            "temperature": 0.7,
            "maxOutputTokens": 1500,
        }
    }
    
    headers = {"Content-Type": "application/json"}
    
    try:
        response = requests.post(GEMINI_URL, json=payload, headers=headers, timeout=60)
        if response.status_code == 200:
            data = response.json()
            text = data.get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", "")
            return text.strip()
        else:
            print(f"API error: {response.status_code} - {response.text[:200]}")
            return None
    except Exception as e:
        print(f"Request error: {e}")
        return None

def main():
    articles_to_fix = [
        {
            "path": "src/content/articles/beste-ai-tools-persoonlijk-shoppen-mode-stijladvies-2026.md",
            "title": "Beste AI tools voor persoonlijk shoppen, mode en stijladvies 2026",
            "description": "Vergelijk AI tools die persoonlijke kledingstijl analyseren, outfit-suggesties geven, en gepersonaliseerde shopping recommendations bieden voor de Nederlandse markt.",
            "providers": "Stitch Fix AI, Amazon Personalize, Zalando Style Guide, Pinterest Style AI, Whering, Dressipi"
        },
        {
            "path": "src/content/articles/beste-ai-tools-persoonlijke-voeding-maaltijdplanning-2026.md",
            "title": "Beste AI tools voor persoonlijke voeding en maaltijdplanning 2026",
            "description": "Vergelijk AI tools voor gepersonaliseerde voedingsadviezen, dieetplanning, boodschappenlijstjes en receptsuggesties op basis van gezondheidsdoelen en voorkeuren.",
            "providers": "Eat This Much, Yazio, Lifesum AI, Mealime, PlateJoy, Foodvisor"
        },
        {
            "path": "src/content/articles/beste-ai-tools-persoonlijke-evenementen-planning-2026.md",
            "title": "Beste AI tools voor persoonlijke evenementen en planning 2026",
            "description": "Vergelijk AI tools voor het plannen van verjaardagen, feesten, bruiloften en andere persoonlijke evenementen, inclusief budgetbeheer, gastenlijsten en tijdlijnen.",
            "providers": "Zola Wedding Planner, Eventbrite AI, Doodle AI, Calendly AI, Canva Event Templates, Pinterest Event Planning"
        }
    ]
    
    for article in articles_to_fix:
        path = Path(article["path"])
        if not path.exists():
            print(f"File not found: {path}")
            continue
            
        print(f"\nFixing {path.name}...")
        
        # Read existing frontmatter
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
        
        # Find where content starts (after YAML frontmatter)
        if "---\n\n" in content:
            frontmatter_end = content.find("---\n\n") + 4  # Keep the second ---
            frontmatter = content[:frontmatter_end]
            existing_body = content[frontmatter_end:]
        else:
            print(f"  No YAML frontmatter delimiter found in {path.name}")
            continue
            
        # If body is already substantial (more than 1000 chars), skip
        if len(existing_body.strip()) > 1000:
            print(f"  Article already has content ({len(existing_body.strip())} chars), skipping")
            continue
            
        print(f"  Current body length: {len(existing_body.strip())} chars")
        print(f"  Generating new content...")
        
        new_body = generate_article_content(
            article["title"],
            article["description"],
            article["providers"]
        )
        
        if new_body:
            # Write back with new content
            new_content = frontmatter + "\n" + new_body
            with open(path, "w", encoding="utf-8") as f:
                f.write(new_content)
            print(f"  ✅ Fixed {path.name} with {len(new_body)} chars")
        else:
            print(f"  ❌ Failed to generate content for {path.name}")
            
        # Rate limiting
        import time
        time.sleep(2)

if __name__ == "__main__":
    main()