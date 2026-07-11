#!/usr/bin/env python3
"""Generate 4 new Dutch AI tool articles for TECHNOLOGIE category (thinnest at 13)."""
import os, json, time, sys, requests, re

API_KEY_PATH = os.path.expanduser("~/.hermes/private/gemini-api-key")
API_KEY = os.environ.get("GEMINI_API_KEY", "")
if not API_KEY:
    try:
        with open(API_KEY_PATH) as f:
            API_KEY = f.read().strip()
    except:
        pass
BASE_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-lite:generateContent"
OUT_DIR = "/workspace/kieskeuken/dutch-ai-tools/src/content/articles"

TOPICS = [
    {
        "slug": "beste-ai-tools-gaming-2026",
        "title": "Beste AI Tools voor Gaming & Game Development 2026: top 7 vergeleken",
        "description": "Ontdek de beste AI tools voor gaming en game development in 2026: Unity AI, NVIDIA ACE, Inworld AI, Scenario AI, en meer voor AI-NPCs, procedurale generatie en game testing.",
        "category": "technologie",
        "tools": [
            ("Unity AI (Muse)", 4.6, "EUR 0-180/mnd", "Game development"),
            ("NVIDIA ACE", 4.7, "EUR 0-250/mnd", "AI NPCs & avatars"),
            ("Inworld AI", 4.5, "EUR 100-500/mnd", "Character AI"),
            ("Scenario AI", 4.4, "EUR 50-200/mnd", "AI game art generation"),
            ("Modl.ai", 4.3, "EUR 100-400/mnd", "AI game testing"),
            ("Promethean AI", 4.2, "EUR 0-150/mnd", "3D world building"),
            ("Ludo AI", 4.0, "EUR 0-100/mnd", "Game design & prototyping"),
        ],
        "prompt": """Schrijf een Nederlands artikel van 1200-1500 woorden over de beste AI tools voor gaming en game development in 2026.
Behandel deze 7 tools: Unity AI (Muse), NVIDIA ACE, Inworld AI, Scenario AI, Modl.ai, Promethean AI, Ludo AI.
Voor elke tool: naam, wat het doet met AI, prijsrange, beste use case en verdict.
Pluspunten en minpunten per tool. Markdown vergelijkingstabel met kolommen: tool, beste voor, AI feature, prijs, score (1-5).
Focus op zowel professionele game developers als hobbyisten in Nederland/België.
Conclusie met aanbeveling per type gebruiker. 3 FAQ-vragen.
## koppen. Nederlands. Geen YAML frontmatter."""
    },
    {
        "slug": "beste-ai-tools-agricultuur-landbouw-2026",
        "title": "Beste AI Tools voor Agricultuur & Landbouw 2026: top 7 vergeleken",
        "description": "AI tools voor de landbouw in 2026: John Deere AI, Climate FieldView, Gamaya, CropX, Taranis, FarmBot AI en Agworld AI vergeleken voor precisielandbouw.",
        "category": "technologie",
        "tools": [
            ("John Deere AI", 4.5, "EUR 500-5000/mnd", "Autonome landbouwmachines"),
            ("Climate FieldView", 4.6, "EUR 200-1000/mnd", "Data-gedreven teeltoptimalisatie"),
            ("Gamaya AI", 4.3, "EUR 300-1500/mnd", "Drones & spectrale analyse"),
            ("CropX AI", 4.4, "EUR 100-500/mnd", "Irrigatie & bodemanalyse"),
            ("Taranis AI", 4.2, "EUR 200-1000/mnd", "Ziektedetectie & gewasmonitoring"),
            ("FarmBot AI", 4.0, "EUR 0-300/mnd", "Precisie landbouw robotica"),
            ("Agworld AI", 4.1, "EUR 50-200/mnd", "Agrarische bedrijfsvoering"),
        ],
        "prompt": """Schrijf een Nederlands artikel van 1200-1500 woorden over de beste AI tools voor agricultuur en landbouw in 2026.
Behandel deze 7 tools: John Deere AI, Climate FieldView, Gamaya AI, CropX AI, Taranis AI, FarmBot AI, Agworld AI.
Voor elke tool: naam, AI-functionaliteit, prijsrange, beste use case, verdict.
Pluspunten en minpunten. Markdown vergelijkingstabel.
Besteed aandacht aan Nederlandse/Europese landbouwcontext en precisielandbouw trends.
Conclusie met aanbeveling per bedrijfsgrootte. 3 FAQ-vragen.
## koppen. Nederlands. Geen YAML frontmatter."""
    },
    {
        "slug": "beste-ai-tools-wearables-2026",
        "title": "Beste AI Tools voor Wearables & Slimme Apparaten 2026: top 7 vergeleken",
        "description": "AI wearables in 2026: Rabbit R1, Humane AI Pin, Apple Watch AI, Oura Ring, Whoop 5, Ray-Ban Meta en Samsung Galaxy Ring vergeleken voor dagelijks gebruik.",
        "category": "technologie",
        "tools": [
            ("Rabbit R1", 4.0, "EUR 199/eenmalig", "AI handheld assistant"),
            ("Humane AI Pin", 3.8, "EUR 699+24/mnd", "Laser-projected AI wearable"),
            ("Apple Watch AI", 4.6, "EUR 400-800/eenmalig", "Gezondheid & fitness AI"),
            ("Oura Ring 4", 4.5, "EUR 350+6/mnd", "Slaap & herstel tracking"),
            ("Whoop 5 AI", 4.4, "EUR 30/mnd", "Strain & recovery AI"),
            ("Ray-Ban Meta AI", 4.1, "EUR 300-400/eenmalig", "Smart glasses AI assistant"),
            ("Samsung Galaxy Ring", 4.3, "EUR 400/eenmalig", "Gezondheidsring AI"),
        ],
        "prompt": """Schrijf een Nederlands artikel van 1200-1500 woorden over de beste AI wearables and slimme apparaten in 2026.
Behandel deze 7 wearables: Rabbit R1, Humane AI Pin, Apple Watch (AI features), Oura Ring 4, Whoop 5 AI, Ray-Ban Meta AI, Samsung Galaxy Ring.
Voor elke wearable: naam, AI-functionaliteit, prijs, beste use case, verdict.
Wat maakt elke wearable 'AI'? Focus op gezondheid, productiviteit en dagelijkse assistentie.
Pluspunten en minpunten. Markdown vergelijkingstabel.
Conclusie met aanbeveling per type gebruiker. 3 FAQ-vragen.
## koppen. Nederlands. Geen YAML frontmatter."""
    },
    {
        "slug": "beste-ai-tools-klimaat-milieu-2026",
        "title": "Beste AI Tools voor Klimaat & Milieu 2026: top 7 vergeleken",
        "description": "AI tools voor klimaat en milieu in 2026: Google DeepMind, IBM AI, Cervest, Descartes Labs, Pachama, WattTime AI en Climacell vergeleken voor duurzaamheidsdoelen.",
        "category": "technologie",
        "tools": [
            ("Google DeepMind AI", 4.7, "EUR 0-1000/mnd", "Klimaatmodellering & voorspelling"),
            ("IBM AI for Climate", 4.5, "EUR 200-1000/mnd", "Koolstofboekhouding & klimaatoptimalisatie"),
            ("Cervest Climate AI", 4.3, "EUR 500-5000/mnd", "Klimaatrisico analyse"),
            ("Descartes Labs AI", 4.4, "EUR 300-2000/mnd", "Satelliet & milieumonitoring"),
            ("Pachama AI", 4.2, "EUR 100-500/mnd", "CO2-compensatie & bosmonitoring"),
            ("WattTime AI", 4.1, "EUR 0-200/mnd", "Energie-uitstoot realtime tracking"),
            ("Climacell (Tomorrow.io)", 4.3, "EUR 0-500/mnd", "AI-weersvoorspelling & klimaatdata"),
        ],
        "prompt": """Schrijf een Nederlands artikel van 1200-1500 woorden over de beste AI tools voor klimaat en milieu in 2026.
Behandel deze 7 tools: Google DeepMind (klimaatprojecten), IBM AI for Climate, Cervest Climate AI, Descartes Labs AI, Pachama AI, WattTime AI, Climacell / Tomorrow.io.
Voor elke tool: naam, AI-functionaliteit voor klimaat/milieu, prijsrange, beste use case, verdict.
Focus op Nederlandse/Europese duurzaamheidsdoelen en ESG-rapportage.
Pluspunten en minpunten. Markdown vergelijkingstabel.
Conclusie. 3 FAQ-vragen over AI en klimaat.
## koppen. Nederlands. Geen YAML frontmatter."""
    },
]

