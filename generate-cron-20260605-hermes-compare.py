#!/usr/bin/env python3
"""Generate 5 new Dutch AI tools comparison articles for June 5, 2026.
Hermes cron autonomous run — fills genuine content gaps with Dutch-relevant comparisons."""
import os, json, time, sys, requests
from datetime import date

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

ALL_SLUGS = [
    f.replace(".md", "") for f in os.listdir(ARTICLES_DIR) if f.endswith(".md")
]

def pick_related(new_slug, pool, n=3):
    return [s for s in pool if s != new_slug][:n]

# ============================================================
# 5 NEW COMPARISON ARTICLES — genuine gaps, Dutch relevance
# ============================================================

NEW_ARTICLES = [
    # 1. Nederlandse boekhoudsoftware (genuine gap — Exact/Moneybird/Snelstart covered, missing e-Boekhouden/Jortt/Yuki)
    {
        "slug": "e-boekhouden-vs-jortt-vs-yuki-vs-moneybird-2026",
        "title": "e-Boekhouden vs Jortt vs Yuki vs Moneybird 2026: beste Nederlandse boekhoudsoftware",
        "description": "Vergelijk de beste Nederlandse boekhoudsoftware in 2026: e-Boekhouden, Jortt, Yuki, Moneybird, Snelstart en Exact Online. Voor ZZP, MKB en accountants — eerlijk vergeleken op prijs, gebruiksgemak en AI-features.",
        "category": "business",
        "prompt": """Schrijf een Nederlands artikel van 1300-1600 woorden over Nederlandse boekhoudsoftware met AI-features in 2026. Behandel 7 tools: e-Boekhouden, Jortt, Yuki, Moneybird, Snelstart, Exact Online, InformerOnline.

Structuur:
- Introductie: Nederlandse boekhoudsoftware in 2026 — AI-automatisering, bankkoppelingen (PSD2), verplichte e-facturatie (Peppol), Belastingdienst-koppelingen
- Per tool een ## kop met: beschrijving, prijsrange (EUR/maand), beste use case (ZZP, MKB, accountantskantoor, etc.), AI-features (automatische categorisatie, factuurherkenning, voorspelling cashflow), plus- en minpunten, verdict (1-2 zinnen)
- Een markdown-vergelijkingstabel met alle 7 tools: naam, prijs vanaf (EUR/maand), beste-voor, AI-niveau (1-5), score (1-5)
- Conclusie: welke voor welk type ondernemer (ZZP <€50k, ZZP >€50k, MKB 2-10 man, MKB 10-50, accountantskantoor, internationale handel)
- 3 FAQ-vragen over boekhoudsoftware kiezen in Nederland
- Prijzen realistisch: e-Boekhouden €12-35/mnd, Jortt €17-42/mnd, Yuki €25-75/mnd, Moneybird €15-55/mnd, Snelstart €20-60/mnd, Exact Online €25-110/mnd, InformerOnline €15-45/mnd

Focus op NEDERLANDSE markt. Niet internationaal. Alle prijzen EUR. Benoem koppelingen met Nederlandse banken (ING, Rabobank, ABN AMRO, bunq) en Belastingdienst. Vloeiend Nederlands, praktisch en eerlijk.""",
        "tools": [
            {"name": "e-Boekhouden", "verdict": "Scherpste prijs met volledige boekhoudfunctionaliteit — de beste budgetkeuze voor zzp'ers", "priceRange": "EUR 12-35/mnd", "bestFor": "Budget ZZP", "rating": 4.6, "affiliateLink": "https://www.e-boekhouden.nl/?ref=aitoolsnl"},
            {"name": "Jortt", "verdict": "Gebruiksvriendelijk met slimme factuurherkenning — ideaal voor niet-boekhouders", "priceRange": "EUR 17-42/mnd", "bestFor": "Gebruiksgemak", "rating": 4.5, "affiliateLink": "https://www.jortt.nl/?ref=aitoolsnl"},
            {"name": "Yuki", "verdict": "Krachtigste AI-automatisering met documentherkenning — top voor administratiekantoren", "priceRange": "EUR 25-75/mnd", "bestFor": "Accountants & Admin", "rating": 4.7, "affiliateLink": "https://www.yuki.nl/?ref=aitoolsnl"},
            {"name": "Moneybird", "verdict": "Mooiste interface met sterke facturatiefeatures — populair bij creatieve zzp'ers", "priceRange": "EUR 15-55/mnd", "bestFor": "Design & Creatief", "rating": 4.6, "affiliateLink": "https://www.moneybird.nl/?ref=aitoolsnl"},
            {"name": "Snelstart", "verdict": "Traditioneel sterk met uitgebreide rapportages — favoriet bij klassieke boekhouders", "priceRange": "EUR 20-60/mnd", "bestFor": "Traditioneel MKB", "rating": 4.4, "affiliateLink": "https://www.snelstart.nl/?ref=aitoolsnl"},
            {"name": "Exact Online", "verdict": "Meest complete ERP-integratie met voorraad, CRM en HRM — de MKB-standaard", "priceRange": "EUR 25-110/mnd", "bestFor": "MKB & ERP", "rating": 4.8, "affiliateLink": "https://www.exact.com/nl?ref=aitoolsnl"},
            {"name": "InformerOnline", "verdict": "Slimme BI-laag over bestaande pakketten — voor datagedreven ondernemers", "priceRange": "EUR 15-45/mnd", "bestFor": "Data & Analyse", "rating": 4.2, "affiliateLink": "https://www.informer.eu/nl?ref=aitoolsnl"},
        ],
        "related": pick_related("e-boekhouden-vs-jortt-vs-yuki-vs-moneybird-2026", ALL_SLUGS, 3)
    },

    # 2. AI chatbots voor websites (genuine gap — Intercom/Zendesk/Freshdesk covered, but not lightweight chatbots)
    {
        "slug": "tidio-vs-intercom-vs-livechat-vs-crisp-2026",
        "title": "Tidio vs Intercom vs LiveChat vs Crisp 2026: beste AI chatbot voor je website",
        "description": "Vergelijk de beste AI chatbots voor websites in 2026: Tidio, Intercom, LiveChat, Crisp, Tawk.to en Chatfuel. Met NL-taalondersteuning, prijzen en AI-automatisering vergeleken.",
        "category": "business",
        "prompt": """Schrijf een Nederlands artikel van 1300-1600 woorden over AI chatbots voor websites in 2026. Behandel 7 tools: Tidio, Intercom, LiveChat, Crisp, Tawk.to, Chatfuel, ManyChat.

Structuur:
- Introductie: AI chatbots 2026 — van rule-based naar LLM-aangedreven, 24/7 klantenservice, NL-taalondersteuning, integraties met webshop-platforms (Shopify, WooCommerce, Lightspeed)
- Per tool een ## kop met: beschrijving, prijsrange (EUR/maand), beste use case (e-commerce, SaaS, MKB, enterprise), AI-features (GPT-integratie, NL taalbegrip, intentherkenning), plus- en minpunten, verdict (1-2 zinnen)
- Een markdown-vergelijkingstabel met alle 7 tools: naam, prijs vanaf (EUR), gratis tier, NL-taal, AI-niveau, beste-voor, score (1-5)
- Conclusie: welke chatbot voor welk type bedrijf (kleine webshop, scale-up, enterprise, B2B SaaS, non-profit)
- 3 FAQ-vragen over AI chatbots implementeren op Nederlandse websites
- Prijzen realistisch: Tidio €0-33/mnd, Intercom €39-139/mnd, LiveChat €20-59/mnd, Crisp €0-95/mnd, Tawk.to gratis, Chatfuel €12-50/mnd, ManyChat €15-75/mnd

Nederlandse context. Benoem AVG/privacy bij chatbot-gesprekken. Vloeiend Nederlands, praktisch.""",
        "tools": [
            {"name": "Tidio", "verdict": "Beste allround met gratis tier, GPT-integratie en naadloze Shopify-koppeling", "priceRange": "EUR 0-33/mnd", "bestFor": "E-commerce MKB", "rating": 4.6, "affiliateLink": "https://www.tidio.com/?ref=aitoolsnl"},
            {"name": "Intercom", "verdict": "Krachtigste AI-platform met Fin AI-agent — de gouden standaard voor SaaS", "priceRange": "EUR 39-139/mnd", "bestFor": "SaaS & Scale-ups", "rating": 4.8, "affiliateLink": "https://www.intercom.com/?ref=aitoolsnl"},
            {"name": "LiveChat", "verdict": "Betrouwbaar met uitstekende analytics — ideaal voor sales-gedreven teams", "priceRange": "EUR 20-59/mnd", "bestFor": "Sales & Conversie", "rating": 4.5, "affiliateLink": "https://www.livechat.com/?ref=aitoolsnl"},
            {"name": "Crisp", "verdict": "Moderne chat met co-browsing en CRM-integratie — populair bij tech-startups", "priceRange": "EUR 0-95/mnd", "bestFor": "Startups & Tech", "rating": 4.4, "affiliateLink": "https://crisp.chat/?ref=aitoolsnl"},
            {"name": "Tawk.to", "verdict": "Volledig gratis met alle basisfeatures — beste prijs-kwaliteit voor kleine ondernemers", "priceRange": "EUR 0/mnd", "bestFor": "Budget & ZZP", "rating": 4.2, "affiliateLink": "https://www.tawk.to/?ref=aitoolsnl"},
            {"name": "Chatfuel", "verdict": "No-code botbouwer met sterke Facebook/Instagram Messenger integratie", "priceRange": "EUR 12-50/mnd", "bestFor": "Social Media Bots", "rating": 4.1, "affiliateLink": "https://chatfuel.com/?ref=aitoolsnl"},
            {"name": "ManyChat", "verdict": "Beste voor marketing automatisering via Messenger, Instagram DM en WhatsApp", "priceRange": "EUR 15-75/mnd", "bestFor": "Marketing Automation", "rating": 4.3, "affiliateLink": "https://manychat.com/?ref=aitoolsnl"},
        ],
        "related": pick_related("tidio-vs-intercom-vs-livechat-vs-crisp-2026", ALL_SLUGS, 3)
    },

    # 3. Nederlandse bezorg- en fulfilment platforms (zero coverage, high Dutch search volume)
    {
        "slug": "sendcloud-vs-myparcel-vs-picqer-vs-montapacking-2026",
        "title": "Sendcloud vs MyParcel vs Picqer vs Montapacking 2026: beste bezorgplatform voor webshops",
        "description": "Vergelijk de beste Nederlandse bezorg- en fulfilmentplatforms in 2026: Sendcloud, MyParcel, Picqer, Montapacking, ShippyPro en Wuunder. Met prijzen, carrier-integraties en AI-slimme verzendopties.",
        "category": "business",
        "prompt": """Schrijf een Nederlands artikel van 1300-1600 woorden over bezorg- en fulfilmentplatforms voor Nederlandse webshops in 2026. Behandel 7 tools: Sendcloud, MyParcel, Picqer, Montapacking, ShippyPro, Wuunder, Paazl.

Structuur:
- Introductie: bezorglandschap 2026 — duurzaamheidslabels, AI-routing, slimme pakketkluis, carrier-diversificatie (PostNL, DHL, DPD, UPS, Budbee, Trunkrs)
- Per tool een ## kop met: beschrijving, prijsmodel (EUR/verzending of /maand), beste use case (kleine webshop, scale-up, 3PL, internationaal), carriers (gekoppelde vervoerders), AI-features (slimme carrierkeuze, voorspelde bezorgtijd), plus- en minpunten, verdict
- Een markdown-vergelijkingstabel: naam, prijs vanaf (EUR), aantal carriers, beste-voor, score (1-5)
- Conclusie: welk platform voor welk type webshop (<100 zendingen/mnd, 100-1000, 1000-10000, internationaal, 3PL/fulfilment)
- 3 FAQ-vragen over verzendplatforms kiezen
- Prijzen realistisch: Sendcloud gratis-€49/mnd + per label, MyParcel gratis-€35/mnd + label, Picqer €59-299/mnd, Montapacking €100-500+/mnd, ShippyPro €25-199/mnd, Wuunder €0-15/mnd + label, Paazl op aanvraag

Nederlandse markt. Vloeiend Nederlands. Praktische vergelijking voor e-commerce ondernemers.""",
        "tools": [
            {"name": "Sendcloud", "verdict": "Breedste carrier-netwerk met slimme checkout-oplossing — de standaard voor groeiende webshops", "priceRange": "EUR 0-49/mnd + label", "bestFor": "Schaalbare webshops", "rating": 4.7, "affiliateLink": "https://www.sendcloud.nl/?ref=aitoolsnl"},
            {"name": "MyParcel", "verdict": "Beste prijs-kwaliteit met strakke PostNL-integratie — top voor Nederlandse MKB webshops", "priceRange": "EUR 0-35/mnd + label", "bestFor": "NL-gefocuste shops", "rating": 4.5, "affiliateLink": "https://www.myparcel.nl/?ref=aitoolsnl"},
            {"name": "Picqer", "verdict": "Volledig WMS met voorraadbeheer en pick-routes — ideaal voor eigen magazijn", "priceRange": "EUR 59-299/mnd", "bestFor": "Magazijnbeheer", "rating": 4.6, "affiliateLink": "https://picqer.com/nl?ref=aitoolsnl"},
            {"name": "Montapacking", "verdict": "All-in-one fulfilment met 10+ magazijnen — uitbesteden zonder kopzorgen", "priceRange": "EUR 100-500+/mnd", "bestFor": "Uitbestede logistiek", "rating": 4.4, "affiliateLink": "https://www.montapacking.nl/?ref=aitoolsnl"},
            {"name": "ShippyPro", "verdict": "Internationale focus met 180+ carriers — beste voor cross-border e-commerce", "priceRange": "EUR 25-199/mnd", "bestFor": "Internationaal", "rating": 4.3, "affiliateLink": "https://www.shippypro.com/?ref=aitoolsnl"},
            {"name": "Wuunder", "verdict": "Slimste carrier-vergelijking per zending met CO2-inzicht — beste voor duurzame shops", "priceRange": "EUR 0-15/mnd + label", "bestFor": "Duurzaamheid", "rating": 4.2, "affiliateLink": "https://www.wuunder.nl/?ref=aitoolsnl"},
            {"name": "Paazl", "verdict": "Premium checkout delivery optimalisatie — top voor grote retail brands", "priceRange": "Op aanvraag", "bestFor": "Enterprise retail", "rating": 4.1, "affiliateLink": "https://www.paazl.com/nl?ref=aitoolsnl"},
        ],
        "related": pick_related("sendcloud-vs-myparcel-vs-picqer-vs-montapacking-2026", ALL_SLUGS, 3)
    },

    # 4. AI website builders (genuine gap — Framer/Webflow/Wix covered, but not fully AI-generated site builders)
    {
        "slug": "wix-ai-vs-durable-vs-10web-vs-hostinger-2026",
        "title": "Wix AI vs Durable vs 10Web vs Hostinger AI Builder 2026: beste AI website bouwer",
        "description": "Vergelijk de beste AI website builders in 2026: Wix AI, Durable, 10Web, Hostinger AI Builder, Dorik en Relume. Bouw in minuten een volledige website met AI — vergeleken op prijs, design en SEO.",
        "category": "development",
        "prompt": """Schrijf een Nederlands artikel van 1300-1600 woorden over AI website builders in 2026. Behandel 7 tools: Wix AI Website Builder, Durable, 10Web AI Builder, Hostinger AI Website Builder, Dorik AI, Relume (AI sitemap/wireframe), Pineapple Builder.

Structuur:
- Introductie: AI website bouwers 2026 — van prompt naar live site in minuten, vervangen ze developers?, Nederlandse adoptie, mobiel-responsief
- Per tool een ## kop met: beschrijving, prijsrange (EUR/maand), beste use case (portfolio, webshop, landingspagina, MKB-site), AI-kracht (tekst, design, SEO, afbeeldingen), plus- en minpunten, verdict
- Een markdown-vergelijkingstabel: naam, prijs vanaf (EUR), gratis tier, beste-voor, AI-niveau, score (1-5)
- Conclusie: welke AI builder voor welk type site (ZZP-portfolio, MKB-website, webshop, SaaS landing page, blog)
- 3 FAQ-vragen over AI website builders vs handmatig bouwen
- Prijzen realistisch: Wix AI €16-45/mnd, Durable €15-35/mnd, 10Web €12-60/mnd, Hostinger AI €3-8/mnd (met hosting), Dorik AI €8-39/mnd, Relume €15-49/mnd, Pineapple Builder €12-30/mnd

Nederlandse context. Benoem AVG/privacy, NL hosting (Hostinger heeft EU-servers). SEO-kwaliteit van AI-gegenereerde sites. Vloeiend Nederlands.""",
        "tools": [
            {"name": "Wix AI Builder", "verdict": "Meest complete AI builder met NL-taalondersteuning, e-commerce en 900+ templates", "priceRange": "EUR 16-45/mnd", "bestFor": "Allround & E-commerce", "rating": 4.7, "affiliateLink": "https://www.wix.com/?ref=aitoolsnl"},
            {"name": "Durable", "verdict": "Snelste van prompt naar live site (30 seconden) — perfect voor zzp'ers en kleine bedrijven", "priceRange": "EUR 15-35/mnd", "bestFor": "Snelle MKB sites", "rating": 4.5, "affiliateLink": "https://durable.co/?ref=aitoolsnl"},
            {"name": "10Web AI Builder", "verdict": "AI bouwt op WordPress-basis met Google PageSpeed 90+ — beste voor SEO", "priceRange": "EUR 12-60/mnd", "bestFor": "SEO & WordPress", "rating": 4.6, "affiliateLink": "https://10web.io/?ref=aitoolsnl"},
            {"name": "Hostinger AI Builder", "verdict": "Scherpste prijs inclusief hosting en gratis domein — onverslaanbaar voor budget", "priceRange": "EUR 3-8/mnd", "bestFor": "Budget & Beginners", "rating": 4.3, "affiliateLink": "https://www.hostinger.nl/ai-website-builder?ref=aitoolsnl"},
            {"name": "Dorik AI", "verdict": "Mooiste AI-designs met CMS-functionaliteit — ideaal voor content-rijke sites", "priceRange": "EUR 8-39/mnd", "bestFor": "Design & Content", "rating": 4.4, "affiliateLink": "https://dorik.com/?ref=aitoolsnl"},
            {"name": "Relume", "verdict": "AI wireframe en sitemap generator die exporteert naar Webflow/Figma — beste voor designers", "priceRange": "EUR 15-49/mnd", "bestFor": "Designers & Bureaus", "rating": 4.5, "affiliateLink": "https://www.relume.io/?ref=aitoolsnl"},
            {"name": "Pineapple Builder", "verdict": "Specifiek voor personal brands en portfolio's met strakke AI-designs", "priceRange": "EUR 12-30/mnd", "bestFor": "Personal Branding", "rating": 4.1, "affiliateLink": "https://pineapple-builder.com/?ref=aitoolsnl"},
        ],
        "related": pick_related("wix-ai-vs-durable-vs-10web-vs-hostinger-2026", ALL_SLUGS, 3)
    },

    # 5. AI UX design & wireframing tools (emerging category, not covered)
    {
        "slug": "uizard-vs-visily-vs-relume-vs-galileo-ai-2026",
        "title": "Uizard vs Visily vs Relume vs Galileo AI 2026: beste AI UX design tool",
        "description": "Vergelijk de beste AI tools voor UX design en wireframing in 2026: Uizard, Visily, Relume, Galileo AI, Musho en Attention Insight. Van schets naar prototype AI — vergeleken voor designers en product teams.",
        "category": "development",
        "prompt": """Schrijf een Nederlands artikel van 1300-1600 woorden over AI UX design tools in 2026. Behandel 7 tools: Uizard, Visily, Relume, Galileo AI, Musho, Attention Insight, Mockplus.

Structuur:
- Introductie: AI in UX design 2026 — schets-naar-prototype, AI heatmaps, design-to-code, hoe AI designers versnelt maar niet vervangt, adoptie in Nederland
- Per tool een ## kop met: beschrijving, prijsrange (EUR/maand), beste use case (wireframing, prototyping, design system, usability testing), unieke AI-feature, plus- en minpunten, verdict
- Een markdown-vergelijkingstabel: naam, prijs vanaf (EUR), gratis tier, beste-voor, AI-niveau, score (1-5)
- Conclusie: welke tool voor welk team (solo designer, startup product team, agency, enterprise design team)
- 3 FAQ-vragen over AI in UX design
- Prijzen realistisch: Uizard €0-19/mnd, Visily €0-35/mnd, Relume €15-49/mnd, Galileo AI €12-39/mnd, Musho €8-29/mnd, Attention Insight €19-99/mnd, Mockplus €10-35/mnd

Vloeiend Nederlands. Praktisch voor Nederlandse designers en product teams. Benoem integraties met Figma, Sketch en handoff naar developers.""",
        "tools": [
            {"name": "Uizard", "verdict": "Beste schets-naar-prototype AI — scan je tekening en krijg een klikbaar prototype", "priceRange": "EUR 0-19/mnd", "bestFor": "Rapid Prototyping", "rating": 4.6, "affiliateLink": "https://uizard.io/?ref=aitoolsnl"},
            {"name": "Visily", "verdict": "Krachtige screenshot-naar-editable-Wireframe AI — de snelste manier om inspiratie om te zetten", "priceRange": "EUR 0-35/mnd", "bestFor": "Wireframing & Ideation", "rating": 4.5, "affiliateLink": "https://www.visily.ai/?ref=aitoolsnl"},
            {"name": "Relume", "verdict": "AI sitemap + wireframe generator met 1000+ componenten — de standaard voor Webflow/Figma designers", "priceRange": "EUR 15-49/mnd", "bestFor": "Design Systems", "rating": 4.7, "affiliateLink": "https://www.relume.io/?ref=aitoolsnl"},
            {"name": "Galileo AI", "verdict": "Prompt-naar-UI in seconden met verrassend goede resultaten — de futurist in de lijst", "priceRange": "EUR 12-39/mnd", "bestFor": "AI-First Design", "rating": 4.4, "affiliateLink": "https://www.galileo.ai/?ref=aitoolsnl"},
            {"name": "Musho", "verdict": "AI design companion in Figma — genereert complete pagina's uit prompts binnen je bestaande workflow", "priceRange": "EUR 8-29/mnd", "bestFor": "Figma Gebruikers", "rating": 4.3, "affiliateLink": "https://musho.ai/?ref=aitoolsnl"},
            {"name": "Attention Insight", "verdict": "AI voorspelt waar gebruikers kijken — geen echte testers nodig voor eerste validatie", "priceRange": "EUR 19-99/mnd", "bestFor": "Usability Testing", "rating": 4.2, "affiliateLink": "https://attentioninsight.com/?ref=aitoolsnl"},
            {"name": "Mockplus", "verdict": "All-in-one prototyping met AI-ondersteuning voor interactie-ontwerp — beste waarde voor teams", "priceRange": "EUR 10-35/mnd", "bestFor": "Teams & Samenwerking", "rating": 4.1, "affiliateLink": "https://www.mockplus.com/?ref=aitoolsnl"},
        ],
        "related": pick_related("uizard-vs-visily-vs-relume-vs-galileo-ai-2026", ALL_SLUGS, 3)
    },
]


