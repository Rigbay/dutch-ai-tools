#!/usr/bin/env python3
"""Generate remaining 4 Dutch AI Tools articles via Ollama (qwen3.5:9b).
Cron job: 2026-07-10 — Hermes autonomous session, Gemini quota exhausted.
"""

import json, time, re, sys
from pathlib import Path
import requests

REPO = Path("/workspace/kieskeuken/dutch-ai-tools")
ARTICLES_DIR = REPO / "src/content/articles"
OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "qwen3.5:9b"

TOPICS = [
    {
        "slug": "ai-tools-kennisbanken-faq-2026",
        "title": "Beste AI Tools voor Kennisbanken & FAQ 2026: top 7 vergeleken",
        "description": "Vergelijk de 7 beste AI tools voor kennisbanken, FAQ-pagina's en self-service documentatie in 2026. Van Notion AI tot Helpjuice — welke kennisbank past bij jouw organisatie?",
        "category": "business",
        "tools": [
            {"name": "Notion AI", "verdict": "Flexibele kennisbank met AI search en automatische organisatie", "priceRange": "EUR 10-18/mnd per gebruiker", "bestFor": "Startups & teams", "rating": 4.6, "affiliateLink": "https://www.notion.so/"},
            {"name": "Helpjuice", "verdict": "Speciaal gebouwde kennisbank met AI-powered search en analytics", "priceRange": "EUR 120-290/mnd", "bestFor": "Klantenservice teams", "rating": 4.5, "affiliateLink": "https://helpjuice.com/"},
            {"name": "Document360", "verdict": "AI knowledge base voor productdocumentatie en developer portals", "priceRange": "EUR 99-399/mnd", "bestFor": "SaaS bedrijven", "rating": 4.4, "affiliateLink": "https://document360.com/"},
            {"name": "Guru", "verdict": "AI kennisbeheer dat integreert met Slack, Teams en browser", "priceRange": "EUR 10-20/mnd per gebruiker", "bestFor": "Remote teams", "rating": 4.3, "affiliateLink": "https://www.getguru.com/"},
            {"name": "Confluence AI", "verdict": "Enterprise wiki met Atlassian-integratie en AI search", "priceRange": "EUR 6-12/mnd per gebruiker", "bestFor": "Grote organisaties", "rating": 4.2, "affiliateLink": "https://www.atlassian.com/software/confluence"},
            {"name": "Slab", "verdict": "Moderne kennisbank met AI suggesties en strak design", "priceRange": "EUR 8-15/mnd per gebruiker", "bestFor": "Tech teams", "rating": 4.3, "affiliateLink": "https://slab.com/"},
            {"name": "Tettra", "verdict": "Eenvoudige AI kennisbank voor kleine teams — snel opgezet", "priceRange": "EUR 8-16/mnd per gebruiker", "bestFor": "Kleine teams", "rating": 4.1, "affiliateLink": "https://tettra.com/"},
        ],
        "related": ["confluence-vs-notion-vs-slab-2026", "beste-ai-tools-voor-klantenservice-2026", "beste-ai-chatbots-klantenservice-2026"],
    },
    {
        "slug": "ai-tools-netwerk-monitoring-2026",
        "title": "Beste AI Tools voor Netwerk Monitoring 2026: top 7 vergeleken",
        "description": "Vergelijk de 7 beste AI-gedreven netwerk monitoring tools in 2026. Van Datadog tot PRTG — welke netwerk monitor past bij jouw IT-infrastructuur in Nederland?",
        "category": "technologie",
        "tools": [
            {"name": "Datadog NPM", "verdict": "Beste AI-gedreven netwerk monitoring met volledige stack visibility", "priceRange": "EUR 5-15/host/mnd", "bestFor": "DevOps teams", "rating": 4.7, "affiliateLink": "https://www.datadoghq.com/"},
            {"name": "PRTG", "verdict": "All-in-one netwerk monitor met AI alerts — populair in Nederland", "priceRange": "EUR 1.750-15.000/jaar", "bestFor": "MKB IT-beheer", "rating": 4.5, "affiliateLink": "https://www.paessler.com/prtg"},
            {"name": "LogicMonitor", "verdict": "SaaS netwerk monitoring met AIOps en automatische root cause analysis", "priceRange": "EUR 15-25/device/mnd", "bestFor": "Managed service providers", "rating": 4.4, "affiliateLink": "https://www.logicmonitor.com/"},
            {"name": "SolarWinds NPM", "verdict": "Uitgebreide netwerk monitoring met AI-detectie van afwijkingen", "priceRange": "EUR 1.500-10.000/jaar", "bestFor": "Enterprise IT", "rating": 4.3, "affiliateLink": "https://www.solarwinds.com/"},
            {"name": "Zabbix", "verdict": "Open-source netwerk monitoring met AI anomaly detection — gratis", "priceRange": "EUR 0 (open source)", "bestFor": "Budget-bewuste teams", "rating": 4.2, "affiliateLink": "https://www.zabbix.com/"},
            {"name": "Checkmk", "verdict": "Hybride IT monitoring met AI forecasting — sterk in Europa", "priceRange": "EUR 0-60/device/mnd", "bestFor": "Hybride omgevingen", "rating": 4.3, "affiliateLink": "https://checkmk.com/"},
            {"name": "Auvik", "verdict": "Cloud-based netwerk monitoring specifiek voor MSP's met AI insights", "priceRange": "EUR 10-20/device/mnd", "bestFor": "MSP's & IT-dienstverleners", "rating": 4.4, "affiliateLink": "https://www.auvik.com/"},
        ],
        "related": ["datadog-vs-grafana-vs-new-relic-vs-dynatrace-2026", "beste-ai-tools-voor-cloud-infrastructuur-2026", "beste-ai-tools-voor-devops-platform-engineering-2026"],
    },
    {
        "slug": "ai-tools-digitale-toegankelijkheid-2026",
        "title": "Beste AI Tools voor Digitale Toegankelijkheid (WCAG) 2026: top 7 vergeleken",
        "description": "Vergelijk de 7 beste AI tools voor digitale toegankelijkheid en WCAG-compliance in 2026. Van accessiBe tot Siteimprove — welke accessibility tool maakt jouw website écht inclusief?",
        "category": "development",
        "tools": [
            {"name": "accessiBe", "verdict": "AI-gedreven toegankelijkheidsoplossing met automatische WCAG 2.2 fixes", "priceRange": "EUR 49-349/mnd", "bestFor": "MKB websites", "rating": 4.3, "affiliateLink": "https://accessibe.com/"},
            {"name": "Siteimprove", "verdict": "Enterprise accessibility platform met AI audits en prioritering", "priceRange": "EUR 500-2.000/mnd", "bestFor": "Grote organisaties", "rating": 4.5, "affiliateLink": "https://www.siteimprove.com/"},
            {"name": "Deque axe", "verdict": "Developer-first accessibility testing met axe-core en axe Auditor", "priceRange": "EUR 0-150/mnd", "bestFor": "Development teams", "rating": 4.6, "affiliateLink": "https://www.deque.com/axe/"},
            {"name": "WAVE", "verdict": "Gratis accessibility evaluatie tool van WebAIM — snel en visueel", "priceRange": "EUR 0 (gratis)", "bestFor": "Snelle checks", "rating": 4.2, "affiliateLink": "https://wave.webaim.org/"},
            {"name": "Monsido", "verdict": "All-in-one web governance met AI accessibility scanning", "priceRange": "EUR 100-500/mnd", "bestFor": "Overheid & onderwijs", "rating": 4.3, "affiliateLink": "https://monsido.com/"},
            {"name": "AudioEye", "verdict": "Hybride AI + handmatige accessibility oplossing met juridische garantie", "priceRange": "EUR 50-500/mnd", "bestFor": "Risicomijdende organisaties", "rating": 4.1, "affiliateLink": "https://www.audioeye.com/"},
            {"name": "EqualWeb", "verdict": "AI accessibility widget met automatische WCAG 2.2 compliance", "priceRange": "EUR 39-199/mnd", "bestFor": "E-commerce", "rating": 4.0, "affiliateLink": "https://www.equalweb.com/"},
        ],
        "related": ["beste-ai-tools-voor-webdesign-website-bouwen-2026", "beste-ai-tools-voor-frontend-web-development-2026", "beste-ai-tools-voor-ux-design-user-research-2026"],
    },
    {
        "slug": "ai-tools-klachtenmanagement-2026",
        "title": "Beste AI Tools voor Klachtenmanagement & Reviews 2026: top 7 vergeleken",
        "description": "Vergelijk de 7 beste AI tools voor klachtenmanagement, review monitoring en customer feedback in 2026. Van Trustpilot tot Zendesk QA — welke tool helpt jouw bedrijf klachten slim afhandelen?",
        "category": "business",
        "tools": [
            {"name": "Trustpilot", "verdict": "Grootste reviewplatform met AI sentiment analyse en automatische responses", "priceRange": "EUR 259-599/mnd", "bestFor": "Reputatiemanagement", "rating": 4.5, "affiliateLink": "https://www.trustpilot.com/"},
            {"name": "Zendesk QA", "verdict": "AI quality assurance voor klantenservice — automatische gespreksanalyse", "priceRange": "EUR 55-150/agent/mnd", "bestFor": "Klantenservice teams", "rating": 4.4, "affiliateLink": "https://www.zendesk.com/"},
            {"name": "BirdEye (Birdeye)", "verdict": "All-in-one reputatie- en klachtenmanagement met AI automation", "priceRange": "EUR 299-599/mnd", "bestFor": "Multi-location bedrijven", "rating": 4.3, "affiliateLink": "https://birdeye.com/"},
            {"name": "Klantenvertellen", "verdict": "Nederlands reviewplatform met AI-gedreven feedback analyse", "priceRange": "EUR 99-299/mnd", "bestFor": "Nederlandse MKB", "rating": 4.2, "affiliateLink": "https://www.klantenvertellen.nl/"},
            {"name": "ReviewTrackers", "verdict": "AI review aggregator met sentiment tracking en concurrentieanalyse", "priceRange": "EUR 150-400/mnd", "bestFor": "Multi-platform monitoring", "rating": 4.3, "affiliateLink": "https://www.reviewtrackers.com/"},
            {"name": "The Feedback Company", "verdict": "Nederlandse feedback software met AI text analytics en dashboards", "priceRange": "EUR 150-500/mnd", "bestFor": "HR & employee feedback", "rating": 4.1, "affiliateLink": "https://www.thefeedbackcompany.nl/"},
            {"name": "Nicereply", "verdict": "CSAT, NPS en CES metingen met AI trendanalyse — eenvoudig en effectief", "priceRange": "EUR 49-149/mnd", "bestFor": "Kleine support teams", "rating": 4.2, "affiliateLink": "https://www.nicereply.com/"},
        ],
        "related": ["beste-ai-tools-voor-klantenservice-2026", "beste-ai-tools-voor-klantfeedback-customer-experience-2026", "beste-delighted-vs-asknicely-vs-surveysparrow-vs-qualtrics-xm-2026"],
    },
]

