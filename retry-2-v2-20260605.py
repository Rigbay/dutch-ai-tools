#!/usr/bin/env python3
"""Retry 2 failed articles with longer delays and fallback model."""
import os, time, sys, requests

API_KEY=os.env...Y", "").strip()
if not API_KEY:
    key_file = os.path.expanduser("~/.hermes/private/gemini-api-key")
    if os.path.exists(key_file):
        with open(key_file) as f:
            API_KEY=f.read...
if not API_KEY:
    env_file = os.path.expanduser("~/.hermes/.env")
    if os.path.exists(env_file):
        with open(env_file) as f:
            for line in f:
                if line.startswith("GEMINI_API_KEY=***                    API_KEY=*** 1)[1].strip().strip('"').strip("'")
                    break

ARTICLES_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "src/content/articles")
ALL_SLUGS = [f.replace(".md", "") for f in os.listdir(ARTICLES_DIR) if f.endswith(".md")]

from datetime import date
today = date.today().isoformat()

ARTICLES = [
    {
        "slug": "sendcloud-vs-myparcel-vs-picqer-vs-montapacking-2026",
        "prompt": """Schrijf een Nederlands artikel van 1300-1600 woorden over bezorg- en fulfilmentplatforms voor Nederlandse webshops in 2026. Behandel 7 tools: Sendcloud, MyParcel, Picqer, Montapacking, ShippyPro, Wuunder, Paazl.

Structuur:
- Introductie: bezorglandschap 2026 — duurzaamheidslabels, AI-routing, slimme pakketkluis, carrier-diversificatie (PostNL, DHL, DPD, UPS, Budbee, Trunkrs)
- Per tool een ## kop met: beschrijving, prijsmodel, beste use case, carriers, AI-features, plus- en minpunten, verdict (1-2 zinnen)
- Een markdown-vergelijkingstabel: naam, prijs vanaf, aantal carriers, beste-voor, score (1-5)
- Conclusie: welk platform voor welk type webshop
- 3 FAQ-vragen over verzendplatforms kiezen
Nederlandse markt. Vloeiend Nederlands. Praktisch voor e-commerce.""",
        "frontmatter": """---
title: 'Sendcloud vs MyParcel vs Picqer vs Montapacking 2026: beste bezorgplatform voor webshops'
slug: sendcloud-vs-myparcel-vs-picqer-vs-montapacking-2026
description: 'Vergelijk de beste Nederlandse bezorg- en fulfilmentplatforms in 2026: Sendcloud, MyParcel, Picqer, Montapacking, ShippyPro en Wuunder. Met prijzen, carrier-integraties en AI-slimme verzendopties.'
category: business
rating: 4.5
priceRange: EUR 0-500/mnd
pros:
- Vergelijking van alle grote Nederlandse bezorgplatforms
- Actuele 2026 prijzen en carrier-integraties
- Praktische keuzehulp per type webshop
cons:
- Prijzen onder voorbehoud
- Fulfilmenttarieven sterk afhankelijk van volume
affiliateLinks:
- https://www.beehiiv.com/?via=anonymous-operator
date: """ + today + """
modelYear: 2026
featuredTool: Sendcloud
readingTime: 9 min
tools:
- name: Sendcloud
  verdict: Breedste carrier-netwerk met slimme checkout-oplossing — de standaard voor groeiende webshops
  priceRange: EUR 0-49/mnd + label
  bestFor: Schaalbare webshops
  rating: 4.7
  affiliateLink: https://www.sendcloud.nl/?ref=aitoolsnl
- name: MyParcel
  verdict: Beste prijs-kwaliteit met strakke PostNL-integratie — top voor Nederlandse MKB webshops
  priceRange: EUR 0-35/mnd + label
  bestFor: NL-gefocuste shops
  rating: 4.5
  affiliateLink: https://www.myparcel.nl/?ref=aitoolsnl
- name: Picqer
  verdict: Volledig WMS met voorraadbeheer en pick-routes — ideaal voor eigen magazijn
  priceRange: EUR 59-299/mnd
  bestFor: Magazijnbeheer
  rating: 4.6
  affiliateLink: https://picqer.com/nl?ref=aitoolsnl
- name: Montapacking
  verdict: All-in-one fulfilment met 10+ magazijnen — uitbesteden zonder kopzorgen
  priceRange: EUR 100-500+/mnd
  bestFor: Uitbestede logistiek
  rating: 4.4
  affiliateLink: https://www.montapacking.nl/?ref=aitoolsnl
- name: ShippyPro
  verdict: Internationale focus met 180+ carriers — beste voor cross-border e-commerce
  priceRange: EUR 25-199/mnd
  bestFor: Internationaal
  rating: 4.3
  affiliateLink: https://www.shippypro.com/?ref=aitoolsnl
- name: Wuunder
  verdict: Slimste carrier-vergelijking per zending met CO2-inzicht — beste voor duurzame shops
  priceRange: EUR 0-15/mnd + label
  bestFor: Duurzaamheid
  rating: 4.2
  affiliateLink: https://www.wuunder.nl/?ref=aitoolsnl
- name: Paazl
  verdict: Premium checkout delivery optimalisatie — top voor grote retail brands
  priceRange: Op aanvraag
  bestFor: Enterprise retail
  rating: 4.1
  affiliateLink: https://www.paazl.com/nl?ref=aitoolsnl
related:
-
""",
    },
    {
        "slug": "wix-ai-vs-durable-vs-10web-vs-hostinger-2026",
        "prompt": """Schrijf een Nederlands artikel van 1300-1600 woorden over AI website builders in 2026. Behandel 7 tools: Wix AI Website Builder, Durable, 10Web AI Builder, Hostinger AI Website Builder, Dorik AI, Relume, Pineapple Builder.

Structuur:
- Introductie: AI website bouwers 2026 — van prompt naar live site in minuten, vervangen ze developers?, Nederlandse adoptie
- Per tool een ## kop met: beschrijving, prijsrange, beste use case, AI-kracht, plus- en minpunten, verdict (1-2 zinnen)
- Een markdown-vergelijkingstabel: naam, prijs vanaf, gratis tier, beste-voor, AI-niveau, score (1-5)
- Conclusie: welke AI builder voor welk type site
- 3 FAQ-vragen over AI website builders vs handmatig bouwen
Nederlandse context. Benoem AVG/privacy. Vloeiend Nederlands.""",
        "frontmatter": """---
title: 'Wix AI vs Durable vs 10Web vs Hostinger AI Builder 2026: beste AI website bouwer'
slug: wix-ai-vs-durable-vs-10web-vs-hostinger-2026
description: 'Vergelijk de beste AI website builders in 2026: Wix AI, Durable, 10Web, Hostinger AI Builder, Dorik en Relume. Bouw in minuten een volledige website met AI — vergeleken op prijs, design en SEO.'
category: development
rating: 4.4
priceRange: EUR 3-60/mnd
pros:
- Vergelijking van de nieuwste AI website builders
- Realistische prijzen en features voor 2026
- Praktische keuzehulp voor Nederlandse gebruikers
cons:
- AI gegenereerde sites hebben soms beperkingen
- Prijzen kunnen wijzigen
affiliateLinks:
- https://www.beehiiv.com/?via=anonymous-operator
date: """ + today + """
modelYear: 2026
featuredTool: Wix AI Builder
readingTime: 9 min
tools:
- name: Wix AI Builder
  verdict: Meest complete AI builder met NL-taalondersteuning, e-commerce en 900+ templates
  priceRange: EUR 16-45/mnd
  bestFor: Allround & E-commerce
  rating: 4.7
  affiliateLink: https://www.wix.com/?ref=aitoolsnl
- name: Durable
  verdict: Snelste van prompt naar live site (30 seconden) — perfect voor zzp'ers en kleine bedrijven
  priceRange: EUR 15-35/mnd
  bestFor: Snelle MKB sites
  rating: 4.5
  affiliateLink: https://durable.co/?ref=aitoolsnl
- name: 10Web AI Builder
  verdict: AI bouwt op WordPress-basis met Google PageSpeed 90+ — beste voor SEO
  priceRange: EUR 12-60/mnd
  bestFor: SEO & WordPress
  rating: 4.6
  affiliateLink: https://10web.io/?ref=aitoolsnl
- name: Hostinger AI Builder
  verdict: Scherpste prijs inclusief hosting en gratis domein — onverslaanbaar voor budget
  priceRange: EUR 3-8/mnd
  bestFor: Budget & Beginners
  rating: 4.3
  affiliateLink: https://www.hostinger.nl/ai-website-builder?ref=aitoolsnl
- name: Dorik AI
  verdict: Mooiste AI-designs met CMS-functionaliteit — ideaal voor content-rijke sites
  priceRange: EUR 8-39/mnd
  bestFor: Design & Content
  rating: 4.4
  affiliateLink: https://dorik.com/?ref=aitoolsnl
- name: Relume
  verdict: AI wireframe en sitemap generator die exporteert naar Webflow/Figma — beste voor designers
  priceRange: EUR 15-49/mnd
  bestFor: Designers & Bureaus
  rating: 4.5
  affiliateLink: https://www.relume.io/?ref=aitoolsnl
- name: Pineapple Builder
  verdict: Specifiek voor personal brands en portfolio's met strakke AI-designs
  priceRange: EUR 12-30/mnd
  bestFor: Personal Branding
  rating: 4.1
  affiliateLink: https://pineapple-builder.com/?ref=aitoolsnl
related:
-
""",
    },
]

