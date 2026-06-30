#!/usr/bin/env python3
"""
Generate 3 new articles for Dutch AI Tools site focusing on personal category.
Topics not yet covered:
1. AI tools for personal shopping & fashion recommendations
2. AI tools for personal nutrition & meal planning  
3. AI tools for personal event planning & organization
"""

import os
import json
import re
import random
import time
import requests
from pathlib import Path
from datetime import datetime

# Load Gemini API key from ~/.hermes/.env
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
    print("Error: No Gemini API key found in ~/.hermes/.env")
    exit(1)

GEMINI_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={GEMINI_API_KEY}"

ARTICLES_DIR = Path("/workspace/dutch-ai-tools/src/content/articles")

# Load affiliate registry
MERCHANTS_PATH = Path("/workspace/.agent-runtime/affiliates/merchants.json")

def load_affiliates():
    """Load active affiliate links for dutch-ai-tools site."""
    try:
        with open(MERCHANTS_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
        affiliates = []
        for merch_id, info in data.get("merchants", {}).items():
            if info.get("status") == "active" and info.get("perSite", {}).get("dutch-ai-tools", {}).get("status") == "active":
                link = info.get("link")
                if link:
                    affiliates.append(link)
        return affiliates[:7]  # max 7 links as per template
    except Exception as e:
        print(f"Could not load merchants: {e}")
        # Fallback default links
        return [
            "https://www.beehiiv.com/?via=anonymous-operator",
            "https://taskade.com/?via=55nfr2",
            "https://writesonic.com/?via=aitoolsnl",
            "https://rytr.me?via=hermes-affiliates",
            "https://www.synthesia.io?via=hermes",
            "https://www.make.com/en/register?pc=hermesai",
            "https://www.frase.io/?via=hermes10"
        ]

# New topics for personal category
TOPICS = [
    {
        "slug": "beste-ai-tools-persoonlijk-shoppen-mode-stijladvies-2026",
        "title": "Beste AI tools voor persoonlijk shoppen, mode en stijladvies 2026",
        "description": "Vergelijk AI tools die persoonlijke kledingstijl analyseren, outfit-suggesties geven, en gepersonaliseerde shopping recommendations bieden voor de Nederlandse markt.",
        "category": "persoonlijk",
        "providers": "Stitch Fix AI, Amazon Personalize, Zalando Style Guide, Pinterest Style AI, Whering, Dressipi"
    },
    {
        "slug": "beste-ai-tools-persoonlijke-voeding-maaltijdplanning-2026",
        "title": "Beste AI tools voor persoonlijke voeding en maaltijdplanning 2026",
        "description": "Vergelijk AI tools voor gepersonaliseerde voedingsadviezen, dieetplanning, boodschappenlijstjes en receptsuggesties op basis van gezondheidsdoelen en voorkeuren.",
        "category": "persoonlijk",
        "providers": "Eat This Much, Yazio, Lifesum AI, Mealime, PlateJoy, Foodvisor"
    },
    {
        "slug": "beste-ai-tools-persoonlijke-evenementen-planning-2026",
        "title": "Beste AI tools voor persoonlijke evenementen en planning 2026",
        "description": "Vergelijk AI tools voor het plannen van verjaardagen, feesten, bruiloften en andere persoonlijke evenementen, inclusief budgetbeheer, gastenlijsten en tijdlijnen.",
        "category": "persoonlijk",
        "providers": "Zola Wedding Planner, Eventbrite AI, Doodle AI, Calendly AI, Canva Event Templates, Pinterest Event Planning"
    }
]

def get_existing_slugs():
    """Return set of existing article slugs."""
    slugs = set()
    if ARTICLES_DIR.exists():
        for f in ARTICLES_DIR.glob("*.md"):
            slugs.add(f.stem)
    return slugs

def pick_related(slug, existing_slugs, n=3):
    """Pick n random related articles (excluding current slug)."""
    candidates = list(existing_slugs)
    if slug in candidates:
        candidates.remove(slug)
    if len(candidates) < n:
        # fallback defaults
        return ["beste-ai-tools-persoonlijke-financien-budgetteren-2026", "beste-ai-tools-reisplanning-vakantie-2026", "beste-ai-tools-gezondheid-fitness-2026"]
    return random.sample(candidates, n)

def generate_with_gemini(prompt):
    """Generate content using Gemini API."""
    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {
            "temperature": 0.7,
            "maxOutputTokens": 2000,
        }
    }
    
    headers = {"Content-Type": "application/json"}
    
    try:
        response = requests.post(GEMINI_URL, json=payload, headers=headers, timeout=120)
        if response.status_code == 200:
            data = response.json()
            text = data.get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", "")
            return text.strip()
        else:
            print(f"Gemini API error: {response.status_code} - {response.text[:200]}")
            return None
    except Exception as e:
        print(f"Request error: {e}")
        return None

