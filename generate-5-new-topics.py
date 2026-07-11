#!/usr/bin/env python3
"""Generate 5 new comparison articles for Dutch AI Tools site."""

import os, sys, json, time, re, random, requests
from datetime import datetime

# Load Gemini API key
def load_api_key():
    env_path = os.path.expanduser("~/.hermes/.env")
    if not os.path.exists(env_path):
        return None
    with open(env_path) as f:
        for line in f:
            if line.startswith("GEMINI_API_KEY=") and not line.startswith("#"):
                return line.strip().split("=", 1)[1]
            if line.startswith("GOOGLE_API_KEY=") and not line.startswith("#"):
                return line.strip().split("=", 1)[1]
    return None

GKEY = load_api_key()
if not GKEY:
    print("FATAL: No GEMINI_API_KEY found")
    sys.exit(1)

BASE_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent"
ARTICLES_DIR = "/workspace/dutch-ai-tools/src/content/articles"

# Existing slugs to avoid duplicates
existing_slugs = set()
if os.path.exists(ARTICLES_DIR):
    for f in os.listdir(ARTICLES_DIR):
        if f.endswith(".md"):
            existing_slugs.add(f.replace(".md", ""))

# 5 new topics covering underrepresented but high-potential niches
TOPICS = [
    {
        "slug": "ai-tools-onderwijs-nederland-2026",
        "topic": "AI tools voor onderwijs in Nederland 2026",
        "category": "productiviteit",
        "audience": "Nederlandse docenten, leraren, onderwijsassistenten en educatieve professionals",
        "providers": "Kahoot!, Quizlet, Socrative, Nearpod, ClassDojo, Google Classroom, Microsoft Education"
    },
    {
        "slug": "ai-tools-gezondheidszorg-therapeuten-2026",
        "topic": "AI tools voor gezondheidszorg en therapie 2026",
        "category": "productiviteit",
        "audience": "Nederlandse zorgprofessionals, therapeuten, psychologen en gezondheidscoaches",
        "providers": "Ada Health, Babylon Health, Woebot, K Health, Buoy Health, Symptomate, HealthTap"
    },
    {
        "slug": "ai-tools-video-editing-nederlands-2026",
        "topic": "Beste AI tools voor video editing en content creatie in Nederland",
        "category": "creatie",
        "audience": "Nederlandse videomakers, content creators, YouTubers en social media professionals",
        "providers": "Runway ML, Descript, Pika Labs, HeyGen, Synthesia, InVideo, Pictory, CapCut"
    },
    {
        "slug": "ai-tools-zakelijke-automatisering-2026",
        "topic": "AI tools voor zakelijke automatisering en workflow optimalisatie",
        "category": "business",
        "audience": "Nederlandse ondernemers, ZZP'ers, managers en bedrijven die processen willen automatiseren",
        "providers": "Zapier, Make (Integromat), n8n, Bardeen, IFTTT, Microsoft Power Automate, Workato"
    },
    {
        "slug": "ai-tools-klantenservice-chatbots-2026",
        "topic": "Beste AI chatbots en klantenservice tools voor Nederlandse bedrijven",
        "category": "business",
        "audience": "Nederlandse bedrijven die klantenservice willen automatiseren met AI",
        "providers": "Intercom, Drift, Freshchat, Zendesk Answer Bot, Ada, Ultimate.ai, Landbot, ManyChat"
    }
]

# Filter out existing slugs
TOPICS = [t for t in TOPICS if t["slug"] not in existing_slugs]
if not TOPICS:
    print("All target articles already exist.")
    sys.exit(0)

def pick_related(slug, n=3):
    """Pick n random related articles (excluding current slug)."""
    candidates = list(existing_slugs)
    if slug in candidates:
        candidates.remove(slug)
    return random.sample(candidates, min(n, len(candidates)))

def call_gemini(prompt):
    """Call Gemini API with retry logic."""
    url = f"{BASE_URL}?key={GKEY}"
    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {"temperature": 0.7, "maxOutputTokens": 4096}
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