# Use gemini-2.0-flash which typically has higher rate limits
MODELS=["gemini-2.5-flash", "gemini-2.0-flash"]

def call_gemini(prompt, model_index=0):
    if model_index >= len(MODELS):
        raise Exception("All models exhausted")
    model = MODELS[model_index]
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={API_KEY}"
    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {"temperature": 0.7, "maxOutputTokens": 4096, "topP": 0.95, "topK": 40}
    }
    resp = requests.post(url, json=payload, timeout=120)
    if resp.status_code == 429 and model_index + 1 < len(MODELS):
        print(f"Rate limited on {model}, trying {MODELS[model_index+1]}...")
        time.sleep(5)
        return call_gemini(prompt, model_index + 1)
    resp.raise_for_status()
    data = resp.json()
    return data["candidates"][0]["content"]["parts"][0]["text"]

def fill_related(fm):
    import random
    related = random.sample([s for s in ALL_SLUGS if s not in [a["slug"] for a in ARTICLES]], 3)
    rel_str = "\n".join(f"- {r}" for r in related)
    return fm.replace("related:\n-", f"related:\n{rel_str}")

for i, art in enumerate(ARTICLES):
    out_path = os.path.join(ARTICLES_DIR, f"{art['slug']}.md")
    if os.path.exists(out_path) and os.path.getsize(out_path) > 1000:
        print(f"[{i+1}/2] SKIP: {art['slug']} already exists")
        continue

    print(f"[{i+1}/2] GENERATING: {art['slug']}...", end=" ", flush=True)
    try:
        body = call_gemini(art["prompt"])
        fm = fill_related(art["frontmatter"])
        full = f"{fm}\n\n{body}\n"
        with open(out_path, "w") as f:
            f.write(full)
        print(f"OK ({os.path.getsize(out_path)} bytes)")
    except Exception as e:
        print(f"FAILED: {e}")

    if i < len(ARTICLES) - 1:
        print("  Waiting 30s between articles...")
        time.sleep(30)

print("Done!")
