#!/usr/bin/env python3
"""Generate 3 new 'huis-tuin' articles using Ollama."""

import os, json, subprocess, time, random, re
from datetime import datetime

ARTICLES_DIR = "/workspace/dutch-ai-tools/src/content/articles"

# Get existing slugs
existing_slugs = set()
if os.path.exists(ARTICLES_DIR):
    for f in os.listdir(ARTICLES_DIR):
        if f.endswith(".md"):
            existing_slugs.add(f.replace(".md", ""))

# 3 new home/garden topics
TOPICS = [
    {
        "slug": "slimme-verlichting-hue-vs-ikea-vs-lifx-2026",
        "topic": "Beste slimme verlichting 2026: Philips Hue vs IKEA Tradfri vs LIFX",
        "category": "huis-tuin",
        "audience": "Nederlandse huishoudens die slimme verlichting willen installeren",
        "providers": "Philips Hue, IKEA Tradfri, LIFX, TP-Link Kasa, Nanoleaf, Yeelight"
    },
    {
        "slug": "slimme-thermostaat-nest-vs-tado-vs-honeywell-2026",
        "topic": "Beste slimme thermostaten 2026: Nest vs Tado vs Honeywell voor Nederlandse huizen",
        "category": "huis-tuin",
        "audience": "Nederlandse huiseigenaren die energie willen besparen met slimme thermostaten",
        "providers": "Google Nest, Tado, Honeywell Home, Netatmo, Bosch, Remeha"
    },
    {
        "slug": "robotstofzuigers-vergelijken-2026-roomba-vs-roborock-vs-dreame",
        "topic": "Robotstofzuigers vergelijken 2026: iRobot Roomba vs Roborock vs Dreame voor Nederlandse huizen",
        "category": "huis-tuin",
        "audience": "Nederlandse huishoudens die tijd willen besparen met robotstofzuigers",
        "providers": "iRobot Roomba, Roborock, Dreame, Ecovacs Deebot, Eufy, Samsung JetBot"
    }
]

# Filter out existing slugs
TOPICS = [t for t in TOPICS if t["slug"] not in existing_slugs]
if not TOPICS:
    print("All huis-tuin topics already exist.")
    exit(0)

def pick_related(slug, n=3):
    """Pick n random related articles from same category."""
    category_slugs = []
    for f in os.listdir(ARTICLES_DIR):
        if not f.endswith(".md"):
            continue
        path = os.path.join(ARTICLES_DIR, f)
        with open(path, 'r', encoding='utf-8') as fp:
            content = fp.read(2000)
            if "category: huis-tuin" in content and f.replace(".md", "") != slug:
                category_slugs.append(f.replace(".md", ""))
    return random.sample(category_slugs, min(n, len(category_slugs)))

def call_ollama(prompt):
    """Call Ollama API."""
    payload = {
        "model": "llama3.2:latest",
        "prompt": prompt,
        "stream": False,
        "options": {"temperature": 0.7}
    }
    try:
        import requests
        response = requests.post("http://localhost:11434/api/generate",
                                 json=payload, timeout=120)
        if response.status_code == 200:
            return response.json()["response"]
    except Exception as e:
        print(f"Ollama API error: {e}")
    # Fallback: use subprocess
    try:
        cmd = ["ollama", "run", "llama3.2:latest", prompt]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        if result.returncode == 0:
            return result.stdout.strip()
    except Exception as e:
        print(f"Ollama subprocess error: {e}")
    return None

def parse_response(raw):
    """Parse response with simple extraction."""
    # Find JSON-like block
    import json
    lines = raw.strip().split('\n')
    # Look for lines containing key-value pairs
    data = {
        "title": "",
        "description": "",
        "tools": [],
        "affiliateLinks": [],
        "pros": [],
        "cons": [],
        "rating": 4.3,
        "priceRange": "€0-100 per maand",
        "featuredTool": "",
        "readingTime": "8 min",
        "faq": [],
        "body_markdown": raw  # fallback
    }
    
    # Extract title
    for line in lines:
        if line.lower().startswith("title:"):
            data["title"] = line.split(":", 1)[1].strip().strip("'\"")
        elif line.lower().startswith("description:"):
            data["description"] = line.split(":", 1)[1].strip().strip("'\"")
    
    # If no structured data, guess
    if not data["title"]:
        # Extract first line as title
        for line in lines:
            if line.strip() and not line.strip().startswith("#"):
                data["title"] = line.strip()
                break
    
    return data