def parse_response(raw):
    """Parse Gemini response with JSON metadata block + ===BODY=== delimiter."""
    raw = raw.strip()
    if raw.startswith("```"):
        lines = raw.split("\n")
        lines = lines[1:]
        if lines and lines[-1].strip() == "```":
            lines = lines[:-1]
        raw = "\n".join(lines)
    
    # Split on delimiter
    parts = raw.split("===BODY===")
    if len(parts) < 2:
        for delim in ["---BODY---", "###BODY###", "***BODY***"]:
            parts = raw.split(delim)
            if len(parts) >= 2:
                break
    
    if len(parts) < 2:
        print("  No BODY delimiter found, falling back to full text")
        return {"title": "", "description": "", "tools": [], "affiliateLinks": [], "body_markdown": raw}
    
    json_part = parts[0].strip()
    body_part = parts[1].strip()
    
    # Fix escaped newlines in JSON
    fixed = []
    in_str = False
    esc = False
    for ch in json_part:
        if esc:
            fixed.append(ch); esc = False; continue
        if ch == '\\':
            fixed.append(ch); esc = True; continue
        if ch == '"':
            in_str = not in_str; fixed.append(ch); continue
        if in_str and ch == '\n':
            fixed.append('\\n')
        elif in_str and ch == '\r':
            fixed.append('\\r')
        elif in_str and ch == '\t':
            fixed.append('\\t')
        else:
            fixed.append(ch)
    
    try:
        data = json.loads(''.join(fixed))
    except json.JSONDecodeError as e:
        print(f"  JSON parse failed at pos {e.pos}")
        # Fallback: extract title and description
        title_match = re.search(r'"title"\s*:\s*"([^"]+)"', json_part)
        desc_match = re.search(r'"description"\s*:\s*"([^"]+)"', json_part)
        data = {
            "title": title_match.group(1) if title_match else "",
            "description": desc_match.group(1) if desc_match else "",
            "tools": [],
            "affiliateLinks": [],
            "pros": [],
            "cons": [],
            "rating": 4.3,
            "priceRange": "€0-100 per maand",
            "featuredTool": "",
            "readingTime": "8 min",
            "faq": []
        }
    
    data["body_markdown"] = body_part
    return data

def build_article(data, slug, category, related_slugs):
    """Build final markdown article with frontmatter."""
    today = datetime.now().strftime("%Y-%m-%d")
    lines = ["---"]
    lines.append(f"title: '{data.get('title', slug)}'")
    lines.append(f"slug: {slug}")
    
    desc = data.get("description", "")
    if len(desc) > 80:
        lines.append(f"description: >-\n  {desc}")
    else:
        lines.append(f"description: {desc}")
    
    lines.append(f"category: {category}")
    lines.append(f"rating: {data.get('rating', 4.3)}")
    lines.append(f"priceRange: {data.get('priceRange', '€0-100 per maand')}")
    
    # Pros/cons
    pros = data.get("pros", ["Uitgebreide 2026 vergelijking", "Duidelijke prijsranges en use cases", "Nederlandstalig en actueel"])
    lines.append("pros:")
    for p in pros:
        lines.append(f"- {p}")
    
    cons = data.get("cons", ["Prijzen kunnen wijzigen", "Voorwaarden veranderen regelmatig", "Keuze hangt af van je situatie"])
    lines.append("cons:")
    for c in cons:
        lines.append(f"- {c}")
    
    # Affiliate links (placeholders)
    affiliate_links = data.get("affiliateLinks", [
        "https://www.beehiiv.com/",
        "https://taskade.com/?via=55nfr2",
        "https://writesonic.com/?via=aitoolsnl",
        "https://rytr.me?via=hermes-affiliates",
        "https://www.synthesia.io?via=hermes",
        "https://www.make.com/en/register?pc=hermesai",
        "https://www.frase.io/?via=hermes10"
    ])
    lines.append("affiliateLinks:")
    for link in affiliate_links:
        lines.append(f"- {link}")
    
    lines.append(f"date: {today}")
    lines.append("modelYear: 2026")
    lines.append(f"featuredTool: \"{data.get('featuredTool', '')}\"")
    lines.append(f"readingTime: \"{data.get('readingTime', '8 min')}\"")
    
    # Tools array
    tools = data.get("tools", [])
    if not tools:
        # Create placeholder tools
        tools = [
            {"name": "Tool 1", "verdict": "Gebruiksvriendelijk met goede integraties.", "priceRange": "€10-50/mnd", "bestFor": "Kleinere teams", "rating": 4.5, "affiliateLink": "https://example.com"},
            {"name": "Tool 2", "verdict": "Krachtige AI-functionaliteiten voor gevorderden.", "priceRange": "€50-200/mnd", "bestFor": "Grote organisaties", "rating": 4.7, "affiliateLink": "https://example.com"},
            {"name": "Tool 3", "verdict": "Betaalbare oplossing met voldoende features.", "priceRange": "€20-80/mnd", "bestFor": "MKB", "rating": 4.2, "affiliateLink": "https://example.com"}
        ]
    
    lines.append("tools:")
    for tool in tools:
        lines.append("- name: \"{}\"".format(tool.get("name", "Unknown")))
        lines.append(f"  verdict: \"{tool.get('verdict', '')}\"")
        lines.append(f"  priceRange: \"{tool.get('priceRange', '€0-0/mnd')}\"")
        lines.append(f"  bestFor: \"{tool.get('bestFor', '')}\"")
        lines.append(f"  rating: {tool.get('rating', 4.0)}")
        lines.append(f"  affiliateLink: \"{tool.get('affiliateLink', 'https://example.com')}\"")
    
    # Related articles
    lines.append("related:")
    for rel in related_slugs:
        lines.append(f"  - {rel}")
    
    # FAQ
    faq = data.get("faq", [])
    if faq:
        lines.append("faq:")
        for qa in faq:
            lines.append(f"- q: \"{qa.get('q', '')}\"")
            lines.append(f"  a: \"{qa.get('a', '')}\"")
    
    lines.append("---\n")
    lines.append(data.get("body_markdown", ""))
    return "\n".join(lines)