SYSTEM_PROMPT = """Je bent een Nederlandse AI-content schrijver voor dutchaitools.nl. Schrijf een compleet vergelijkingsartikel in het Nederlands.

STRUCTUUR:
1. ## Introductie (2-3 alinea's)
2. ## Waarop vergeleken (korte sectie)
3. ## De top 7 tools — per tool: naam, verdict, features, prijs, beste voor, minpunten
4. ## Vergelijkingstabel (Markdown tabel)
5. ## Conclusie: welke tool voor welke situatie
6. ## FAQ (3 vragen)
7. ## Disclaimer

STIJL: Professioneel, data-gedreven, eerlijk (noem nadelen), praktisch. Gebruik de exacte toolnamen en prijzen die gegeven zijn. Verzin geen andere tools.

OUTPUT: Alleen de Markdown body (geen frontmatter, geen ``` markers). Begin direct met ## Introductie."""

def build_frontmatter(topic):
    tools_yaml = "\n".join([
        f"  - name: {t['name']}\n"
        f"    verdict: {t['verdict']}\n"
        f"    priceRange: {t['priceRange']}\n"
        f"    bestFor: {t['bestFor']}\n"
        f"    rating: {t['rating']}\n"
        f"    affiliateLink: {t['affiliateLink']}"
        for t in topic['tools']
    ])
    pros = [
        "- Actuele 2026 vergelijking met concrete prijzen en features",
        "- Nederlandstalig en relevant voor de Nederlandse markt",
        "- Eerlijke minpunten per tool — geen gesponsorde content",
    ]
    cons = [
        "- AI-markt evolueert snel — prijzen en features kunnen wijzigen",
        "- Niet elke tool is dagelijks hands-on getest",
        "- Sommige tools richten zich primair op de internationale markt",
    ]
    return f"""---
title: '{topic['title']}'
slug: {topic['slug']}
description: {topic['description']}
category: {topic['category']}
rating: 4.3
priceRange: EUR 0-500/mnd
pros:
{chr(10).join(pros)}
cons:
{chr(10).join(cons)}
affiliateLinks:
  - https://www.partnero.com/?via=dutchaitools
date: 2026-07-10
modelYear: 2026
featuredTool: {topic['tools'][0]['name']}
readingTime: 9 min
tools:
{tools_yaml}
related:
  - {topic['related'][0]}
  - {topic['related'][1]}
  - {topic['related'][2]}
draft: false
faq:
  - q: "Voor wie is dit artikel geschreven?"
    a: "Voor Nederlandse professionals, ondernemers en teams die willen weten welke AI tools relevant zijn in 2026. Zowel beginners als gevorderden vinden hier bruikbare inzichten."
  - q: "Hoe actueel is deze informatie?"
    a: "Dit artikel is geschreven in juli 2026 en weerspiegelt de stand van de markt op dat moment. De AI-wereld verandert snel — check bij twijfel de actuele prijzen en features bij de aanbieder zelf."
  - q: "Zijn de affiliate links betrouwbaar?"
    a: "Ja, we linken naar officiële aanbieders. Sommige links zijn affiliate links — we ontvangen een kleine commissie zonder extra kosten voor jou. Dit helpt ons de site onafhankelijk te houden."
---
"""

