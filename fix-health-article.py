#!/usr/bin/env python3
"""Regenerate the health article with proper content."""
import os, requests, json, sys

# Load Gemini API key
env_path = os.path.expanduser("~/.hermes/.env")
key = None
with open(env_path) as f:
    for line in f:
        if "GEMINI_API_KEY" in line and not line.startswith("#"):
            key = line.strip().split("=", 1)[1]
            break
if not key:
    print("No GEMINI_API_KEY found")
    sys.exit(1)

BASE_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent"
ARTICLES_DIR = "/workspace/dutch-ai-tools/src/content/articles"

topic = {
    "slug": "ai-tools-gezondheidszorg-therapeuten-2026",
    "topic": "AI tools voor gezondheidszorg en therapie 2026",
    "category": "productiviteit",
    "audience": "Nederlandse zorgprofessionals, therapeuten, psychologen en gezondheidscoaches",
    "providers": "Ada Health, Babylon Health, Woebot, K Health, Buoy Health, Symptomate, HealthTap"
}

prompt = f"""Je bent een Nederlandse tech-journalist die gespecialiseerd is in AI tools voor bedrijven en professionals. Schrijf een compleet vergelijkingsartikel over:

ONDERWERP: {topic['topic']}
CATEGORIE: {topic['category']}
DOELGROEP: {topic['audience']}
AANBIEDERS: {topic['providers']}

STRUCTUUR voor de body (na ===BODY===):
1. ## Inleiding (2-3 alinea's)
2. ## Snel advies (3 bullets: "Kies X als je...")
3. ## Vergelijking per aanbieder (5-7 secties met ### koppen)
4. ## Waar op letten? (3-4 alinea's)
5. ## Vergelijkingstabel (Markdown tabel)
6. ## Conclusie (1-2 alinea's)
7. ## Veelgestelde vragen (> FAQ blocks)

OUTPUT FORMAT — TWEE DELEN gescheiden door ===BODY===:

EERST de JSON metadata (géén body_markdown veld!):
{{
  "title": "Beste AI tools voor gezondheidszorg en therapie 2026: Een Gids voor de Nederlandse Zorgprofessional",
  "description": "Ontdek de top AI tools voor efficiëntere zorg en therapie in 2026. Vergelijk Ada Health, Woebot, K Health en meer voor de Nederlandse zorgprofessional.",
  "category": "productiviteit",
  "rating": 4.3,
  "priceRange": "€0-100 per maand",
  "pros": ["Energiebesparing", "Gemak", "Integratie"],
  "cons": ["Kosten", "Privacy", "Afhankelijkheid"],
  "affiliateLinks": ["https://www.beehiiv.com/", "https://taskade.com/?via=55nfr2", "https://writesonic.com/?via=aitoolsnl", "https://rytr.me?via=hermes-affiliates", "https://www.synthesia.io?via=hermes", "https://www.make.com/en/register?pc=hermesai", "https://www.frase.io/?via=hermes10"],
  "featuredTool": "Ada Health",
  "readingTime": "8 min",
  "tools": [
    {{"name": "Ada Health", "verdict": "Leidende AI-symptoomchecker met medische nauwkeurigheid.", "priceRange": "€0-50/mnd", "bestFor": "Huisartsenpraktijken", "rating": 4.7, "affiliateLink": "https://ada.com/nl"}},
    {{"name": "Woebot", "verdict": "CBT-gebaseerde therapeutische chatbot voor mentale gezondheid.", "priceRange": "€20-80/mnd", "bestFor": "Therapeuten en coaches", "rating": 4.5, "affiliateLink": "https://woebothealth.com"}},
    {{"name": "K Health", "verdict": "Datagestuurde AI voor gepersonaliseerde behandelplannen.", "priceRange": "€30-100/mnd", "bestFor": "Ziekenhuizen en specialisten", "rating": 4.6, "affiliateLink": "https://khealth.com"}},
    {{"name": "Babylon Health", "verdict": "Telehealth platform met AI-diagnostiek en videoconsults.", "priceRange": "€40-150/mnd", "bestFor": "Zorgorganisaties", "rating": 4.4, "affiliateLink": "https://babylonhealth.com"}},
    {{"name": "Buoy Health", "verdict": "AI-symptoomchecker met geïntegreerde doorverwijzing.", "priceRange": "€15-60/mnd", "bestFor": "GGD en publieke gezondheid", "rating": 4.3, "affiliateLink": "https://buoyhealth.com"}}
  ],
  "faq": [
    {{"q": "Zijn deze AI tools veilig voor medische diagnoses?", "a": "Ze zijn bedoeld als ondersteuning, niet als vervanging van een arts."}},
    {{"q": "Voldoen ze aan de AVG?", "a": "Ja, mits geïmplementeerd volgens Europese regelgeving."}}
  ]
}}

DAN ===BODY=== op een eigen regel.

DAARNA de volledige artikeltekst in Markdown (800+ woorden). Dit mag gewone newlines bevatten, géén \\n escapes nodig.

BELANGRIJK: Schrijf levendig Nederlands. Geen superlatieven. Echte prijzen. Minimaal 5 tools. Minimaal 800 woorden body. Géén markdown fences om de hele output."""

print(f"Calling Gemini API for {topic['slug']}...")
url = f"{BASE_URL}?key={key}"
payload = {
    "contents": [{"parts": [{"text": prompt}]}],
    "generationConfig": {"temperature": 0.7, "maxOutputTokens": 4096}
}

try:
    resp = requests.post(url, json=payload, timeout=180)
    if resp.status_code != 200:
        print(f"Error: {resp.status_code}")
        print(resp.text[:500])
        sys.exit(1)
    
    data = resp.json()
    text = data['candidates'][0]['content']['parts'][0]['text']
    print(f"Response length: {len(text)} chars")
    
    # Parse JSON and body
    if "===BODY===" not in text:
        print("Error: No ===BODY=== separator found")
        sys.exit(1)
    
    json_part, body_part = text.split("===BODY===", 1)
    json_part = json_part.strip()
    body_part = body_part.strip()
    
    # Parse JSON
    try:
        metadata = json.loads(json_part)
    except json.JSONDecodeError as e:
        print(f"JSON parse error: {e}")
        print("JSON part:", json_part[:500])
        sys.exit(1)
    
    # Build markdown
    output_lines = ["---"]
    for key, value in metadata.items():
        if key == "tools":
            output_lines.append("tools:")
            for tool in value:
                output_lines.append(f"- name: \"{tool['name']}\"")
                output_lines.append(f"  verdict: \"{tool['verdict']}\"")
                output_lines.append(f"  priceRange: \"{tool['priceRange']}\"")
                output_lines.append(f"  bestFor: \"{tool['bestFor']}\"")
                output_lines.append(f"  rating: {tool['rating']}")
                output_lines.append(f"  affiliateLink: \"{tool['affiliateLink']}\"")
        elif key == "faq":
            output_lines.append("faq:")
            for faq in value:
                output_lines.append(f"- q: \"{faq['q']}\"")
                output_lines.append(f"  a: \"{faq['a']}\"")
        else:
            if isinstance(value, list):
                output_lines.append(f"{key}:")
                for item in value:
                    output_lines.append(f"- \"{item}\"")
            else:
                output_lines.append(f"{key}: \"{value}\"")
    output_lines.append("---")
    output_lines.append("")
    output_lines.append(body_part)
    
    out_path = os.path.join(ARTICLES_DIR, f"{topic['slug']}.md")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write("\n".join(output_lines))
    
    print(f"Saved to {out_path}")
    print("Done.")
    
except Exception as e:
    print(f"Exception: {e}")
    sys.exit(1)