#!/usr/bin/env python3
"""Generate final article: Optimizely vs VWO 2026."""
import os, time, sys, requests, yaml
from datetime import date

key_file = os.path.expanduser("~/.hermes/private/gemini-api-key")
with open(key_file) as f:
    API_KEY = f.read().strip()

BASE_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent"
ARTICLES_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "src/content/articles")

prompt = """Schrijf een Nederlands artikel van 1200-1500 woorden over Optimizely vs VWO vs AB Tasty vs Convert in 2026. Behandel precies 7 tools: Optimizely, VWO, AB Tasty, Convert Experiences, Crazy Egg, Kameleoon, PostHog Experiments.

Structuur:
- Introductie: A/B testing 2026 — AI-gestuurde personalisatie, server-side testing, cookieloze tracking, NL/EU privacy
- Per tool een ## kop: beschrijving, prijs (EUR/maand bij start), beste use case, plus- en minpunten, verdict
- Markdown vergelijkingstabel: naam, prijs vanaf, beste voor, AI-personalisatie, server-side, AVG-compliant, score (1-5)
- Conclusie: voor startup webshop, MKB marketingteam, enterprise e-commerce, budget-bewust, AI-first, privacy-first
- 3 FAQ's

Let op: Google Optimize is gestopt (2023). Europese tools benadrukken: AB Tasty (Frans), Kameleoon (Frans). AVG/cookieloze tracking relevant. Server-side testing voor betrouwbare data. Vloeiend Nederlands."""

url = f"{BASE_URL}?key={API_KEY}"
payload = {"contents": [{"parts": [{"text": prompt}]}], "generationConfig": {"temperature": 0.7, "maxOutputTokens": 4096}}

for attempt in range(5):
    try:
        resp = requests.post(url, json=payload, timeout=120, headers={"Content-Type": "application/json"})
        if resp.status_code == 429:
            wait = 30*(attempt+1)
            print(f"429 wait {wait}s")
            time.sleep(wait)
            continue
        if resp.status_code not in (200,):
            print(f"HTTP {resp.status_code}: {resp.text[:200]}")
            time.sleep(15)
            continue
        data = resp.json()
        body = data["candidates"][0]["content"]["parts"][0]["text"]
        print(f"OK {len(body.split())} words")

        slugs = sorted([f.replace(".md","") for f in os.listdir(ARTICLES_DIR) if f.endswith(".md")])
        related = [s for s in slugs if s != "optimizely-vs-vwo-vs-ab-tasty-vs-convert-2026"][:3]

        tools_data = [
            {"name": "Optimizely", "verdict": "Beste enterprise experimentatieplatform — full-stack, feature flags + web testing", "priceRange": "EUR 36.000+/jaar", "bestFor": "Enterprise & Full-stack", "rating": 4.6, "affiliateLink": "https://optimizely.com/?ref=aitoolsnl"},
            {"name": "VWO", "verdict": "Beste all-in-one CRO platform — testing + heatmaps + session recordings + surveys", "priceRange": "EUR 200-500/mnd", "bestFor": "MKB Marketing teams", "rating": 4.5, "affiliateLink": "https://vwo.com/?ref=aitoolsnl"},
            {"name": "AB Tasty", "verdict": "Beste EU-alternatief — Frans, AVG-compliant, sterke AI-personalisatie", "priceRange": "EUR 300-1500/mnd", "bestFor": "EU E-commerce", "rating": 4.4, "affiliateLink": "https://abtasty.com/?ref=aitoolsnl"},
            {"name": "Convert Experiences", "verdict": "Beste prijs-kwaliteit — onbeperkte tests, privacy-first, geen data-sharing", "priceRange": "EUR 99-499/mnd", "bestFor": "Budget & Privacy", "rating": 4.2, "affiliateLink": "https://convert.com/?ref=aitoolsnl"},
            {"name": "Crazy Egg", "verdict": "Beste visuele analyse — heatmaps, scrollmaps en confetti reports op schaal", "priceRange": "EUR 29-99/mnd", "bestFor": "Visuele Analyse & MKB", "rating": 4.0, "affiliateLink": "https://crazyegg.com/?ref=aitoolsnl"},
            {"name": "Kameleoon", "verdict": "Frans AI-first platform — realtime personalisatie, sterke EU-compliance", "priceRange": "EUR 500-2000/mnd", "bestFor": "AI-personalisatie", "rating": 4.3, "affiliateLink": "https://kameleoon.com/?ref=aitoolsnl"},
            {"name": "PostHog Experiments", "verdict": "Open-source Google Optimize alternatief — feature flags + A/B testing + analytics", "priceRange": "EUR 0 (tot 1M events/mnd)", "bestFor": "Google Optimize vervanger", "rating": 4.1, "affiliateLink": "https://posthog.com/?ref=aitoolsnl"},
        ]
        avg = round(sum(t["rating"] for t in tools_data) / len(tools_data), 1)
        article_data = {
            "title": "Optimizely vs VWO vs AB Tasty vs Convert 2026: beste A/B testing en CRO tools",
            "slug": "optimizely-vs-vwo-vs-ab-tasty-vs-convert-2026",
            "description": "Optimizely, VWO, AB Tasty of Convert in 2026? Vergelijk de beste A/B testing en conversie-optimalisatie platforms op features, prijs, AI en AVG-compliance voor Nederlandse marketeers.",
            "category": "business", "rating": avg, "priceRange": "EUR 0-100/mnd",
            "pros": ["Uitgebreide 2026 vergelijking", "Duidelijke prijsranges en use cases", "Nederlandstalig"],
            "cons": ["Prijzen kunnen wijzigen", "AI-features in ontwikkeling", "Niet alles dagelijks getest"],
            "affiliateLinks": ["https://www.beehiiv.com/?via=anonymous-operator"],
            "date": str(date.today()), "modelYear": 2026,
            "featuredTool": "Optimizely", "readingTime": "8 min",
            "tools": tools_data, "related": related, "draft": False,
            "faq": [
                {"q": "Wat is de beste tool?", "a": "Dat hangt af van je situatie. Optimizely is voor de meeste gebruikers een prima startpunt."},
                {"q": "Zijn er gratis alternatieven?", "a": "Ja, meerdere tools hebben gratis tiers. Perfect om te beginnen."},
                {"q": "Hoe kies ik de juiste tool?", "a": "Begin met je use case en budget. Filter de tabel op score en prijs."},
            ]
        }
        fm = yaml.dump(article_data, allow_unicode=True, default_flow_style=False, sort_keys=False, width=120)
        out_path = os.path.join(ARTICLES_DIR, "optimizely-vs-vwo-vs-ab-tasty-vs-convert-2026.md")
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(f"---\n{fm}---\n{body}")
        print("Written OK")
        break
    except Exception as e:
        print(f"Exception: {e}")
        time.sleep(15)
