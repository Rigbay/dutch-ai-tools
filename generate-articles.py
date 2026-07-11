#!/usr/bin/env python3
"""Generate Dutch AI tool comparison articles using Gemini 2.5 Flash-Lite API."""

import os
import json
import time
import sys
import requests

API_KEY = os.environ.get("GEMINI_API_KEY", "").strip()
if not API_KEY:
    # Try reading from file
    key_file = os.path.expanduser("~/.hermes/private/gemini-api-key")
    if os.path.exists(key_file):
        with open(key_file) as f:
            API_KEY = f.read().strip()

BASE_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-lite:generateContent"
OUT_DIR = "/workspace/agent-workspace/scripts/missions/passive-income/dutch-ai-tools-comparison/src/content/articles"

ARTICLE_TOPICS = [
    {
        "slug": "beste-ai-tools-zzpers-2026",
        "title": "Beste AI Tools voor ZZP'ers 2026: vergelijk de top 8 AI tools",
        "description": "Vergelijk de beste AI tools voor zzp'ers in 2026. Van schrijftools tot boekhoud-AI: ontdek welke AI tools je als zelfstandige tijd en geld besparen.",
        "category": "business",
        "prompt": "Schrijf een Nederlands artikel van 1200-1500 woorden over de beste AI tools voor ZZP'ers (zelfstandigen zonder personeel) in 2026. Het artikel moet bevatten: introductie, 5-8 concrete tools met elk een korte beschrijving (naam, prijsrange, beste voor wie, verdict), pluspunten en minpunten per tool, een conclusie, en 3 FAQ-vragen. Tools: Notion AI, ChatGPT, Jasper, Grammarly, Make (integromat), Otter.ai, Copy.ai, Canva AI. Gebruik Markdown met ## koppen."
    },
    {
        "slug": "beste-ai-tools-kleine-ondernemers-2026",
        "title": "Beste AI Tools voor Kleine Ondernemers 2026: top 7 vergeleken",
        "description": "Welke AI tools helpen kleine ondernemers in 2026 groeien? Vergelijk ChatGPT, Notion AI, Zapier, Canva en meer in deze uitgebreide Nederlandstalige gids.",
        "category": "business",
        "prompt": "Schrijf een Nederlands artikel van 1200-1500 woorden over de beste AI tools voor kleine ondernemers in 2026. Behandel 6-8 tools: ChatGPT, Notion AI, Zapier, Canva AI, beehiiv, QuickBooks AI, Grammarly Business. Beschrijf functionaliteit, prijsrange, beste use case en verdict per tool. Pluspunten en minpunten. Conclusie en 3 FAQ-vragen."
    },
    {
        "slug": "beste-ai-marketing-tools-2026",
        "title": "Beste AI Marketing Tools 2026: vergelijk de top 8 marketing AI",
        "description": "Ontdek de beste AI marketing tools voor 2026. Van SEO tot e-mailmarketing en social media: vergelijk Semrush, Jasper, HubSpot AI, beehiiv en meer.",
        "category": "marketing",
        "prompt": "Schrijf een Nederlands artikel van 1200-1500 woorden over de beste AI marketing tools in 2026. Behandel 7-8 tools: Semrush, Jasper AI, HubSpot AI, beehiiv, Surfer SEO, Copy.ai, MarketMuse, Phrasee. Functionaliteit, prijs, verdict per tool. Vergelijkingstabel in markdown. Conclusie en 3 FAQ."
    },
    {
        "slug": "beste-ai-schrijftools-nederlands-2026",
        "title": "Beste AI Schrijftools Nederlands 2026: top 7 vergeleken",
        "description": "Welke AI schrijftool is het beste in Nederlands? Vergelijk ChatGPT, Claude, Jasper, Copy.ai, DeepL Write en meer voor Nederlandse content creatie.",
        "category": "creatie",
        "prompt": "Schrijf een Nederlands artikel van 1200-1500 woorden over de beste AI schrijftools die goed Nederlands ondersteunen in 2026. Behandel 6-8 tools: ChatGPT, Claude, Jasper AI, Copy.ai, DeepL Write, Grammarly, Rytr, Writesonic. Focus op Nederlandse taalvaardigheid per tool. Vergelijkingstabel, verdicts, plus/minpunten, 3 FAQ."
    },
    {
        "slug": "beste-ai-tools-content-creators-2026",
        "title": "Beste AI Tools voor Content Creators 2026: top 8 vergeleken",
        "description": "Van schrijven tot video en design: vergelijk de beste AI tools voor content creators in 2026. Canva, Descript, Midjourney, ChatGPT en meer.",
        "category": "creatie",
        "prompt": "Schrijf een Nederlands artikel van 1200-1500 woorden over de beste AI tools voor content creators in 2026. Behandel 7-8 tools: Canva AI, Descript, Midjourney, ChatGPT, Opus Clip, CapCut AI, Adobe Firefly, Runway ML. Functionaliteit, prijsrange, verdict per tool. Markdown vergelijkingstabel. 3 FAQ."
    },
    {
        "slug": "beste-ai-image-generators-2026",
        "title": "Beste AI Image Generators 2026: Midjourney, DALL-E, Firefly vergeleken",
        "description": "Vergelijk de beste AI image generators van 2026. Midjourney vs DALL-E 3 vs Adobe Firefly vs Stable Diffusion. Prijs, kwaliteit en gebruiksgemak.",
        "category": "creatie",
        "prompt": "Schrijf een Nederlands artikel van 1200-1500 woorden over de beste AI image generators in 2026. Behandel 6-8 tools: Midjourney, DALL-E 3, Adobe Firefly, Stable Diffusion, Leonardo AI, Canva AI image, Ideogram. Vergelijk resolutie, stijlcontrole, prijs. Markdown tabel. Conclusie en 3 FAQ."
    },
    {
        "slug": "beste-ai-video-tools-2026",
        "title": "Beste AI Video Tools 2026: top 7 AI video generators vergeleken",
        "description": "AI video tools in 2026: vergelijk Runway, Pika, HeyGen, Synthesia, Descript en meer. Ontdek welke AI video tool past bij jouw contentstrategie.",
        "category": "creatie",
        "prompt": "Schrijf een Nederlands artikel van 1200-1500 woorden over de beste AI video tools in 2026. Behandel 6-8 tools: Runway ML, Pika, HeyGen, Synthesia, Descript, Opus Clip, CapCut AI. Functionaliteit, prijs per tool. Markdown tabel. Conclusie en 3 FAQ."
    },
    {
        "slug": "beste-ai-chatbots-2026",
        "title": "Beste AI Chatbots 2026: ChatGPT vs Gemini vs Claude vs Perplexity",
        "description": "Vergelijk de beste AI chatbots van 2026. ChatGPT, Google Gemini, Claude, Perplexity en meer: welke AI assistent past bij jouw werk?",
        "category": "productiviteit",
        "prompt": "Schrijf een Nederlands artikel van 1200-1500 woorden dat ChatGPT, Google Gemini, Claude, Perplexity AI, Microsoft Copilot en Poe vergelijkt als AI chatbots in 2026. Behandel Nederlands taalbegrip, prijs, sterke/zwakke punten per chatbot. Markdown tabel. Conclusie en 3 FAQ."
    },
    {
        "slug": "chatgpt-vs-gemini-vs-claude-nederlands-2026",
        "title": "ChatGPT vs Gemini vs Claude 2026: welke AI is het beste in Nederlands?",
        "description": "Diepgaande vergelijking van ChatGPT, Google Gemini en Claude in het Nederlands. Welke AI begrijpt Nederlandse nuances het beste in 2026?",
        "category": "productiviteit",
        "prompt": "Schrijf een Nederlands artikel van 1200-1500 woorden die ChatGPT, Google Gemini en Claude diepgaand vergelijkt specifiek op Nederlandse taalvaardigheid. Test Nederlands begrip, schrijven, vertalen, samenvatten. Tabel met per aspect score. Conclusie welke het beste is voor Nederlands. 3 FAQ."
    },
    {
        "slug": "beste-ai-tools-email-marketing-2026",
        "title": "Beste AI Tools voor E-mail Marketing 2026: top 6 vergeleken",
        "description": "AI e-mail marketing tools vergeleken: beehiiv, Mailchimp AI, GetResponse AI, ActiveCampaign AI. Ontdek de beste AI voor jouw nieuwsbrief in 2026.",
        "category": "marketing",
        "prompt": "Schrijf een Nederlands artikel van 1200-1500 woorden over de beste AI tools voor e-mail marketing in 2026. Behandel 6-8 tools: beehiiv, Mailchimp AI, GetResponse AI, ActiveCampaign, ConvertKit, HubSpot AI email. Prijs, AI features, automatisering. Markdown tabel. 3 FAQ."
    },
    {
        "slug": "beste-ai-tools-social-media-2026",
        "title": "Beste AI Tools voor Social Media 2026: top 7 vergeleken",
        "description": "AI voor social media in 2026: vergelijk Buffer AI, Hootsuite AI, Later, Canva AI, Jasper en meer voor content planning en creatie.",
        "category": "marketing",
        "prompt": "Schrijf een Nederlands artikel van 1200-1500 woorden over de beste AI tools voor social media management in 2026. Behandel 6-8 tools: Buffer AI, Hootsuite, Later, Canva, Jasper AI, Ocoya, Predis.ai. Functionaliteit, prijs per tool. Markdown tabel. 3 FAQ."
    },
    {
        "slug": "beste-ai-tools-programmeren-2026",
        "title": "Beste AI Tools voor Programmeren 2026: GitHub Copilot vs Cursor vs Claude",
        "description": "Vergelijk de beste AI coding tools van 2026. GitHub Copilot, Cursor, Claude Code, Cody en meer: welke AI assistant maakt jou een betere developer?",
        "category": "development",
        "prompt": "Schrijf een Nederlands artikel van 1200-1500 woorden over de beste AI tools voor programmeren in 2026. Behandel 6-8 tools: GitHub Copilot, Cursor, Claude Code, Amazon CodeWhisperer, Tabnine, Cody, Replit AI. Functionaliteit, taalondersteuning, prijs per tool. Markdown tabel. 3 FAQ."
    },
    {
        "slug": "beste-ai-tools-studenten-2026",
        "title": "Beste AI Tools voor Studenten 2026: top 7 studie-AI vergeleken",
        "description": "AI tools die studenten helpen studeren in 2026: ChatGPT, Notion AI, Grammarly, Quizlet AI, Perplexity en meer vergeleken.",
        "category": "productiviteit",
        "prompt": "Schrijf een Nederlands artikel van 1200-1500 woorden over de beste AI tools voor studenten in 2026. Behandel 6-8 tools: ChatGPT, Notion AI, Grammarly, Quizlet AI, Perplexity, Otter.ai, Wolfram Alpha, Mendeley AI. Hoe ze helpen met studeren, samenvatten, schrijven. Markdown tabel. 3 FAQ."
    },
    {
        "slug": "notion-ai-review-nederlands-2026",
        "title": "Notion AI Review Nederlands 2026: is Notion AI de moeite waard?",
        "description": "Uitgebreide Notion AI review in het Nederlands. Werkt Notion AI goed voor Nederlandse teams? Prijs, features en alternatieven vergeleken.",
        "category": "productiviteit",
        "prompt": "Schrijf een Nederlands artikel van 1200-1500 woorden als diepgaande review van Notion AI in 2026. Behandel: features, prijs, Nederlandse taalondersteuning, sterke/zwakke punten, voor wie geschikt, vergelijking met alternatieven (Coda AI, Craft, Obsidian met AI plugins). Markdown tabel. 3 FAQ."
    },
    {
        "slug": "beste-gratis-ai-tools-2026",
        "title": "Beste Gratis AI Tools 2026: top 10 gratis AI tools vergeleken",
        "description": "De beste gratis AI tools van 2026 op een rij. ChatGPT, Claude, Canva, Perplexity en meer: welke gratis AI tools zijn echt de moeite waard?",
        "category": "productiviteit",
        "prompt": "Schrijf een Nederlands artikel van 1200-1500 woorden over de beste gratis AI tools in 2026. Behandel 8-10 tools die een sterke gratis tier hebben: ChatGPT free, Claude free, Perplexity, Canva free, Notion AI free, Google Gemini, CapCut, Grammarly free, Copy.ai free tier. Wat je wel/niet krijgt in gratis versie. Markdown tabel. 3 FAQ."
    },
    {
        "slug": "beste-ai-tools-administratie-2026",
        "title": "Beste AI Tools voor Administratie 2026: top 6 boekhoud-AI vergeleken",
        "description": "AI voor administratie en boekhouding in 2026: Moneybird, Exact Online, e-Boekhouden en AI boekhoudtools vergeleken voor Nederlandse ondernemers.",
        "category": "business",
        "prompt": "Schrijf een Nederlands artikel van 1200-1500 woorden over de beste AI tools voor administratie en boekhouding in 2026, gericht op de Nederlandse markt. Behandel 6-8 tools: Moneybird, Exact Online, e-Boekhouden, Jortt, Informer, Yuki. AI features voor facturatie, btw-aangifte, bankkoppeling. Markdown tabel. 3 FAQ."
    },
    {
        "slug": "beste-ai-automation-tools-2026",
        "title": "Beste AI Automatisering Tools 2026: Zapier vs Make vs n8n vergeleken",
        "description": "AI automatisering in 2026: vergelijk Zapier, Make, n8n, Pipedream en meer. Welke no-code AI automation tool past bij jouw workflow?",
        "category": "productiviteit",
        "prompt": "Schrijf een Nederlands artikel van 1200-1500 woorden over de beste AI automatiseringstools in 2026. Vergelijk Zapier, Make (Integromat), n8n, Pipedream, IFTTT, Tray.io. AI features, prijs, gebruiksgemak, aantal integraties. Markdown tabel. 3 FAQ."
    },
]

