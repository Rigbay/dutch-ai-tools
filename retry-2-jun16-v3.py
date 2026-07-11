#!/usr/bin/env python3
"""Retry 2 failed articles — V6: Gemini structured output with response_schema."""
import os, time, requests, json, sys
from datetime import date

def load_api_key():
    # Read from .env file
    env_path = os.path.expanduser("~/.hermes/.env")
    with open(env_path) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if "GEMINI_API_KEY" in line and "=" in line:
                return line.split("=", 1)[1].strip()
            if "GOOGLE_API_KEY" in line and "=" in line:
                return line.split("=", 1)[1].strip()
    return None

GKEY = load_api_key()
if not GKEY:
    print("FATAL: No key")
    sys.exit(1)

BASE_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent"
ARTICLES_DIR = "/workspace/dutch-ai-tools/src/content/articles"

def pick_related(new_slug, n=3):
    slugs = sorted([f.replace(".md", "") for f in os.listdir(ARTICLES_DIR) if f.endswith(".md")])
    return [s for s in slugs if s != new_slug][:n]

def call_gemini(prompt, schema):
    url = f"{BASE_URL}?key={GKEY}"
    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {
            "temperature": 0.7,
            "maxOutputTokens": 4096,
            "responseMimeType": "application/json",
            "responseSchema": schema
        }
    }
    for attempt in range(8):
        try:
            resp = requests.post(url, json=payload, timeout=120, headers={"Content-Type": "application/json"})
            if resp.status_code == 429:
                wait = 35 * (attempt + 1)
                print(f"  429 wait {wait}s")
                time.sleep(wait)
                continue
            if resp.status_code in (503, 500):
                print(f"  {resp.status_code} retry 30s")
                time.sleep(30)
                continue
            if resp.status_code != 200:
                print(f"  HTTP {resp.status_code}: {resp.text[:200]}")
                return None
            return resp.json()["candidates"][0]["content"]["parts"][0]["text"]
        except Exception as e:
            print(f"  Exception: {e}")
            time.sleep(15)
    return None

def build_article(data, slug):
    today = date.today().isoformat()
    lines = ["---"]
    lines.append(f"title: '{data.get('title', slug)}'")
    lines.append(f"slug: {slug}")
    desc = data.get("description", "")
    if len(desc) > 80:
        lines.append(f"description: >-\n  {desc}")
    else:
        lines.append(f"description: {desc}")
    lines.append(f"category: {data.get('category', 'persoonlijk')}")
    lines.append(f"rating: {data.get('rating', 4.3)}")
    lines.append(f"priceRange: {data.get('priceRange', 'EUR 0-50 per maand')}")
    
    pros = data.get("pros", ["Uitgebreide 2026 vergelijking", "Duidelijke prijsranges en use cases", "Nederlandstalig en actueel"])
    lines.append("pros:")
    for p in pros:
        lines.append(f"- {p}")
    
    cons = data.get("cons", ["Prijzen kunnen wijzigen", "Voorwaarden veranderen regelmatig", "Keuze hangt af van je situatie"])
    lines.append("cons:")
    for c in cons:
        lines.append(f"- {c}")
    
    links = data.get("affiliateLinks", [
        "https://www.beehiiv.com/",
        "https://taskade.com/?via=55nfr2",
        "https://writesonic.com/?via=aitoolsnl",
        "https://rytr.me?via=hermes-affiliates",
        "https://www.synthesia.io?via=hermes",
        "https://www.make.com/en/register?pc=hermesai",
        "https://www.frase.io/?via=hermes10",
    ])
    lines.append("affiliateLinks:")
    for link in links:
        lines.append(f"- {link}")
    
    lines.append(f"date: '{today}'")
    lines.append("modelYear: 2026")
    lines.append(f"featuredTool: {data.get('featuredTool', '')}")
    lines.append(f"readingTime: {data.get('readingTime', '8 min')}")
    
    tools = data.get("tools", [])
    lines.append("tools:")
    for t in tools:
        lines.append(f"- name: {t.get('name', '')}")
        lines.append(f"  verdict: {t.get('verdict', '')}")
        lines.append(f"  priceRange: {t.get('priceRange', '')}")
        lines.append(f"  bestFor: {t.get('bestFor', '')}")
        lines.append(f"  rating: {t.get('rating', 4.0)}")
        lines.append(f"  affiliateLink: {t.get('affiliateLink', '')}")
    
    related = data.get("related", pick_related(slug, 3))
    lines.append("related:")
    for r in related:
        lines.append(f"- {r}")
    
    lines.append("draft: false")
    
    faq = data.get("faq", [])
    if faq:
        lines.append("faq:")
        for item in faq:
            lines.append(f"- q: {item.get('q', '')}")
            lines.append(f"  a: {item.get('a', '')}")
    
    lines.append("---")
    lines.append("")
    lines.append(data.get("body_markdown", "").strip())
    
    return "\n".join(lines) + "\n"