def main():
    import requests
    
    total_cost = 0
    generated = 0
    failed = []
    
    PROMPT_TEMPLATE = """Je bent een Nederlandse tech-journalist die gespecialiseerd is in AI tools voor bedrijven en professionals. Schrijf een compleet vergelijkingsartikel over:

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
  "title": "Beste [onderwerp] 2026: [ondertitel]",
  "description": "[150-170 tekens SEO Nederlands]",
  "category": "{category}",
  "rating": 4.3,
  "priceRange": "€[min]-[max] per maand",
  "pros": ["pro 1", "pro 2", "pro 3"],
  "cons": ["con 1", "con 2", "con 3"],
  "affiliateLinks": ["https://www.beehiiv.com/", "https://taskade.com/?via=55nfr2", "https://writesonic.com/?via=aitoolsnl", "https://rytr.me?via=hermes-affiliates", "https://www.synthesia.io?via=hermes", "https://www.make.com/en/register?pc=hermesai", "https://www.frase.io/?via=hermes10"],
  "featuredTool": "[Beste aanbieder]",
  "readingTime": "8 min",
  "tools": [
    {{"name": "...", "verdict": "...", "priceRange": "€X-Y/mnd", "bestFor": "...", "rating": 4.X, "affiliateLink": "https://..."}}
  ],
  "faq": [{{"q": "...", "a": "..."}}]
}}

DAN ===BODY=== op een eigen regel.

DAARNA de volledige artikeltekst in Markdown (800+ woorden). Dit mag gewone newlines bevatten, géén \\\\n escapes nodig.

BELANGRIJK: Schrijf levendig Nederlands. Geen superlatieven. Echte prijzen. Minimaal 5 tools. Minimaal 800 woorden body. Géén markdown fences om de hele output."""

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
        
        prompt = PROMPT_TEMPLATE.format(topic=topic, category=category, audience=audience, providers=providers)
        tokens_in = int(len(prompt) / 3.5)
        cost = (tokens_in * 0.10 + 4000 * 0.40) / 1_000_000
        total_cost += cost
        
        raw = call_gemini(prompt)
        if not raw:
            print(f"  Failed to generate content")
            failed.append(slug)
            continue
        
        data = parse_response(raw)
        if not data:
            print(f"  Failed to parse response")
            failed.append(slug)
            continue
        
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
        time.sleep(2)
    
    print(f"\nDONE: {generated}/{len(TOPICS)} articles, cost ${total_cost:.4f}")
    if failed:
        print(f"Failed: {', '.join(failed)}")

if __name__ == "__main__":
    main()