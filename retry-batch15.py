#!/usr/bin/env python3
"""Retry failed articles from batch 15 (e-commerce and interior design)."""
import os, glob as globmod, requests, yaml, time, sys
from datetime import date

API_KEY = os.environ.get("GEMINI_API_KEY", "").strip()
if not API_KEY:
    key_file = os.path.expanduser("~/.hermes/.env")
    if os.path.exists(key_file):
        for line in open(key_file):
            if line.startswith("GEMINI_API_KEY="):
                API_KEY = line.split("=", 1)[1].strip().strip('"').strip("'")

BASE_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent"
ARTICLES_DIR = "/workspace/dutch-ai-tools/src/content/articles"

ALL_SLUGS = sorted([f.replace(".md","").replace(f"{ARTICLES_DIR}/","") for f in globmod.glob(f"{ARTICLES_DIR}/*.md")])

def pick_related(slug, pool, n=3):
    return [s for s in pool if s != slug][:n]

articles = [
    {
        "slug": "beste-ai-e-commerce-dropshipping-tools-2026",
        "title": "Beste AI Tools voor E-commerce & Dropshipping 2026: top 7 vergeleken",
        "description": "AI tools die e-commerce en dropshipping automatiseren in 2026. Vergelijk Spocket, DSers, Zendrop, Sell The Trend, EcomHunt, Niche Scraper en SaleHoo voor productonderzoek, orderverwerking en marketing.",
        "category": "business",
        "prompt": "Schrijf een Nederlands artikel van 1200-1500 woorden over de beste AI tools voor e-commerce en dropshipping in 2026. Behandel precies 7 tools: Spocket, DSers, Zendrop, Sell The Trend, EcomHunt, Niche Scraper, SaleHoo. Gebruik ## koppen per tool met beschrijving, prijsrange in EUR, beste use case, plus- en minpunten, verdict. Voeg een markdown-vergelijkingstabel toe. Eindig met conclusie en 3 FAQ. Focus op Nederlandse context.",
        "tools": [
            {"name":"Spocket","verdict":"AI-gebaseerd dropshipping platform met focus op EU- en US-leveranciers","priceRange":"EUR 25-100/mnd","bestFor":"Snelle levering EU & VS","rating":4.5,"affiliateLink":"https://www.spocket.co/?ref=aitoolsnl"},
            {"name":"DSers","verdict":"AI-gestuurd order management en product sourcing voor AliExpress","priceRange":"EUR 0-30/mnd","bestFor":"AliExpress dropshipping","rating":4.3,"affiliateLink":"https://www.dsers.com/?ref=aitoolsnl"},
            {"name":"Zendrop","verdict":"AI-order fulfillment platform met eigen magazijn","priceRange":"EUR 0-60/mnd","bestFor":"Branded fulfillment","rating":4.2,"affiliateLink":"https://www.zendrop.com/?ref=aitoolsnl"},
            {"name":"Sell The Trend","verdict":"AI-product research engine met winstberekening en trendanalyse","priceRange":"EUR 30-80/mnd","bestFor":"AI productonderzoek","rating":4.6,"affiliateLink":"https://www.sellthetrend.com/?ref=aitoolsnl"},
            {"name":"EcomHunt","verdict":"Dagelijkse AI-geselecteerde productvondsten","priceRange":"EUR 0-40/mnd","bestFor":"Dagelijkse product curation","rating":4.1,"affiliateLink":"https://ecomhunt.com/?ref=aitoolsnl"},
            {"name":"Niche Scraper","verdict":"AI-product scraper en validator","priceRange":"EUR 12-30/mnd","bestFor":"Product validatie","rating":4.3,"affiliateLink":"https://www.nichescraper.com/?ref=aitoolsnl"},
            {"name":"SaleHoo","verdict":"AI-leveranciersdirectory met 8000+ geverifieerde groothandels","priceRange":"EUR 60/jaar","bestFor":"Groothandel sourcing","rating":4.4,"affiliateLink":"https://www.salehoo.com/?ref=aitoolsnl"},
        ],
        "related": pick_related("beste-ai-e-commerce-dropshipping-tools-2026", ALL_SLUGS, 3)
    },
    {
        "slug": "beste-ai-interieur-ontwerp-tools-2026",
        "title": "Beste AI Interieur & Woonontwerp Tools 2026: top 6 vergeleken",
        "description": "AI tools voor interieurontwerp en woninginrichting in 2026. Vergelijk Planner 5D, Interior AI, HomeByMe, RoomGPT, DecorMatters en Hutch voor AI-gestuurd woonadvies en virtuele inrichting.",
        "category": "technologie",
        "prompt": "Schrijf een Nederlands artikel van 1200-1500 woorden over de beste AI tools voor interieurontwerp en woninginrichting in 2026. Behandel precies 6 tools: Planner 5D, Interior AI, HomeByMe, RoomGPT, DecorMatters, Hutch. Gebruik ## koppen per tool met beschrijving, prijsrange in EUR, beste use case, plus- en minpunten, verdict. Voeg een markdown-vergelijkingstabel toe. Eindig met conclusie en 3 FAQ. Focus op Nederlandse context.",
        "tools": [
            {"name":"Planner 5D","verdict":"AI-gestuurde 2D/3D interieurontwerper","priceRange":"EUR 0-15/mnd","bestFor":"Volledig 3D-interieurontwerp","rating":4.6,"affiliateLink":"https://planner5d.com/?ref=aitoolsnl"},
            {"name":"Interior AI","verdict":"AI die fotos omzet in heringerichte ruimtes","priceRange":"EUR 0-20/mnd","bestFor":"Snelle stijl-visualisatie","rating":4.5,"affiliateLink":"https://interiorai.com/?ref=aitoolsnl"},
            {"name":"HomeByMe","verdict":"3D-interieurplatform met AI-room planner","priceRange":"EUR 0-10/mnd","bestFor":"Realistische 3D-plattegronden","rating":4.3,"affiliateLink":"https://homeby.me/?ref=aitoolsnl"},
            {"name":"RoomGPT","verdict":"AI-remodelling tool die fotos transformeert","priceRange":"EUR 0-15/mnd","bestFor":"Stijl-transformatie fotos","rating":4.4,"affiliateLink":"https://www.roomgpt.io/?ref=aitoolsnl"},
            {"name":"DecorMatters","verdict":"AI-interieur app met augmented reality","priceRange":"EUR 0-10/mnd","bestFor":"AR-meubelvisualisatie","rating":4.2,"affiliateLink":"https://www.decormatters.com/?ref=aitoolsnl"},
            {"name":"Hutch","verdict":"AI-interieur stylist voor complete kamers","priceRange":"EUR 0-30/eenmalig","bestFor":"Complete styling op maat","rating":4.1,"affiliateLink":"https://www.hutch.com/?ref=aitoolsnl"},
        ],
        "related": pick_related("beste-ai-interieur-ontwerp-tools-2026", ALL_SLUGS, 3)
    }
]