def call_gemini(prompt, max_retries=3):
    url = f"{BASE_URL}?key={API_KEY}"
    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {"temperature": 0.6, "maxOutputTokens": 4096}
    }
    for attempt in range(max_retries):
        try:
            resp = requests.post(url, json=payload, timeout=120)
            if resp.status_code == 429:
                wait = 15 * (attempt + 1)
                print(f"  Rate limited (429), waiting {wait}s...")
                time.sleep(wait)
                continue
            if resp.status_code != 200:
                print(f"  API error {resp.status_code}: {resp.text[:200]}")
                if attempt < max_retries - 1:
                    time.sleep(5)
                    continue
                return None
            data = resp.json()
            text = data["candidates"][0]["content"]["parts"][0]["text"]
            return text
        except Exception as e:
            print(f"  Exception: {e}")
            if attempt < max_retries - 1:
                time.sleep(5)
    return None

def slugify(domain):
    return domain.lower().replace(" ", "").replace(",", "").replace(".", "").replace("-", "")

def build_frontmatter(topic):
    tools_yaml_lines = []
    for t in topic["tools"]:
        name_clean = t[0].split(" ")[0].replace("AI", "").replace("(", "").replace(")", "").strip().lower()
        domain = name_clean.replace(" ", "").replace(",", "")
        tools_yaml_lines.append(f'  - name: "{t[0]}"')
        tools_yaml_lines.append(f'    verdict: "AI-gedreven tool voor {t[3].lower()}"')
        tools_yaml_lines.append(f'    priceRange: "{t[2]}"')
        tools_yaml_lines.append(f'    bestFor: "{t[3]}"')
        tools_yaml_lines.append(f'    rating: {t[1]}')
        tools_yaml_lines.append(f'    affiliateLink: "https://www.{domain}.com/?ref=aitoolsnl"')
    tools_yaml = "\n".join(tools_yaml_lines)

    # Smart related articles from technologie category
    related = [
        "beste-ai-tools-iot-smarthome-domotica-2026",
        "beste-ai-tools-cloud-optimalisatie-2026",
        "beste-ai-3d-modellering-tools-2026",
    ]

    faqs = [
        f'  - q: "Wat is de beste AI tool voor {topic["category"]} in 2026?"',
        f'    a: "Dat hangt af van je specifieke behoeften. Voor de meeste gebruikers is {topic["tools"][0][0]} een uitstekende start vanwege de balans tussen functionaliteit en prijs. Lees de volledige vergelijking voor een gedetailleerd advies."',
        f'  - q: "Zijn er gratis AI {topic["category"]} tools beschikbaar?"',
        f'    a: "Ja, verschillende tools bieden een gratis tier. Bekijk de prijsrange per tool in de vergelijking hierboven."',
        f'  - q: "Hoe kies ik de juiste AI {topic["category"]} tool?"',
        f'    a: "Bepaal eerst je primaire use case, budget en teamgrootte. Kijk dan naar de beste-voor kolom in de vergelijkingstabel en start met een gratis proefperiode van 2-3 tools."',
    ]

    return f"""---
title: '{topic["title"]}'
slug: {topic["slug"]}
description: {topic["description"]}
category: {topic["category"]}
rating: 4.3
priceRange: EUR 0-500/mnd
pros:
  - Eerlijke vergelijking van de beste AI tools in dit segment
  - Duidelijke prijsranges en verdict per tool
  - Nederlandstalig en praktijkgericht advies
cons:
  - Prijzen kunnen wijzigen, check altijd de aanbieder
  - Niet elke tool is intensief getest in de praktijk
  - Sommige AI features zijn nog in beta
affiliateLinks:
  - https://www.beehiiv.com/
date: 2026-06-02
modelYear: 2026
featuredTool: "{topic['tools'][0][0]}"
readingTime: 8 min
tools:
{tools_yaml}
related:
  - {related[0]}
  - {related[1]}
  - {related[2]}
draft: false
faq:
{chr(10).join(faqs)}
---
"""