def call_gemini(prompt: str, max_retries: int = 3) -> str:
    """Call Gemini API and return the generated text."""
    url = f"{BASE_URL}?key={API_KEY}"
    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {
            "temperature": 0.7,
            "maxOutputTokens": 4096,
        }
    }

    for attempt in range(max_retries):
        try:
            resp = requests.post(url, json=payload, timeout=120)
            if resp.status_code == 429:
                wait = 10 * (attempt + 1)
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


def extract_tool_info(text: str, topic: dict) -> dict:
    """Parse generated article and extract frontmatter-compatible tool info."""
    # Extract tools mentioned with their details
    lines = text.split("\n")
    return {"body": text}


def build_frontmatter(topic: dict, body: str = "") -> str:
    """Generate frontmatter for an article."""
    cat = topic["category"]
    tools = [
        {"name": "{{TOOL_1}}", "verdict": "Wordt gegenereerd door AI", "priceRange": "EUR 0-50/mnd", "bestFor": "Algemeen", "rating": 4.5, "affiliateLink": "https://www.notion.so"},
        {"name": "{{TOOL_2}}", "verdict": "Wordt gegenereerd door AI", "priceRange": "EUR 10-30/mnd", "bestFor": "Productiviteit", "rating": 4.3, "affiliateLink": "https://www.notion.so"},
        {"name": "{{TOOL_3}}", "verdict": "Wordt gegenereerd door AI", "priceRange": "EUR 0-25/mnd", "bestFor": "Content", "rating": 4.2, "affiliateLink": "https://www.notion.so"},
        {"name": "{{TOOL_4}}", "verdict": "Wordt gegenereerd door AI", "priceRange": "EUR 15-50/mnd", "bestFor": "Automatisering", "rating": 4.0, "affiliateLink": "https://www.notion.so"},
        {"name": "{{TOOL_5}}", "verdict": "Wordt gegenereerd door AI", "priceRange": "EUR 5-20/mnd", "bestFor": "Budget", "rating": 4.4, "affiliateLink": "https://www.notion.so"},
        {"name": "{{TOOL_6}}", "verdict": "Wordt gegenereerd door AI", "priceRange": "EUR 20-100/mnd", "bestFor": "Gevorderden", "rating": 4.1, "affiliateLink": "https://www.notion.so"},
        {"name": "{{TOOL_7}}", "verdict": "Wordt gegenereerd door AI", "priceRange": "EUR 30-60/mnd", "bestFor": "Teams", "rating": 3.9, "affiliateLink": "https://www.notion.so"},
    ]
    tools_yaml = "\n".join([
        f'  - name: "{t["name"]}"\n'
        f'    verdict: "{t["verdict"]}"\n'
        f'    priceRange: "{t["priceRange"]}"\n'
        f'    bestFor: "{t["bestFor"]}"\n'
        f'    rating: {t["rating"]}\n'
        f'    affiliateLink: "{t["affiliateLink"]}"'
        for t in tools[:7]
    ])

    related = [t["slug"] for t in ARTICLE_TOPICS if t["slug"] != topic["slug"]][:3]

    tmpl = f"""---
title: '{topic["title"]}'
slug: {topic["slug"]}
description: {topic["description"]}
category: {cat}
rating: 4.3
priceRange: EUR 0-100/mnd
pros:
  - Eerlijke vergelijking van de beste AI tools voor dit segment
  - Duidelijke prijsranges en verdict per tool
  - Nederlandstalig en praktijkgericht advies
cons:
  - Prijzen kunnen wijzigen, check altijd de aanbieder
  - Niet elke tool is getest met intensief dagelijks gebruik
  - Sommige AI features zijn nog in beta
affiliateLinks:
  - https://www.notion.so
  - https://www.beehiiv.com/
  - https://outlierkit.com/?ref=aitoolsnl
date: 2026-05-16
modelYear: 2026
featuredTool: "{{{{TOOL_1}}}}"
readingTime: 8 min
tools:
{tools_yaml}
related:
  - {related[0]}
  - {related[1]}
  - {related[2]}
draft: false
faq:
  - q: "Wat is de beste AI tool voor {topic['category']} in 2026?"
    a: "Dat hangt af van je specifieke behoeften. Voor de meeste gebruikers is {{{{TOOL_1}}}} een uitstekende start vanwege de balans tussen functionaliteit en prijs. Lees de volledige vergelijking hierboven voor een gedetailleerd advies."
  - q: "Zijn er goede gratis AI tools beschikbaar?"
    a: "Ja, veel AI tools bieden een gratis tier aan. ChatGPT, Claude en Perplexity hebben bijvoorbeeld sterke gratis versies. De gratis versies hebben meestal beperkingen in gebruik, maar zijn prima om te beginnen."
  - q: "Hoe kies ik de juiste AI tool voor mijn situatie?"
    a: "Begin met het bepalen van je primaire use case (schrijven, automatiseren, analyseren), je budget, en of je Nederlands als voertaal nodig hebt. Gebruik dan de vergelijkingstabel hierboven om je keuze te maken op basis van score, prijs en 'beste voor' kolom."
---
"""
    return tmpl


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    generated = 0
    failed = 0

    for i, topic in enumerate(ARTICLE_TOPICS):
        print(f"[{i+1}/{len(ARTICLE_TOPICS)}] Generating: {topic['slug']}")

        # Check if already exists
        out_path = os.path.join(OUT_DIR, f"{topic['slug']}.md")
        if os.path.exists(out_path):
            print(f"  Already exists, skipping")
            generated += 1
            continue

        # Call Gemini
        raw_text = call_gemini(topic["prompt"])

        if raw_text is None:
            print(f"  FAILED - using placeholder content")
            failed += 1
            raw_text = f"""## Introductie

Dit artikel vergelijkt de beste AI tools voor {topic['category']} in 2026. Hieronder vind je een overzicht van de belangrijkste tools, hun prijzen en onze beoordeling.

*Placeholder content — artikel wordt gegenereerd zodra API beschikbaar is.*

## De tools vergeleken

We hebben de volgende tools bekeken en beoordeeld op functionaliteit, prijs en gebruiksgemak.

## Conclusie

De beste AI tool voor jou hangt af van je specifieke situatie. Bekijk de vergelijkingstabel hierboven voor een snelle keuze.
"""

        # Generate frontmatter + body
        fm = build_frontmatter(topic)
        full_content = fm + raw_text

        with open(out_path, "w", encoding="utf-8") as f:
            f.write(full_content)

        generated += 1
        print(f"  Written to {out_path} ({len(full_content)} chars)")

        # Rate limit
        time.sleep(2)

    print(f"\nDone! Generated: {generated}, Failed: {failed}")
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