for i, art in enumerate(articles, 1):
    slug = art["slug"]
    out_path = os.path.join(ARTICLES_DIR, f"{slug}.md")
    if os.path.exists(out_path):
        print(f"[{i}/2] {slug} ALREADY EXISTS, skipping")
        continue
    print(f"[{i}/2] {slug}...", end=" ", flush=True)
    time.sleep(2)  # brief delay
    url = f"{BASE_URL}?key={API_KEY}"
    resp = requests.post(url, json={
        "contents": [{"parts": [{"text": art["prompt"]}]}],
        "generationConfig": {"temperature": 0.8, "topP": 0.95, "maxOutputTokens": 4096}
    }, timeout=120)
    if resp.status_code != 200:
        print(f"FAIL {resp.status_code}")
        time.sleep(5)
        # retry once
        resp = requests.post(url, json={
            "contents": [{"parts": [{"text": art["prompt"]}]}],
            "generationConfig": {"temperature": 0.8, "topP": 0.95, "maxOutputTokens": 4096}
        }, timeout=120)
        if resp.status_code != 200:
            print(f"RETRY FAIL {resp.status_code}: {resp.text[:100]}")
            continue
    text = resp.json()["candidates"][0]["content"]["parts"][0]["text"]
    fm = {
        "title": art["title"], "slug": slug, "description": art["description"],
        "category": art["category"], "rating": 4.5, "priceRange": "EUR 0-50/mnd",
        "pros": ["Gebaseerd op actuele marktdata uit 2026","Duidelijke vergelijking met prijzen","Nederlandstalig voor NL gebruikers"],
        "cons": ["Prijzen kunnen wijzigen","Niet elke tool dagelijks getest","Sommige AI-features nog in beta"],
        "affiliateLinks": [t["affiliateLink"] for t in art["tools"]],
        "related": art["related"], "date": date.today().isoformat(),
        "modelYear": 2026, "featuredTool": art["tools"][0]["name"],
        "readingTime": "7 min", "tools": art["tools"],
    }
    with open(out_path, "w") as f:
        f.write("---\n")
        f.write(yaml.dump(fm, allow_unicode=True, default_flow_style=False, sort_keys=False))
        f.write("---\n\n")
        f.write(text)
    print(f"OK ({len(text)} chars)")
    time.sleep(3)

print("Done")