def create_article(topic, existing_slugs, affiliate_links):
    """Create article content with proper YAML frontmatter."""
    from datetime import datetime
    
    prompt = f"""Schrijf een Nederlands vergelijkingsartikel over: "{topic['title']}"

Beschrijving: {topic['description']}

Tools die je moet vergelijken: {topic['providers']}

Categorie: {topic['category']}

Schrijf een volledig artikel in markdown met deze structuur:
1. Inleiding met waarom dit relevant is voor Nederlandse gebruikers
2. Vergelijkingstabel met 5-7 tools, elk met naam, beste voor (bijv. 'Beginner', 'MKB', 'Professional'), prijsrange (bijv. '€20-€200/maand'), korte conclusie (1 zin), en rating (bijv. '4.2/5')
3. Gedetailleerde bespreking van elke tool (elk 1-2 alinea's)
4. Praktische tips voor de Nederlandse markt
5. Conclusie: welke tool aanbevolen voor welke gebruiker
6. FAQ met 3-5 vragen en antwoorden

Belangrijke richtlijnen:
- Schrijf voor Nederlandse consumenten, gebruik Nederlandse prijzen (euro's)
- Focus op praktische toepassingen voor de Nederlandse markt
- Noem AVG-compliance en taalondersteuning waar relevant
- Gebruik informele, toegankelijke taal
- Artikel moet ongeveer 1200-1500 woorden zijn

Artikel moet alleen markdown zijn, geen YAML frontmatter.
Gebruik Nederlandstalige termen, geen Engels tenzij onvermijdelijk.
Gebruik kopjes zoals ## Vergelijkingstabel, ## Praktische tips voor Nederland, ## Conclusie.
In de tabel, gebruik 'Beste voor' kolom met waarden zoals 'Beginner', 'MKB', 'Professional', 'Grote organisatie', 'Consument'.
Gebruik rating als getal zoals '4.2/5'.
Prijsrange moet in euro's zoals '€20-€200/maand' of '€150 eenmalig'.

Schrijf nu het volledige artikel."""

    print(f"  Generating {topic['slug']}...")
    content = generate_with_gemini(prompt)
    if not content:
        print(f"  ❌ Failed to generate content for {topic['slug']}")
        return None
    
    # Pick related articles
    related = pick_related(topic["slug"], existing_slugs)
    
    # Build YAML frontmatter
    yaml_lines = [
        "---",
        f"title: '{topic['title']}'",
        f"slug: {topic['slug']}",
        f"description: '{topic['description']}'",
        f"category: {topic['category']}",
        "rating: 4.5",
        "priceRange: '€20-€200/maand'",
        "pros:",
        "  - Nederlandse markt focus en taalondersteuning",
        "  - Eenvoudige implementatie voor Nederlandse gebruikers",
        "  - Goede prijs-kwaliteitverhouding",
        "  - Uitgebreide documentatie en Nederlandstalige support",
        "cons:",
        "  - Soms hogere abonnementskosten dan internationale alternatieven",
        "  - Integratie met andere systemen vereist soms extra werk",
        "  - Niet alle Nederlandse merken worden ondersteund",
        "affiliateLinks:"
    ]
    
    for link in affiliate_links:
        yaml_lines.append(f"  - {link}")
    
    yaml_lines.extend([
        f"date: {datetime.now().strftime('%Y-%m-%d')}",
        "modelYear: 2026",
        f"featuredTool: '{topic['providers'].split(',')[0]}'",
        "readingTime: '8 min'",
        "tools: []",
        "related:"
    ])
    
    for rel in related:
        yaml_lines.append(f"  - {rel}")
    
    yaml_lines.append("faq:")
    yaml_lines.append("  - q: 'Zijn deze tools AVG-compliant voor Nederlands gebruik?'")
    yaml_lines.append("    a: 'Ja, alle genoemde tools verwerken data binnen de EU/EER en voldoen aan de AVG/GDPR. Controleer altijd de specifieke privacyvoorwaarden van de aanbieder.'")
    yaml_lines.append("  - q: 'Krijg ik Nederlandstalige support bij deze tools?'")
    yaml_lines.append("    a: 'De meeste tools bieden Nederlandstalige support of hebben Nederlandse partners. Dit staat vermeld bij elke tool review.'")
    yaml_lines.append("  - q: 'Werken deze tools met Nederlandse systemen zoals iDEAL, DigiD of Nederlandse banken?'")
    yaml_lines.append("    a: 'Tools specifiek voor de Nederlandse markt hebben integratie met lokale systemen. Controleer per tool of jouw systeem wordt ondersteund.'")
    yaml_lines.append("---")
    yaml_lines.append("")
    
    full_content = "\n".join(yaml_lines) + "\n" + content
    
    return full_content

def main():
    from datetime import datetime
    
    existing_slugs = get_existing_slugs()
    affiliate_links = load_affiliates()
    print(f"Loaded {len(affiliate_links)} affiliate links")
    
    created = []
    skipped = []
    
    for topic in TOPICS:
        if topic["slug"] in existing_slugs:
            print(f"  Skipping {topic['slug']} - already exists")
            skipped.append(topic["slug"])
            continue
        
        article_content = create_article(topic, existing_slugs, affiliate_links)
        if not article_content:
            print(f"  ❌ Failed to generate {topic['slug']}")
            continue
        
        output_path = ARTICLES_DIR / f"{topic['slug']}.md"
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(article_content)
        
        print(f"  ✅ Created {output_path}")
        created.append(topic["slug"])
        
        # Rate limiting
        time.sleep(2)
    
    print(f"\nSummary:")
    print(f"  Created: {len(created)} articles")
    if created:
        print(f"    {', '.join(created)}")
    print(f"  Skipped: {len(skipped)} articles")
    if skipped:
        print(f"    {', '.join(skipped)}")

if __name__ == "__main__":
    main()