SCHEMA = {
    "type": "OBJECT",
    "properties": {
        "title": {"type": "STRING"},
        "description": {"type": "STRING"},
        "category": {"type": "STRING"},
        "rating": {"type": "NUMBER"},
        "priceRange": {"type": "STRING"},
        "pros": {"type": "ARRAY", "items": {"type": "STRING"}},
        "cons": {"type": "ARRAY", "items": {"type": "STRING"}},
        "affiliateLinks": {"type": "ARRAY", "items": {"type": "STRING"}},
        "featuredTool": {"type": "STRING"},
        "readingTime": {"type": "STRING"},
        "tools": {
            "type": "ARRAY",
            "items": {
                "type": "OBJECT",
                "properties": {
                    "name": {"type": "STRING"},
                    "verdict": {"type": "STRING"},
                    "priceRange": {"type": "STRING"},
                    "bestFor": {"type": "STRING"},
                    "rating": {"type": "NUMBER"},
                    "affiliateLink": {"type": "STRING"}
                },
                "required": ["name", "verdict", "priceRange", "bestFor", "rating", "affiliateLink"]
            }
        },
        "related": {"type": "ARRAY", "items": {"type": "STRING"}},
        "faq": {
            "type": "ARRAY",
            "items": {
                "type": "OBJECT",
                "properties": {
                    "q": {"type": "STRING"},
                    "a": {"type": "STRING"}
                },
                "required": ["q", "a"]
            }
        },
        "body_markdown": {"type": "STRING"}
    },
    "required": ["title", "description", "category", "rating", "priceRange", "pros", "cons", "affiliateLinks", "featuredTool", "readingTime", "tools", "related", "faq", "body_markdown"]
}

PROMPT = """Je bent een Nederlandse consumentenjournalist. Schrijf een compleet vergelijkingsartikel over:

ONDERWERP: {topic}
CATEGORIE: {category}
DOELGROEP: {audience}
AANBIEDERS: {providers}

STRUCTUUR voor de body_markdown:
1. ## Inleiding (2-3 alinea's)
2. ## Snel advies (3 bullets: "Kies X als je...")
3. ## Vergelijking per aanbieder (5-7 secties met ### koppen)
4. ## Waar op letten? (3-4 alinea's)
5. ## Vergelijkingstabel (Markdown tabel)
6. ## Conclusie (1-2 alinea's)
7. ## Veelgestelde vragen (> FAQ blocks)

BELANGRIJK: Echte prijzen. Minimaal 5 tools. Minimaal 800 woorden body. Schrijf levendig Nederlands."""

ARTICLES = [
    ("zonnepanelen-vergelijken-2026-zonneplan-sungevity-solar-buddy-coolblue", "de beste zonnepanelen aanbieders: installatie, garantie, terugverdientijd en salderingsregeling 2026", "huis-tuin", "Nederlandse huiseigenaren die zonnepanelen willen laten installeren", "Zonneplan, Sungevity, Solar Buddy, Coolblue Energie, Essent Energie, Vandebron, Vereniging Eigen Huis"),
    ("thuisbatterijen-vergelijken-2026-sessy-zonneplan-nexus-enphase-solaredge", "de beste thuisbatterijen voor zonnepanelen: opslag, saldering en zelfverbruik in 2026", "huis-tuin", "Nederlandse huiseigenaren met zonnepanelen die een thuisbatterij overwegen", "Sessy, Zonneplan Nexus, Enphase IQ Battery, SolarEdge Home Battery, Huawei Luna2000, Growatt, BYD Battery-Box"),
]

for slug, topic, category, audience, providers in ARTICLES:
    out_path = os.path.join(ARTICLES_DIR, f"{slug}.md")
    if os.path.exists(out_path):
        print(f"SKIP {slug} — exists")
        continue
    
    prompt = PROMPT.format(topic=topic, category=category, audience=audience, providers=providers)
    tokens_in = int(len(prompt) / 3.5)
    cost = (tokens_in * 0.10 + 4000 * 0.40) / 1_000_000
    
    print(f"GEN {slug} (${cost:.4f})... ", end="", flush=True)
    t0 = time.time()
    
    raw = call_gemini(prompt, SCHEMA)
    if raw is None:
        print("FAILED: no response")
        continue
    
    try:
        data = json.loads(raw)
    except json.JSONDecodeError as e:
        print(f"FAILED: JSON parse at pos {e.pos}")
        continue
    
    article = build_article(data, slug)
    os.makedirs(ARTICLES_DIR, exist_ok=True)
    with open(out_path, "w") as f:
        f.write(article)
    
    elapsed = time.time() - t0
    body_len = len(data.get('body_markdown', ''))
    tools_n = len(data.get('tools', []))
    print(f"OK ({elapsed:.1f}s) body={body_len}c tools={tools_n}")
    
    time.sleep(3)

print(f"\nDONE: retry complete")
