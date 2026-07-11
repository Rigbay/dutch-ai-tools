#!/usr/bin/env python3
"""Generate one huis-tuin article directly."""
import os, requests, json, time, random

def load_api_key():
    env_path = os.path.expanduser("~/.hermes/.env")
    if not os.path.exists(env_path):
        return None
    with open(env_path) as f:
        for line in f:
            if line.startswith("GEMINI_API_KEY=") and not line.startswith("#"):
                return line.strip().split("=", 1)[1]
    return None

GKEY = load_api_key()
if not GKEY:
    print("FATAL: No GEMINI_API_KEY found")
    exit(1)

ARTICLES_DIR = "/workspace/dutch-ai-tools/src/content/articles"
existing_slugs = set()
if os.path.exists(ARTICLES_DIR):
    for f in os.listdir(ARTICLES_DIR):
        if f.endswith(".md"):
            existing_slugs.add(f.replace(".md", ""))

# Pick related slugs
def pick_related(slug, n=3):
    candidates = list(existing_slugs)
    if slug in candidates:
        candidates.remove(slug)
    return random.sample(candidates, min(n, len(candidates)))

topic = "Beste slimme thermostaten 2026 voor Nederlandse huishoudens"
slug = "beste-slimme-thermostaten-2026-nest-tado-honeywell"
category = "huis-tuin"
audience = "Nederlandse huiseigenaren en bewoners die energie willen besparen met slimme thermostaten"
providers = "Google Nest, Tado, Honeywell, Netatmo, Bosch, Eve"

if slug in existing_slugs:
    print(f"{slug} already exists")
    exit(0)

prompt = f"""Je bent een Nederlandse tech-journalist die gespecialiseerd is in AI tools voor bedrijven en professionals. Schrijf een compleet vergelijkingsartikel over:

ONDERWERP: {topic}
CATEGORIE: {category}
DOELGROEP: {audience}
AANBIEDERS: {providers}

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
  "title": "Beste slimme thermostaten 2026 voor Nederlandse huishoudens",
  "description": "Vergelijk de top slimme thermostaten in Nederland 2026. Welke thermostaat bespaart het meest op energiekosten en past het beste bij jouw situatie?",
  "category": "huis-tuin",
  "rating": 4.3,
  "priceRange": "€150-€500 eenmalig",
  "pros": ["Energiebesparing tot 30%", "Eenvoudige installatie en app", "Integratie met slimme huissystemen"],
  "cons": ["Initieel hoge aanschafkosten", "Mogelijke privacy risico's", "Afhankelijk van internetconnectie"],
  "affiliateLinks": ["https://www.beehiiv.com/", "https://taskade.com/?via=55nfr2"],
  "featuredTool": "Google Nest",
  "readingTime": "8 min",
  "tools": [
    {{"name": "Google Nest", "verdict": "Beste allround slimme thermostaat met Google integratie.", "priceRange": "€200-€400", "bestFor": "Nieuwe huiseigenaren", "rating": 4.7, "affiliateLink": "https://example.com"}},
    {{"name": "Tado", "verdict": "Sterk in energiebesparing en automatische planning.", "priceRange": "€150-€300", "bestFor": "Energiebewuste huishoudens", "rating": 4.5, "affiliateLink": "https://example.com"}},
    {{"name": "Honeywell", "verdict": "Betrouwbare optie met solide basisfunctionaliteit.", "priceRange": "€120-€250", "bestFor": "Budget bewuste gebruikers", "rating": 4.2, "affiliateLink": "https://example.com"}}
  ],
  "faq": [{{"q": "Hoeveel energie kan ik besparen?", "a": "Gemiddeld 15-30% afhankelijk van gebruik en isolatie."}}]
}}

DAN ===BODY=== op een eigen regel.

DAARNA de volledige artikeltekst in Markdown (800+ woorden). Dit mag gewone newlines bevatten, géén \\n escapes nodig.

BELANGRIJK: Schrijf levendig Nederlands. Geen superlatieven. Echte prijzen. Minimaal5 tools. Minimaal 800 woorden body. Géén markdown fences om de hele output."""

print(f"Generating {slug}...")
url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={GKEY}"
payload = {'contents': [{'parts': [{'text': prompt}]}], 'generationConfig': {'temperature': 0.7, 'maxOutputTokens': 4000}}

