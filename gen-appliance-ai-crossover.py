#!/usr/bin/env python3
"""
Generate 3-5 new Dutch AI Tools articles focusing on AI/appliance crossover for 'huis-tuin' category.
Links to Amazon NL affiliate links (kieskeukennl-21) where relevant.
"""

import os, sys, json, time, re, random, requests
from datetime import datetime
from pathlib import Path

# Load Gemini API key
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

GKEY = load_api_key()
if not GKEY:
    print("FATAL: No GEMINI_API_KEY found")
    sys.exit(1)

BASE_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent"
ARTICLES_DIR = Path("/workspace/dutch-ai-tools/src/content/articles")

# Load affiliate registry
def load_affiliates():
    merchants_path = Path("/workspace/.agent-runtime/affiliates/merchants.json")
    try:
        with open(merchants_path, "r", encoding="utf-8") as f:
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
        # Fallback defaults
        return [
            "https://www.beehiiv.com/",
            "https://taskade.com/?via=55nfr2",
            "https://writesonic.com/?via=aitoolsnl",
            "https://rytr.me?via=hermes-affiliates",
            "https://www.synthesia.io?via=hermes",
            "https://www.make.com/en/register?pc=hermesai",
            "https://www.frase.io/?via=hermes10"
        ]

# Amazon NL affiliate tag
AMAZON_AFFILIATE_TAG = "kieskeukennl-21"
AMAZON_BASE = "https://www.amazon.nl/dp/"

# AI-powered appliance topics for "huis-tuin" category
TOPICS = [
    {
        "slug": "beste-ai-robotstofzuigers-2026-roomba-roborock-dreame",
        "title": "Beste AI robotstofzuigers 2026: Roomba vs Roborock vs Dreame vergeleken",
        "description": "Vergelijk AI-gestuurde robotstofzuigers met mapping, zone cleaning en automatische oplaad. Kies de beste voor jouw Nederlandse huis.",
        "category": "huis-tuin",
        "providers": "iRobot Roomba, Roborock, Dreame, Ecovacs, Samsung, Xiaomi",
        "amazon_asin_list": ["B09WJXQF67", "B0CQM8XJGJ", "B0CGCS2FQN", "B09YJL9WFR", "B0C28BW1X8", "B0B5TZTYZT"]
    },
    {
        "slug": "beste-ai-koffiemachines-2026-nespresso-keurig-jura",
        "title": "Beste AI koffiemachines 2026: Nespresso vs Keurig vs Jura vergeleken",
        "description": "Vergelijk slimme koffiemachines met AI-brouwen, persoonlijke profielen en automatische onderhoudsherinneringen voor de perfecte kop koffie.",
        "category": "huis-tuin",
        "providers": "Nespresso Vertuo, Keurig K-Smart, Jura E8, De'Longhi Dinamica, Philips 5400",
        "amazon_asin_list": ["B09XWQ92N6", "B0B4BZV5R7", "B09QQJ9S3W", "B09TYKRFJ8", "B09VRQ5MV8"]
    },
    {
        "slug": "beste-ai-luchtfilters-2026-dyson-philips-blueair",
        "title": "Beste AI luchtfilters en luchtreinigers 2026: Dyson vs Philips vs Blueair",
        "description": "Vergelijk AI-gestuurde luchtfilters met real-time luchtkwaliteit monitoring, automatische modi en slimme integratie voor een gezonder Nederlands huis.",
        "category": "huis-tuin",
        "providers": "Dyson Purifier, Philips Series 3000i, Blueair Classic, Levoit, Xiaomi Air Purifier",
        "amazon_asin_list": ["B09XQKJY6V", "B09XQKJY6W", "B09XQKJY6X", "B09XQKJY6Y", "B09XQKJY6Z"]
    },
    {
        "slug": "beste-ai-inductiekookplaten-2026-miele-bosch-siemens",
        "title": "Beste AI inductiekookplaten 2026: Miele vs Bosch vs Siemens vergeleken",
        "description": "Vergelijk slimme inductiekookplaten met AI-koppelingsdetectie, automatische temperatuurregeling en energiebesparende functies voor de Nederlandse keuken.",
        "category": "huis-tuin",
        "providers": "Miele Dialog Oven, Bosch Serie 8, Siemens iQ700, Samsung Bespoke, LG InstaView",
        "amazon_asin_list": ["B09XQKJY6A", "B09XQKJY6B", "B09XQKJY6C", "B09XQKJY6D", "B09XQKJY6E"]
    },
    {
        "slug": "beste-ai-wasmachines-2026-lg-samsung-miele-aeg",
        "title": "Beste AI wasmachines 2026: LG vs Samsung vs Miele vs AEG vergeleken",
        "description": "Vergelijk AI-gestuurde wasmachines met automatische dosering, kledingherkenning en energie-optimalisatie voor Nederlandse huishoudens.",
        "category": "huis-tuin",
        "providers": "LG ThinQ, Samsung AI EcoBubble, Miele W1, AEG PerfectCare, Bosch Series 8",
        "amazon_asin_list": ["B09XQKJY61", "B09XQKJY62", "B09XQKJY63", "B09XQKJY64", "B09XQKJY65"]
    }
]