def generate_ollama(topic):
    tools_text = "\n".join([
        f"- {t['name']}: {t['verdict']} — {t['priceRange']} — Best for: {t['bestFor']} — Rating: {t['rating']}/5"
        for t in topic['tools']
    ])
    user_prompt = f"""Schrijf een compleet Nederlands vergelijkingsartikel voor dutchaitools.nl.

TITEL: {topic['title']}
CATEGORIE: {topic['category']}
BESCHRIJVING: {topic['description']}

TE VERGELIJKEN TOOLS:
{tools_text}

GERELATEERDE ARTIKELEN: {', '.join(topic['related'])}

Schrijf het volledige artikel in Markdown. Begin met ## Introductie."""

    payload = {
        "model": MODEL,
        "prompt": f"{SYSTEM_PROMPT}\n\n{user_prompt}",
        "stream": False,
        "options": {
            "temperature": 0.7,
            "num_predict": 4096,
        }
    }

    for attempt in range(3):
        try:
            resp = requests.post(OLLAMA_URL, json=payload, timeout=180)
            if resp.status_code != 200:
                print(f"  Attempt {attempt+1}: HTTP {resp.status_code}")
                time.sleep(5)
                continue
            data = resp.json()
            body = data.get("response", "").strip()
            if body.startswith("```"):
                body = re.sub(r'^```\w*\n?', '', body)
                body = re.sub(r'\n?```$', '', body)
            if len(body) > 500:
                return body
            print(f"  Attempt {attempt+1}: too short ({len(body)} chars), retrying...")
            time.sleep(2)
        except Exception as e:
            print(f"  Attempt {attempt+1}: {e}")
            time.sleep(5)
    return None

def main():
    print(f"=== Hermes Cron: Dutch AI Tools (Ollama fallback) ===")
    print(f"Model: {MODEL}")
    print(f"Topics: {len(TOPICS)}")
    print()

    generated = 0
    for i, topic in enumerate(TOPICS):
        slug = topic['slug']
        out_path = ARTICLES_DIR / f"{slug}.md"

        if out_path.exists():
            print(f"[{i+1}/{len(TOPICS)}] SKIP {slug} — already exists")
            continue

        print(f"[{i+1}/{len(TOPICS)}] Generating: {topic['title']}...")
        body = generate_ollama(topic)

        if not body:
            print(f"  FAILED after 3 attempts")
            continue

        fm = build_frontmatter(topic)
        full_article = fm + "\n" + body

        out_path.write_text(full_article, encoding='utf-8')
        print(f"  OK — {len(full_article)} chars → {out_path}")
        generated += 1

        if i < len(TOPICS) - 1:
            time.sleep(2)

    print(f"\n=== Done: {generated}/{len(TOPICS)} articles generated ===")
    return generated

if __name__ == "__main__":
    main()