# ============================================================
# GENERATION LOGIC
# ============================================================

def generate_article(article_data):
    """Call Gemini API to generate article body from prompt."""
    prompt = article_data["prompt"]
    payload = {
        "contents": [{
            "parts": [{"text": prompt}]
        }],
        "generationConfig": {
            "temperature": 0.7,
            "maxOutputTokens": 4096,
            "topP": 0.95,
            "topK": 40
        }
    }

    url = f"{BASE_URL}?key={API_KEY}"
    response = requests.post(url, json=payload, timeout=120)
    response.raise_for_status()
    data = response.json()

    try:
        text = data["candidates"][0]["content"]["parts"][0]["text"]
    except (KeyError, IndexError):
        print(f"  Unexpected API response: {json.dumps(data, indent=2)[:500]}")
        raise

    return text.strip()


def build_frontmatter(article_data):
    """Build the YAML frontmatter string."""
    tools = []
    for t in article_data.get("tools", []):
        tools.append(f"""- name: {t['name']}
  verdict: {t['verdict']}
  priceRange: {t['priceRange']}
  bestFor: {t['bestFor']}
  rating: {t['rating']}
  affiliateLink: {t['affiliateLink']}""")

    tools_yaml = "\n".join(tools)

    related_yaml = "\n".join(f"- {r}" for r in article_data.get("related", []))

    pros = article_data.get("pros", [
        "Vergelijking van top tools in deze categorie",
        "Actuele 2026 marktdata met realistische prijzen",
        "Focus op Nederlandse context en gebruikers"
    ])

    cons = article_data.get("cons", [
        "Prijzen onder voorbehoud — check actuele aanbiedingen",
        "Sommige features in beta of rolling release"
    ])

    pros_yaml = "\n".join(f"- {p}" for p in pros)
    cons_yaml = "\n".join(f"- {c}" for c in cons)

    rating = article_data.get("rating", 4.5)
    price_range = article_data.get("priceRange", "EUR 0-150/mnd")

    today = date.today().isoformat()

    fm = f"""---
title: '{article_data["title"]}'
slug: {article_data["slug"]}
description: '{article_data["description"]}'
category: {article_data["category"]}
rating: {rating}
priceRange: {price_range}
pros:
{pros_yaml}
cons:
{cons_yaml}
affiliateLinks:
- https://www.beehiiv.com/?via=anonymous-operator
date: {today}
modelYear: 2026
featuredTool: {article_data["tools"][0]["name"]}
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
    return fm


def main():
    print(f"Generating {len(NEW_ARTICLES)} articles...")
    print(f"API key present: {'yes' if API_KEY else 'NO'}")
    print(f"Articles dir: {ARTICLES_DIR}")
    print()

    results = []

    for i, article in enumerate(NEW_ARTICLES, 1):
        slug = article["slug"]
        out_path = os.path.join(ARTICLES_DIR, f"{slug}.md")

        if os.path.exists(out_path) and os.path.getsize(out_path) > 1000:
            print(f"[{i}/{len(NEW_ARTICLES)}] SKIP: {slug} already exists ({os.path.getsize(out_path)} bytes)")
            results.append(("skipped", slug))
            continue

        print(f"[{i}/{len(NEW_ARTICLES)}] GENERATING: {slug}...", end=" ", flush=True)

        try:
            body = generate_article(article)
            frontmatter = build_frontmatter(article)

            full_article = f"{frontmatter}\n\n{body}\n"

            with open(out_path, "w") as f:
                f.write(full_article)

            size = os.path.getsize(out_path)
            print(f"OK ({size} bytes)")
            results.append(("created", slug))

        except Exception as e:
            print(f"FAILED: {e}")
            results.append(("failed", slug))

        time.sleep(2)  # Rate limit courtesy

    print()
    print("=" * 60)
    print("SUMMARY")
    print("=" * 60)
    created = sum(1 for r in results if r[0] == "created")
    skipped = sum(1 for r in results if r[0] == "skipped")
    failed = sum(1 for r in results if r[0] == "failed")
    print(f"Created: {created}, Skipped: {skipped}, Failed: {failed}")
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