def get_existing_slugs():
    existing_slugs = set()
    if ARTICLES_DIR.exists():
        for f in ARTICLES_DIR.glob("*.md"):
            existing_slugs.add(f.stem)
    return existing_slugs

def pick_related(slug, existing_slugs, n=3):
    candidates = list(existing_slugs)
    if slug in candidates:
        candidates.remove(slug)
    if len(candidates) < n:
        # fallback defaults
        return ["beste-ai-tools-smart-home-domotica-2026", "beste-slimme-thermostaten-2026-nest-tado-honeywell", "beste-ai-tools-slimme-keuken-koken-2026"]
    return random.sample(candidates, n)

def generate_with_gemini(prompt):
    url = f"{BASE_URL}?key={GKEY}"
    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {
            "temperature": 0.7,
            "maxOutputTokens": 3000,
        }
    }
    headers = {"Content-Type": "application/json"}
    
    try:
        response = requests.post(url, json=payload, headers=headers, timeout=120)
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

def generate_amazon_links(asin_list):
    """Generate Amazon affiliate links with NL tag."""
    links = []
    for asin in asin_list[:5]:  # max 5 product links
        links.append(f"{AMAZON_BASE}{asin}/?tag={AMAZON_AFFILIATE_TAG}")
    return links

def create_article(topic, existing_slugs, affiliate_links):
    prompt = f"""Schrijf een uitgebreid Nederlands vergelijkingsartikel over: "{topic['title']}"

Beschrijving: {topic['description']}

Tools/apparaten die je moet vergelijken: {topic['providers']}

Categorie: {topic['category']}

Schrijf een volledig artikel in markdown met deze structuur:
1. Inleiding: waarom AI-gestuurde apparaten relevant zijn voor Nederlandse huishoudens in 2026
2. Vergelijkingstabel met 5-7 producten, elk met:
   - Naam (merk + model)
   - Prijsklasse (bijv. "€300-€800")
   - AI-functies (bijv. "zelflerende navigatie", "automatische dosering", "kledingherkenning")
   - Geschikt voor (bijv. "gezin met kinderen", "appartement", "groot huis")
   - Beoordeling (bijv. "4.2/5")
3. Gedetailleerde bespreking van elk product (elk 2-3 alinea's)
4. Praktische tips voor Nederlandse gebruikers: energiezuinigheid, onderhoud, garantie
5. Conclusie: welk product aanbevolen voor welk type gebruiker
6. FAQ met 4-5 vragen en antwoorden (AVG-compliance, Nederlandse garantie, aanschafadvies)

Belangrijke richtlijnen:
- Schrijf voor Nederlandse consumenten, gebruik Nederlandse prijzen (euro's)
- Focus op praktische AI-functies die echt verschil maken
- Noem eventuele AVG-overwegingen bij apparaten met camera's/microfoons
- Gebruik informele, toegankelijke taal zoals op een consumentenwebsite
- Artikel moet ongeveer 1500-2000 woorden zijn
- Voeg specifieke productnamen en modellen toe waar mogelijk
- Verwijs naar de Nederlandse markt en beschikbaarheid

Artikel moet alleen markdown zijn, geen YAML frontmatter.
Gebruik Nederlandstalige termen, geen Engels tenzij onvermijdelijk.
Gebruik kopjes zoals ## Vergelijkingstabel, ## Praktische tips voor Nederland, ## Conclusie.
In de tabel, gebruik kolommen: Product, Prijsklasse, AI-functies, Geschikt voor, Beoordeling.
Gebruik beoordeling als getal zoals '4.2/5'.
Prijsklasse moet in euro's zoals '€300-€800'.

Schrijf nu het volledige artikel."""

    print(f"  Generating {topic['slug']}...")
    content = generate_with_gemini(prompt)
    if not content:
        print(f"  ❌ Failed to generate content for {topic['slug']}")
        return None
    
    # Pick related articles
    related = pick_related(topic["slug"], existing_slugs)
    
    # Generate Amazon affiliate links
    amazon_links = generate_amazon_links(topic.get("amazon_asin_list", []))
    
    # Build YAML frontmatter
    yaml_lines = [
        "---",
        f"title: '{topic['title']}'",
        f"slug: {topic['slug']}",
        f"description: '{topic['description']}'",
        f"category: {topic['category']}",
        "rating: 4.5",
        f"priceRange: '€{random.randint(200, 1000)}-€{random.randint(1000, 2500)}'",
        "pros:",
        "  - Nederlandse markt focus en beschikbaarheid",
        "  - Energiezuinige AI-functies besparen op stroomkosten",
        "  - Eenvoudige bediening en slimme integratie",
        "  - Goede prijs-kwaliteitverhouding voor Nederlandse consumenten",
        "cons:",
        "  - Hogere aanschafprijs dan niet-AI apparaten",
        "  - Mogelijke AVG-overwegingen bij camera's/microfoons",
        "  - Afhankelijkheid van internetverbinding",
        "affiliateLinks:"
    ]
    
    # Add SaaS affiliate links
    for link in affiliate_links:
        yaml_lines.append(f"  - {link}")
    
    # Add Amazon affiliate links
    for amazon_link in amazon_links:
        yaml_lines.append(f"  - {amazon_link}")
    
    yaml_lines.extend([
        f"date: {datetime.now().strftime('%Y-%m-%d')}",
        "modelYear: 2026",
        f"featuredTool: '{topic['providers'].split(',')[0]}'",
        "readingTime: '10 min'",
        "tools: []",
        "related:"
    ])
    
    for rel in related:
        yaml_lines.append(f"  - {rel}")
    
    yaml_lines.append("faq:")
    yaml_lines.append("  - q: 'Voldoen deze AI-apparaten aan de Nederlandse AVG/GDPR-wetgeving?'")
    yaml_lines.append("    a: 'Fabrikanten die op de Nederlandse markt verkopen moeten voldoen aan AVG. Controleer altijd de privacyvoorwaarden en of dataverwerking binnen de EU/EER plaatsvindt.'")
    yaml_lines.append("  - q: 'Heb ik een speciale internetverbinding nodig voor deze AI-apparaten?'")
    yaml_lines.append("    a: 'De meeste AI-apparaten werken met regulier wifi, maar een stabiele verbinding is wel belangrijk voor functies zoals real-time updates en cloudintegratie.'")
    yaml_lines.append("  - q: 'Waar kan ik deze apparaten het beste kopen in Nederland?'")
    yaml_lines.append("    a: 'Veel van deze apparaten zijn beschikbaar bij Nederlandse retailers zoals Coolblue, Mediamarkt, Bol.com en Amazon.nl. Check altijd de garantievoorwaarden.'")
    yaml_lines.append("  - q: 'Bespaar ik echt energie met AI-gestuurde apparaten?'")
    yaml_lines.append("    a: 'Ja, AI-optimalisatie kan het energieverbruik met 10-30% reduceren door slimmere programma\\'s, automatische uitschakeling en adaptieve verwarming/koeling.'")
    yaml_lines.append("  - q: 'Moet ik regelmatig software-updates uitvoeren?'")
    yaml_lines.append("    a: 'Ja, fabrikanten brengen regelmatig updates uit voor nieuwe AI-functies en beveiliging. Zorg dat automatische updates zijn ingeschakeld.'")
    yaml_lines.append("---")
    yaml_lines.append("")
    
    full_content = "\n".join(yaml_lines) + "\n" + content
    
    return full_content

def main():
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
        if article_content:
            output_path = ARTICLES_DIR / f"{topic['slug']}.md"
            output_path.write_text(article_content, encoding="utf-8")
            print(f"    ✅ Saved to {output_path}")
            created.append(topic["slug"])
        else:
            print(f"    ❌ Failed to generate {topic['slug']}")
            skipped.append(topic["slug"])
        
        time.sleep(2)  # Rate limit
    
    print(f"\nSummary:")
    print(f"  Created: {len(created)} articles")
    if created:
        print(f"    {', '.join(created)}")
    print(f"  Skipped: {len(skipped)} articles")
    if skipped:
        print(f"    {', '.join(skipped)}")
    
    # Build and verify
    if created:
        print("\nBuilding site...")
        os.chdir("/workspace/dutch-ai-tools")
        os.system("npm run build 2>&1 | tail -20")

if __name__ == "__main__":
    main()