def build_article(data, slug, category, related_slugs):
    """Build markdown article."""
    today = datetime.now().strftime("%Y-%m-%d")
    lines = ["---"]
    lines.append(f"title: '{data.get('title', slug.replace('-', ' ').title())}'")
    lines.append(f"slug: {slug}")
    
    desc = data.get("description", f"Vergelijk de beste opties voor {slug.replace('-', ' ')} in 2026.")
    if len(desc) > 80:
        lines.append(f"description: >-\n  {desc}")
    else:
        lines.append(f"description: {desc}")
    
    lines.append(f"category: {category}")
    lines.append(f"rating: {data.get('rating', 4.3)}")
    lines.append(f"priceRange: {data.get('priceRange', '€0-100 per maand')}")
    
    pros = data.get("pros", ["Uitgebreide 2026 vergelijking", "Duidelijke prijsranges", "Nederlandstalig en actueel"])
    lines.append("pros:")
    for p in pros:
        lines.append(f"- {p}")
    
    cons = data.get("cons", ["Prijzen kunnen wijzigen", "Voorwaarden veranderen regelmatig", "Keuze hangt af van je situatie"])
    lines.append("cons:")
    for c in cons:
        lines.append(f"- {c}")
    
    lines.append("affiliateLinks:")
    for link in data.get("affiliateLinks", [
        "https://www.beehiiv.com/?via=anonymous-operator",
        "https://taskade.com/?via=55nfr2",
        "https://writesonic.com/?via=aitoolsnl",
        "https://rytr.me?via=hermes-affiliates",
        "https://www.synthesia.io?via=hermes",
        "https://www.make.com/en/register?pc=hermesai",
        "https://www.frase.io/?via=hermes10"
    ]):
        lines.append(f"- {link}")
    
    lines.append(f"date: {today}")
    lines.append("modelYear: 2026")
    lines.append(f"featuredTool: \"{data.get('featuredTool', '')}\"")
    lines.append(f"readingTime: \"{data.get('readingTime', '8 min')}\"")
    
    tools = data.get("tools", [])
    if not tools:
        tools = [
            {"name": "Product 1", "verdict": "Gebruiksvriendelijk met goede features.", "priceRange": "€100-300", "bestFor": "Kleinere huizen", "rating": 4.5, "affiliateLink": "https://example.com"},
            {"name": "Product 2", "verdict": "Krachtige functionaliteiten voor gevorderden.", "priceRange": "€300-800", "bestFor": "Grote woningen", "rating": 4.7, "affiliateLink": "https://example.com"},
            {"name": "Product 3", "verdict": "Betaalbare oplossing met voldoende kwaliteit.", "priceRange": "€200-500", "bestFor": "Middenklasse", "rating": 4.2, "affiliateLink": "https://example.com"}
        ]
    
    lines.append("tools:")
    for tool in tools:
        lines.append(f"- name: \"{tool.get('name', 'Unknown')}\"")
        lines.append(f"  verdict: \"{tool.get('verdict', '')}\"")
        lines.append(f"  priceRange: \"{tool.get('priceRange', '€0-0')}\"")
        lines.append(f"  bestFor: \"{tool.get('bestFor', '')}\"")
        lines.append(f"  rating: {tool.get('rating', 4.0)}")
        lines.append(f"  affiliateLink: \"{tool.get('affiliateLink', 'https://example.com')}\"")
    
    lines.append("related:")
    for rel in related_slugs:
        lines.append(f"  - {rel}")
    
    faq = data.get("faq", [])
    if faq:
        lines.append("faq:")
        for qa in faq:
            lines.append(f"- q: \"{qa.get('q', '')}\"")
            lines.append(f"  a: \"{qa.get('a', '')}\"")
    
    lines.append("---\n")
    lines.append(data.get("body_markdown", f"# {data.get('title', slug.replace('-', ' ').title())}\n\nDit artikel vergelijkt de beste opties voor {slug.replace('-', ' ')}.\n\nInhoud volgt binnenkort."))
    return "\n".join(lines)

def main():
    import requests
    
    generated = 0
    failed = []
    
    for topic_data in TOPICS:
        slug = topic_data["slug"]
        topic = topic_data["topic"]
        category = topic_data["category"]
        audience = topic_data["audience"]
        providers = topic_data["providers"]
        
        out_path = os.path.join(ARTICLES_DIR, f"{slug}.md")
        if os.path.exists(out_path):
            print(f"SKIP {slug} — already exists")
            continue
        
        print(f"Generating {slug}...")
        
        prompt = f"""Je bent een Nederlandse tech-journalist gespecialiseerd in slimme technologie voor thuis en tuin. Schrijf een compleet vergelijkingsartikel over:

ONDERWERP: {topic}
CATEGORIE: {category}
DOELGROEP: {audience}
AANBIEDERS: {providers}

STRUCTUUR:
1. ## Inleiding (2-3 alinea's)
2. ## Snel advies (3 bullets: "Kies X als je...")
3. ## Vergelijking per aanbieder (5-7 secties met ### koppen)
4. ## Waar op letten? (3-4 alinea's)
5. ## Vergelijkingstabel (Markdown tabel)
6. ## Conclusie (1-2 alinea's)
7. ## Veelgestelde vragen (minimaal 3 FAQ)

Schrijf in levendig Nederlands voor een Nederlands publiek. Gebruik concrete prijzen in euro's. Minimaal 800 woorden."""
        
        raw = call_ollama(prompt)
        if not raw:
            print(f"  Failed to generate content")
            failed.append(slug)
            continue
        
        data = parse_response(raw)
        
        # Pick related articles
        related = pick_related(slug, n=3)
        
        # Build article
        article_content = build_article(data, slug, category, related)
        
        # Write file
        os.makedirs(ARTICLES_DIR, exist_ok=True)
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(article_content)
        
        print(f"  ✓ Created {out_path}")
        generated += 1
        
        # Throttle
        time.sleep(5)
    
    print(f"\nDONE: {generated}/{len(TOPICS)} articles generated.")
    if failed:
        print(f"Failed: {', '.join(failed)}")

if __name__ == "__main__":
    main()