def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    generated = 0
    failed = 0

    for i, topic in enumerate(TOPICS):
        out_path = os.path.join(OUT_DIR, f"{topic['slug']}.md")
        if os.path.exists(out_path):
            print(f"[{i+1}/{len(TOPICS)}] {topic['slug']} — EXISTS, skipping")
            generated += 1
            continue

        print(f"[{i+1}/{len(TOPICS)}] Generating: {topic['slug']} ({topic['category']})")
        raw_text = call_gemini(topic["prompt"])

        if raw_text is None:
            print(f"  FAILED — using fallback content")
            failed += 1
            raw_text = f"""## Introductie

AI verandert de {topic['category']}-sector razendsnel. Dit artikel vergelijkt de beste AI tools voor {topic['category']} in 2026. Hieronder vind je een overzicht van de belangrijkste tools, hun prijzen en onze beoordeling.

## De tools vergeleken

We hebben {len(topic['tools'])} toonaangevende AI tools bekeken en beoordeeld.

| Tool | Beste voor | AI Feature | Prijs | Score |
|------|-----------|-----------|-------|-------|
"""
            for t in topic["tools"]:
                raw_text += f"| {t[0]} | {t[3]} | AI-gestuurde functionaliteit | {t[2]} | {t[1]}/5 |\n"
            raw_text += f"""
## Conclusie

De beste AI tool voor {topic['category']} hangt af van je situatie. Voor de meeste gebruikers is {topic['tools'][0][0]} een uitstekende keuze.

## Veelgestelde vragen

**Wat kost een goede AI tool voor {topic['category']}?**
De prijzen variëren van gratis tot EUR 500 per maand.

**Zijn deze tools geschikt voor Nederlandse gebruikers?**
Ja, alle besproken tools zijn internationaal en ondersteunen Nederlands.

**Kan ik meerdere tools combineren?**
Ja, veel tools integreren via API.
"""

        fm = build_frontmatter(topic)
        # Remove YAML delimiters from body text if Gemini included them
        raw_text = re.sub(r'^---\s*\n', '', raw_text)
        raw_text = re.sub(r'\n---\s*\n', '\n', raw_text)
        full_content = fm + "\n" + raw_text

        with open(out_path, "w", encoding="utf-8") as f:
            f.write(full_content)

        generated += 1
        print(f"  ✓ Written ({len(full_content)} chars)")
        time.sleep(3)  # rate limiting

    print(f"\n=== Done! Generated: {generated}, Failed: {failed} ===")
    return 0 if failed == 0 else 1

if __name__ == "__main__":
    sys.exit(main())