try:
    resp = requests.post(url, json=payload, timeout=180)
    if resp.status_code == 200:
        data = resp.json()
        text = data['candidates'][0]['content']['parts'][0]['text']
        print(f"Response length: {len(text)} chars")
        
        # Save raw for inspection
        with open('raw_output.txt', 'w', encoding='utf-8') as f:
            f.write(text)
        
        # Parse
        parts = text.split("===BODY===")
        if len(parts) < 2:
            print("No BODY delimiter found")
            exit(1)
        
        metadata_str = parts[0].strip()
        body_markdown = parts[1].strip()
        
        try:
            metadata = json.loads(metadata_str)
        except json.JSONDecodeError:
            # Fallback
            metadata = {
                "title": topic,
                "description": "Vergelijk de top slimme thermostaten in Nederland 2026.",
                "category": category,
                "rating": 4.3,
                "priceRange": "€150-€500 eenmalig",
                "pros": ["Energiebesparing", "Gemak", "Integratie"],
                "cons": ["Kosten", "Privacy", "Afhankelijkheid"],
                "featuredTool": "Google Nest",
                "readingTime": "8 min",
                "tools": [],
                "faq": []
            }
        
        # Build article
        today = "2026-06-17"
        lines = ["---"]
        lines.append(f"title: '{metadata.get('title', topic)}'")
        lines.append(f"slug: {slug}")
        lines.append(f"description: >-")
        lines.append(f"  {metadata.get('description', '')}")
        lines.append(f"category: {metadata.get('category', category)}")
        lines.append(f"rating: {metadata.get('rating', 4.3)}")
        lines.append(f"priceRange: {metadata.get('priceRange', '€150-€500 eenmalig')}")
        
        lines.append("pros:")
        for p in metadata.get("pros", []):
            lines.append(f"- {p}")
        lines.append("cons:")
        for c in metadata.get("cons", []):
            lines.append(f"- {c}")
        
        lines.append("affiliateLinks:")
        for link in metadata.get("affiliateLinks", ["https://www.beehiiv.com/", "https://taskade.com/?via=55nfr2"]):
            lines.append(f"- {link}")
        
        lines.append(f"date: {today}")
        lines.append("modelYear: 2026")
        lines.append('featuredTool: "Google Nest"')
        lines.append('readingTime: "8 min"')
        
        tools = metadata.get("tools", [])
        if not tools:
            tools = [
                {"name": "Google Nest", "verdict": "Beste allround slimme thermostaat met Google integratie.", "priceRange": "€200-€400", "bestFor": "Nieuwe huiseigenaren", "rating": 4.7, "affiliateLink": "https://example.com"},
                {"name": "Tado", "verdict": "Sterk in energiebesparing en automatische planning.", "priceRange": "€150-€300", "bestFor": "Energiebewuste huishoudens", "rating": 4.5, "affiliateLink": "https://example.com"},
                {"name": "Honeywell", "verdict": "Betrouwbare optie met solide basisfunctionaliteit.", "priceRange": "€120-€250", "bestFor": "Budget bewuste gebruikers", "rating": 4.2, "affiliateLink": "https://example.com"}
            ]
        
        lines.append("tools:")
        for tool in tools:
            name = tool.get("name", "")
            verdict = tool.get("verdict", "")
            price_range = tool.get("priceRange", "€0-0")
            best_for = tool.get("bestFor", "")
            rating = tool.get("rating", 4.0)
            affiliate_link = tool.get("affiliateLink", "https://example.com")
            lines.append(f'- name: "{name}"')
            lines.append(f'  verdict: "{verdict}"')
            lines.append(f'  priceRange: "{price_range}"')
            lines.append(f'  bestFor: "{best_for}"')
            lines.append(f'  rating: {rating}')
            lines.append(f'  affiliateLink: "{affiliate_link}"')
        
        related = pick_related(slug, n=3)
        lines.append("related:")
        for rel in related:
            lines.append(f"  - {rel}")
        
        faq = metadata.get("faq", [])
        if faq:
            lines.append("faq:")
            for qa in faq:
                q_text = qa.get("q", "")
                a_text = qa.get("a", "")
                lines.append(f'- q: "{q_text}"')
                lines.append(f'  a: "{a_text}"')
        
        lines.append("---\n")
        lines.append(body_markdown)
        
        out_path = os.path.join(ARTICLES_DIR, f"{slug}.md")
        os.makedirs(ARTICLES_DIR, exist_ok=True)
        with open(out_path, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))
        
        print(f"✓ Created {out_path}")
    else:
        print(f"Error: {resp.status_code} {resp.text[:200]}")
except Exception as e:
    print(f"Exception: {e}")