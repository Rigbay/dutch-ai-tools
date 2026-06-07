#!/usr/bin/env python3
"""Retry the 2 failed articles from generate-cron-20260605-hermes-compare.py"""
import os, time, sys, requests

API_KEY = os.environ.get("GEMINI_API_KEY", "").strip()
if not API_KEY:
    key_file = os.path.expanduser("~/.hermes/private/gemini-api-key")
    if os.path.exists(key_file):
        with open(key_file) as f:
            API_KEY = f.read().strip()
if not API_KEY:
    env_file = os.path.expanduser("~/.hermes/.env")
    if os.path.exists(env_file):
        with open(env_file) as f:
            for line in f:
                if line.startswith("GEMINI_API_KEY="):
                    API_KEY = line.split("=", 1)[1].strip().strip('"').strip("'")
                    break

BASE_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent"
ARTICLES_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "src/content/articles")

# Copy the needed article definitions from the main script
ARTICLES = [
    {
        "slug": "sendcloud-vs-myparcel-vs-picqer-vs-montapacking-2026",
        "prompt": """Schrijf een Nederlands artikel van 1300-1600 woorden over bezorg- en fulfilmentplatforms voor Nederlandse webshops in 2026. Behandel 7 tools: Sendcloud, MyParcel, Picqer, Montapacking, ShippyPro, Wuunder, Paazl.

Structuur:
- Introductie: bezorglandschap 2026 — duurzaamheidslabels, AI-routing, slimme pakketkluis, carrier-diversificatie (PostNL, DHL, DPD, UPS, Budbee, Trunkrs)
- Per tool een ## kop met: beschrijving, prijsmodel (EUR/verzending of /maand), beste use case (kleine webshop, scale-up, 3PL, internationaal), carriers (gekoppelde vervoerders), AI-features (slimme carrierkeuze, voorspelde bezorgtijd), plus- en minpunten, verdict
- Een markdown-vergelijkingstabel: naam, prijs vanaf (EUR), aantal carriers, beste-voor, score (1-5)
- Conclusie: welk platform voor welk type webshop (<100 zendingen/mnd, 100-1000, 1000-10000, internationaal, 3PL/fulfilment)
- 3 FAQ-vragen over verzendplatforms kiezen
- Prijzen realistisch: Sendcloud gratis-€49/mnd + per label, MyParcel gratis-€35/mnd + label, Picqer €59-299/mnd, Montapacking €100-500+/mnd, ShippyPro €25-199/mnd, Wuunder €0-15/mnd + label, Paazl op aanvraag

Nederlandse markt. Vloeiend Nederlands. Praktische vergelijking voor e-commerce ondernemers.""",
        "title": "Sendcloud vs MyParcel vs Picqer vs Montapacking 2026: beste bezorgplatform voor webshops",
        "slug_file": "sendcloud-vs-myparcel-vs-picqer-vs-montapacking-2026",
        "description": "Vergelijk de beste Nederlandse bezorg- en fulfilmentplatforms in 2026: Sendcloud, MyParcel, Picqer, Montapacking, ShippyPro en Wuunder. Met prijzen, carrier-integraties en AI-slimme verzendopties.",
        "category": "business",
        "tools": [
            {"name": "Sendcloud", "verdict": "Breedste carrier-netwerk met slimme checkout-oplossing — de standaard voor groeiende webshops", "priceRange": "EUR 0-49/mnd + label", "bestFor": "Schaalbare webshops", "rating": 4.7, "affiliateLink": "https://www.sendcloud.nl/?ref=aitoolsnl"},
            {"name": "MyParcel", "verdict": "Beste prijs-kwaliteit met strakke PostNL-integratie — top voor Nederlandse MKB webshops", "priceRange": "EUR 0-35/mnd + label", "bestFor": "NL-gefocuste shops", "rating": 4.5, "affiliateLink": "https://www.myparcel.nl/?ref=aitoolsnl"},
            {"name": "Picqer", "verdict": "Volledig WMS met voorraadbeheer en pick-routes — ideaal voor eigen magazijn", "priceRange": "EUR 59-299/mnd", "bestFor": "Magazijnbeheer", "rating": 4.6, "affiliateLink": "https://picqer.com/nl?ref=aitoolsnl"},
            {"name": "Montapacking", "verdict": "All-in-one fulfilment met 10+ magazijnen — uitbesteden zonder kopzorgen", "priceRange": "EUR 100-500+/mnd", "bestFor": "Uitbestede logistiek", "rating": 4.4, "affiliateLink": "https://www.montapacking.nl/?ref=aitoolsnl"},
            {"name": "ShippyPro", "verdict": "Internationale focus met 180+ carriers — beste voor cross-border e-commerce", "priceRange": "EUR 25-199/mnd", "bestFor": "Internationaal", "rating": 4.3, "affiliateLink": "https://www.shippypro.com/?ref=aitoolsnl"},
            {"name": "Wuunder", "verdict": "Slimste carrier-vergelijking per zending met CO2-inzicht — beste voor duurzame shops", "priceRange": "EUR 0-15/mnd + label", "bestFor": "Duurzaamheid", "rating": 4.2, "affiliateLink": "https://www.wuunder.nl/?ref=aitoolsnl"},
            {"name": "Paazl", "verdict": "Premium checkout delivery optimalisatie — top voor grote retail brands", "priceRange": "Op aanvraag", "bestFor": "Enterprise retail", "rating": 4.1, "affiliateLink": "https://www.paazl.com/nl?ref=aitoolsnl"},
        ],
    },
    {
        "slug": "wix-ai-vs-durable-vs-10web-vs-hostinger-2026",
        "prompt": """Schrijf een Nederlands artikel van 1300-1600 woorden over AI website builders in 2026. Behandel 7 tools: Wix AI Website Builder, Durable, 10Web AI Builder, Hostinger AI Website Builder, Dorik AI, Relume (AI sitemap/wireframe), Pineapple Builder.

Structuur:
- Introductie: AI website bouwers 2026 — van prompt naar live site in minuten, vervangen ze developers?, Nederlandse adoptie, mobiel-responsief
- Per tool een ## kop met: beschrijving, prijsrange (EUR/maand), beste use case (portfolio, webshop, landingspagina, MKB-site), AI-kracht (tekst, design, SEO, afbeeldingen), plus- en minpunten, verdict
- Een markdown-vergelijkingstabel: naam, prijs vanaf (EUR), gratis tier, beste-voor, AI-niveau, score (1-5)
- Conclusie: welke AI builder voor welk type site (ZZP-portfolio, MKB-website, webshop, SaaS landing page, blog)
- 3 FAQ-vragen over AI website builders vs handmatig bouwen
- Prijzen realistisch: Wix AI €16-45/mnd, Durable €15-35/mnd, 10Web €12-60/mnd, Hostinger AI €3-8/mnd (met hosting), Dorik AI €8-39/mnd, Relume €15-49/mnd, Pineapple Builder €12-30/mnd

Nederlandse context. Benoem AVG/privacy, NL hosting (Hostinger heeft EU-servers). SEO-kwaliteit van AI-gegenereerde sites. Vloeiend Nederlands.""",
        "title": "Wix AI vs Durable vs 10Web vs Hostinger AI Builder 2026: beste AI website bouwer",
        "slug_file": "wix-ai-vs-durable-vs-10web-vs-hostinger-2026",
        "description": "Vergelijk de beste AI website builders in 2026: Wix AI, Durable, 10Web, Hostinger AI Builder, Dorik en Relume. Bouw in minuten een volledige website met AI — vergeleken op prijs, design en SEO.",
        "category": "development",
        "tools": [
            {"name": "Wix AI Builder", "verdict": "Meest complete AI builder met NL-taalondersteuning, e-commerce en 900+ templates", "priceRange": "EUR 16-45/mnd", "bestFor": "Allround & E-commerce", "rating": 4.7, "affiliateLink": "https://www.wix.com/?ref=aitoolsnl"},
            {"name": "Durable", "verdict": "Snelste van prompt naar live site (30 seconden) — perfect voor zzp'ers en kleine bedrijven", "priceRange": "EUR 15-35/mnd", "bestFor": "Snelle MKB sites", "rating": 4.5, "affiliateLink": "https://durable.co/?ref=aitoolsnl"},
            {"name": "10Web AI Builder", "verdict": "AI bouwt op WordPress-basis met Google PageSpeed 90+ — beste voor SEO", "priceRange": "EUR 12-60/mnd", "bestFor": "SEO & WordPress", "rating": 4.6, "affiliateLink": "https://10web.io/?ref=aitoolsnl"},
            {"name": "Hostinger AI Builder", "verdict": "Scherpste prijs inclusief hosting en gratis domein — onverslaanbaar voor budget", "priceRange": "EUR 3-8/mnd", "bestFor": "Budget & Beginners", "rating": 4.3, "affiliateLink": "https://www.hostinger.nl/ai-website-builder?ref=aitoolsnl"},
            {"name": "Dorik AI", "verdict": "Mooiste AI-designs met CMS-functionaliteit — ideaal voor content-rijke sites", "priceRange": "EUR 8-39/mnd", "bestFor": "Design & Content", "rating": 4.4, "affiliateLink": "https://dorik.com/?ref=aitoolsnl"},
            {"name": "Relume", "verdict": "AI wireframe en sitemap generator die exporteert naar Webflow/Figma — beste voor designers", "priceRange": "EUR 15-49/mnd", "bestFor": "Designers & Bureaus", "rating": 4.5, "affiliateLink": "https://www.relume.io/?ref=aitoolsnl"},
            {"name": "Pineapple Builder", "verdict": "Specifiek voor personal brands en portfolio's met strakke AI-designs", "priceRange": "EUR 12-30/mnd", "bestFor": "Personal Branding", "rating": 4.1, "affiliateLink": "https://pineapple-builder.com/?ref=aitoolsnl"},
        ],
    },
]

ALL_SLUGS = [f.replace(".md", "") for f in os.listdir(ARTICLES_DIR) if f.endswith(".md")]

def build_frontmatter(art):
    tools = []
    for t in art.get("tools", []):
        tools.append(f"""- name: {t['name']}
  verdict: {t['verdict']}
  priceRange: {t['priceRange']}
  bestFor: {t['bestFor']}
  rating: {t['rating']}
  affiliateLink: {t['affiliateLink']}""")
    tools_yaml = "\n".join(tools)

    related = [s for s in ALL_SLUGS if s != art["slug_file"]][:3]
    related_yaml = "\n".join(f"- {r}" for r in related)

    from datetime import date
    today = date.today().isoformat()

    return f"""---
title: '{art["title"]}'
slug: {art["slug_file"]}
description: '{art["description"]}'
category: {art["category"]}
rating: 4.5
priceRange: EUR 0-150/mnd
pros:
- Vergelijking van top tools in deze categorie
- Actuele 2026 marktdata met realistische prijzen
- Focus op Nederlandse context en gebruikers
cons:
- Prijzen onder voorbehoud — check actuele aanbiedingen
- Sommige features in beta of rolling release
affiliateLinks:
- https://www.beehiiv.com/?via=anonymous-operator
date: {today}
modelYear: 2026
featuredTool: {art["tools"][0]["name"]}
readingTime: 9 min
tools:
{tools_yaml}
related:
{related_yaml}
draft: false
faq:
- q: Wat is de beste tool in deze categorie?
  a: Dat hangt af van je budget en specifieke wensen. Lees de volledige vergelijking voor advies per type gebruiker.
- q: Zijn er gratis versies beschikbaar?
  a: De meeste tools bieden een gratis tier of proefperiode aan. Zie de prijsranges per tool.
- q: Werkt dit in het Nederlands?
  a: Ja, alle besproken tools ondersteunen Nederlands of hebben een Nederlandse interface.
---"""

def main():
    for art in ARTICLES:
        out_path = os.path.join(ARTICLES_DIR, f"{art['slug_file']}.md")
        if os.path.exists(out_path) and os.path.getsize(out_path) > 1000:
            print(f"SKIP: {art['slug_file']} already exists")
            continue

        print(f"GENERATING: {art['slug_file']}...", end=" ", flush=True)
        try:
            payload = {
                "contents": [{"parts": [{"text": art["prompt"]}]}],
                "generationConfig": {"temperature": 0.7, "maxOutputTokens": 4096, "topP": 0.95, "topK": 40}
            }
            url = f"{BASE_URL}?key={API_KEY}"
            resp = requests.post(url, json=payload, timeout=120)
            resp.raise_for_status()
            data = resp.json()
            body = data["candidates"][0]["content"]["parts"][0]["text"]

            fm = build_frontmatter(art)
            full = f"{fm}\n\n{body}\n"
            with open(out_path, "w") as f:
                f.write(full)
            print(f"OK ({os.path.getsize(out_path)} bytes)")
        except Exception as e:
            print(f"FAILED: {e}")

        time.sleep(3)

if __name__ == "__main__":
    main()
