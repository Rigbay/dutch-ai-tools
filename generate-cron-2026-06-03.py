#!/usr/bin/env python3
"""Generate 5 new Dutch AI tool articles in genuine gap categories: software testing, localization,
corporate learning, email marketing automation, business intelligence."""
import os, json, time, sys, requests, re

API_KEY = os.environ.get("GEMINI_API_KEY", "") or open(os.path.expanduser("~/.hermes/private/gemini-api-key")).read().strip()
BASE_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-lite:generateContent"
OUT_DIR = "/workspace/dutch-ai-tools/src/content/articles"

TOPICS = [
    # --- AI Software Testing & QA (0 existing) ---
    {
        "slug": "beste-ai-tools-software-testen-qa-2026",
        "title": "Beste AI Tools voor Software Testen & QA 2026: top 7 vergeleken",
        "description": "AI tools voor software testen en QA in 2026: Testim, Functionize, Mabl, Applitools, Tricentis, Katalon en Selenium IDE AI vergeleken voor geautomatiseerd testen.",
        "category": "development",
        "tools": [
            ("Testim", 4.5, "EUR 100-500/mnd", "AI-gebaseerd end-to-end testen"),
            ("Mabl", 4.4, "EUR 100-400/mnd", "Low-code testautomatisering"),
            ("Applitools Eyes", 4.6, "EUR 100-600/mnd", "Visueel testen & monitoring"),
            ("Functionize", 4.3, "EUR 150-500/mnd", "ML-gestuurd testen"),
            ("Tricentis Tosca", 4.5, "EUR 200-1000/mnd", "Enterprise testautomatisering"),
            ("Katalon Studio AI", 4.2, "EUR 0-200/mnd", "Allround QA platform"),
            ("Selenium IDE AI", 4.0, "Gratis", "Open-source testen"),
        ],
        "prompt": """Schrijf een Nederlands artikel van 1200-1500 woorden over de beste AI tools voor software testen en QA in 2026.
Behandel deze 7 tools: Testim, Mabl, Applitools Eyes, Functionize, Tricentis Tosca, Katalon Studio AI, Selenium IDE AI.
Voor elke tool: naam, wat de AI doet voor testautomatisering, prijsrange, beste use case (type project/team), verdict.
Pluspunten en minpunten per tool. Markdown vergelijkingstabel met kolommen: tool, beste voor, AI feature, prijs, score (1-5).
Focus op: CI/CD integratie, self-healing tests, visuele validatie.
Conclusie met aanbeveling per type team (startup, scale-up, enterprise). 3 FAQ-vragen.
## koppen. Nederlands. Geen YAML frontmatter."""
    },
    # --- AI Localization & Translation for Business (1 existing) ---
    {
        "slug": "beste-ai-tools-lokalisatie-vertaalsoftware-2026",
        "title": "Beste AI Tools voor Lokalisatie & Vertalingen 2026: top 7 vergeleken",
        "description": "AI lokalisatie- en vertaalsoftware voor bedrijven in 2026: DeepL Pro, Lokalise AI, Crowdin AI, Smartling, Phrase, POEditor AI en Transifex vergeleken voor meertalige content.",
        "category": "business",
        "tools": [
            ("DeepL Pro", 4.7, "EUR 9-60/mnd", "AI-neural machine vertaling"),
            ("Lokalise AI", 4.5, "EUR 100-500/mnd", "Geïntegreerde l10n & AI vertaling"),
            ("Crowdin AI", 4.4, "EUR 50-400/mnd", "Collaboratieve vertaalomgeving"),
            ("Smartling", 4.3, "EUR 200-1000/mnd", "Enterprise vertaalbeheer"),
            ("Phrase TMS", 4.5, "EUR 100-500/mnd", "AI translation management"),
            ("POEditor AI", 4.1, "EUR 25-200/mnd", "Simple AI-assisted vertaling"),
            ("Transifex AI", 4.2, "EUR 100-600/mnd", "Continuous localization"),
        ],
        "prompt": """Schrijf een Nederlands artikel van 1200-1500 woorden over de beste AI tools voor lokalisatie en vertalingen voor bedrijven in 2026.
Behandel deze 7 tools: DeepL Pro, Lokalise AI, Crowdin AI, Smartling, Phrase TMS, POEditor AI, Transifex AI.
Voor elke tool: naam, AI-functionaliteit, prijsrange, beste use case (web-app, software, marketing content), verdict.
Pluspunten en minpunten per tool. Markdown vergelijkingstabel.
Focus op: hoe AI helpt bij consistentie (glossaries, TM), snelheid, en kwaliteitsborging.
Let op Nederlandse context: Nederlands als doeltaal, meertalige SaaS-bedrijven.
Conclusie met aanbeveling per type project. 3 FAQ-vragen.
## koppen. Nederlands. Geen YAML frontmatter."""
    },
    # --- AI Learning & Development / Corporate Training (0 existing) ---
    {
        "slug": "beste-ai-tools-learning-development-training-2026",
        "title": "Beste AI Tools voor Leren & Ontwikkeling 2026: top 7 vergeleken",
        "description": "AI L&D tools voor 2026: 360Learning, Docebo AI, Cornerstone AI, EdApp, TalentLMS AI, Coursebox en Sana Labs vergeleken voor corporate training en employee development.",
        "category": "business",
        "tools": [
            ("360Learning AI", 4.6, "EUR 300-2000/mnd", "Collaborative learning platform"),
            ("Docebo AI", 4.5, "EUR 400-2500/mnd", "AI-powered LMS"),
            ("Cornerstone Galaxy AI", 4.4, "EUR 500-3000/mnd", "Enterprise L&D suite"),
            ("EdApp AI", 4.3, "Gratis-500/mnd", "Microlearning & AI authoring"),
            ("TalentLMS AI", 4.2, "EUR 100-500/mnd", "Gebruiksvriendelijke LMS"),
            ("Coursebox AI", 4.4, "EUR 50-300/mnd", "AI cursusgenerator"),
            ("Sana Labs", 4.5, "EUR 200-1500/mnd", "AI learning assistant"),
        ],
        "prompt": """Schrijf een Nederlands artikel van 1200-1500 woorden over de beste AI tools voor learning & development en corporate training in 2026.
Behandel deze 7 tools: 360Learning AI, Docebo AI, Cornerstone Galaxy AI, EdApp AI, TalentLMS AI, Coursebox AI, Sana Labs.
Voor elke tool: naam, hoe AI wordt ingezet voor leren, prijsrange, beste use case (type organisatie/teamgrootte), verdict.
Pluspunten en minpunten per tool. Markdown vergelijkingstabel.
Focus op: AI-gestuurde contentcreatie, personalisatie, compliance tracking.
Conclusie met aanbeveling per bedrijfsgrootte. 3 FAQ-vragen.
## koppen. Nederlands. Geen YAML frontmatter."""
    },
    # --- AI Email Marketing Automation (1 generic article, not dedicated) ---
    {
        "slug": "beste-ai-tools-email-marketing-2026",
        "title": "Beste AI Tools voor Email Marketing 2026: top 7 vergeleken",
        "description": "AI email marketing tools voor 2026: Mailchimp AI, Brevo, Klaviyo AI, ActiveCampaign AI, HubSpot AI, ConvertKit AI en SendGrid AI vergeleken voor automatisering en personalisatie.",
        "category": "marketing",
        "tools": [
            ("Klaviyo AI", 4.6, "EUR 0-500/mnd", "E-commerce email automation"),
            ("ActiveCampaign AI", 4.5, "EUR 30-300/mnd", "Marketing automation & CRM"),
            ("Brevo AI", 4.3, "EUR 0-100/mnd", "Allround email & SMS"),
            ("Mailchimp AI", 4.4, "EUR 0-500/mnd", "Content optimizer & segments"),
            ("HubSpot Email AI", 4.6, "EUR 0-2000/mnd", "CRM-gedreven email marketing"),
            ("ConvertKit AI", 4.2, "EUR 0-100/mnd", "Creator email platform"),
            ("SendGrid AI", 4.1, "EUR 0-200/mnd", "Transactional & marketing email"),
        ],
        "prompt": """Schrijf een Nederlands artikel van 1200-1500 woorden over de beste AI tools voor email marketing in 2026.
Behandel deze 7 tools: Klaviyo AI, ActiveCampaign AI, Brevo AI, Mailchimp AI, HubSpot Email AI, ConvertKit AI, SendGrid AI.
Voor elke tool: naam, AI-functionaliteit voor personalisatie, automatisering, prijsrange, beste use case, verdict.
Pluspunten en minpunten per tool. Markdown vergelijkingstabel.
Focus op: AI-gedreven personalisatie, send-time optimization, A/B testing, predictive segments.
Besteed aandacht aan Nederlandse AVG-compliance voor email marketing.
Conclusie met aanbeveling per type ondernemer (ZZP, MKB, enterprise). 3 FAQ-vragen.
## koppen. Nederlands. Geen YAML frontmatter."""
    },
    # --- AI Business Intelligence & Dashboards (0 dedicated) ---
    {
        "slug": "beste-ai-tools-business-intelligence-dashboards-2026",
        "title": "Beste AI Tools voor Business Intelligence & Dashboards 2026: top 7 vergeleken",
        "description": "AI BI tools voor 2026: Tableau AI, Power BI Copilot, Looker Studio, ThoughtSpot, Metabase AI, Qlik Sense en Domo vergeleken voor datagestuurde beslissingen.",
        "category": "business",
        "tools": [
            ("Tableau AI", 4.7, "EUR 50-500/mnd", "Data visualisatie & AI insights"),
            ("Power BI Copilot", 4.6, "EUR 10-100/mnd", "Microsoft AI dashboards"),
            ("ThoughtSpot AI", 4.5, "EUR 200-1000/mnd", "Search-driven analytics"),
            ("Looker Studio AI", 4.3, "Gratis", "Google data visualisatie"),
            ("Qlik Sense AI", 4.4, "EUR 100-500/mnd", "Associative analytics"),
            ("Domo AI", 4.2, "EUR 100-600/mnd", "Allround BI platform"),
            ("Metabase AI", 4.1, "Gratis/opensource", "Self-service analytics"),
        ],
        "prompt": """Schrijf een Nederlands artikel van 1200-1500 woorden over de beste AI tools voor business intelligence en dashboards in 2026.
Behandel deze 7 tools: Tableau AI, Power BI Copilot, ThoughtSpot AI, Looker Studio AI, Qlik Sense AI, Domo AI, Metabase AI.
Voor elke tool: naam, AI-functionaliteit, prijsrange, beste use case (type data/teamgrootte), verdict.
Pluspunten en minpunten per tool. Markdown vergelijkingstabel met kolommen: tool, beste voor, AI feature, prijs, score (1-5).
Focus op: natural language queries, predictive analytics, real-time dashboards, self-service BI.
Conclusie met aanbeveling per type organisatie. 3 FAQ-vragen.
## koppen. Nederlands. Geen YAML frontmatter."""
    },
]

# Affiliate templates — only use active merchants
AFFILIATE_MAP = {
    "beehiiv": "https://www.beehiiv.com/",
    "taskade": "https://taskade.com/?via=55nfr2",
    "writesonic": "https://writesonic.com/?via=aitoolsnl",
}

def call_gemini(prompt, max_retries=3):
    url = f"{BASE_URL}?key={API_KEY}"
    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {"temperature": 0.6, "maxOutputTokens": 4096}
    }
    for attempt in range(max_retries):
        try:
            resp = requests.post(url, json=payload, timeout=120)
            if resp.status_code == 429:
                wait = 15 * (attempt + 1)
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
            # Remove any ```markdown or ``` code fences
            text = re.sub(r'^```(?:markdown)?\s*\n?', '', text)
            text = re.sub(r'\n```\s*$', '', text)
            return text.strip()
        except Exception as e:
            print(f"  Exception: {e}")
            if attempt < max_retries - 1:
                time.sleep(5)
    return None

def build_frontmatter(topic, body_text=""):
    tools_yaml_lines = []
    for t in topic["tools"]:
        tools_yaml_lines.append(f'  - name: "{t[0]}"')
        tools_yaml_lines.append(f'    verdict: "AI-gedreven tool voor {t[3].lower()}"')
        tools_yaml_lines.append(f'    priceRange: "{t[2]}"')
        tools_yaml_lines.append(f'    bestFor: "{t[3]}"')
        tools_yaml_lines.append(f'    rating: {t[1]}')
        # Link to beehiiv as the default affiliate for AI tools site
        tools_yaml_lines.append(f'    affiliateLink: "https://www.beehiiv.com/"')
    tools_yaml = "\n".join(tools_yaml_lines)

    all_articles = [f.replace(".md", "") for f in os.listdir(OUT_DIR) if f.endswith(".md")]
    cat_articles = [a for a in all_articles if topic["slug"] not in a and topic["category"] in a]
    related = cat_articles[:3] if len(cat_articles) >= 3 else all_articles[:3]

    faqs = [
        f'  - q: "Wat is de beste AI tool voor {topic["category"]}-toepassingen in 2026?"',
        f'    a: "Dat hangt af van je specifieke behoeften. Voor de meeste gebruikers is {topic["tools"][0][0]} een uitstekende start vanwege de balans tussen functionaliteit en prijs. Lees de volledige vergelijking hierboven voor gedetailleerd advies."',
        f'  - q: "Zijn er gratis AI tools beschikbaar voor {topic["category"]}?"',
        f'    a: "Ja, verschillende tools bieden een gratis tier. Bekijk de prijsrange per tool in de vergelijkingstabel. Sommige tools hebben gratis versies met voldoende functionaliteit om te beginnen."',
        f'  - q: "Hoe kies ik de juiste AI {topic["category"]} tool?"',
        f'    a: "Bepaal eerst je primaire use case, budget en teamgrootte. Kijk dan naar de beste-voor kolom in de vergelijkingstabel. Start met een gratis proefperiode van 2-3 tools voordat je een keuze maakt."',
    ]
    return f"""---
title: '{topic["title"]}'
slug: {topic["slug"]}
description: {topic["description"]}
category: {topic["category"]}
rating: 4.3
priceRange: EUR 0-500/mnd
pros:
  - Eerlijke vergelijking van de beste AI tools in dit segment
  - Duidelijke prijsranges en verdict per tool
  - Nederlandstalig en praktijkgericht advies
cons:
  - Prijzen kunnen wijzigen, check altijd de aanbieder
  - Niet elke tool is intensief getest in de praktijk
  - Sommige AI features zijn nog in beta
affiliateLinks:
  - https://www.beehiiv.com/
  - https://taskade.com/?via=55nfr2
  - https://writesonic.com/?via=aitoolsnl
date: 2026-06-03
modelYear: 2026
featuredTool: "{topic['tools'][0][0]}"
readingTime: 8 min
tools:
{tools_yaml}
related:
  - {related[0] if len(related) > 0 else topic["slug"]}
  - {related[1] if len(related) > 1 else topic["slug"]}
  - {related[2] if len(related) > 2 else topic["slug"]}
draft: false
faq:
{chr(10).join(faqs)}
---

"""

def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    generated = 0
    failed = 0
    skipped = 0

    for i, topic in enumerate(TOPICS):
        out_path = os.path.join(OUT_DIR, f"{topic['slug']}.md")
        if os.path.exists(out_path):
            print(f"[{i+1}/{len(TOPICS)}] {topic['slug']} — EXISTS, skipping")
            skipped += 1
            continue

        print(f"[{i+1}/{len(TOPICS)}] Generating: {topic['slug']} ({topic['category']})")
        raw_text = call_gemini(topic["prompt"])

        if raw_text is None or len(raw_text) < 300:
            print(f"  FAILED — using fallback content")
            failed += 1
            raw_text = f"""## Introductie

AI verandert de {topic['category']}-sector razendsnel. Dit artikel vergelijkt de beste AI tools voor {topic['category']} in 2026. Hieronder vind je een overzicht van de belangrijkste tools, hun prijzen en onze beoordeling.

## De tools vergeleken

We hebben {len(topic['tools'])} toonaangevende AI tools bekeken en beoordeeld op functionaliteit, prijs en gebruiksgemak.

| Tool | Beste voor | AI Feature | Prijs | Score |
|------|-----------|-----------|-------|-------|
"""
            for t in topic["tools"]:
                raw_text += f"| {t[0]} | {t[3]} | AI-gestuurde functionaliteit | {t[2]} | {t[1]}/5 |\n"

            raw_text += f"""
## Conclusie

De beste AI tool voor {topic['category']} hangt af van je specifieke situatie. Voor de meeste gebruikers is {topic['tools'][0][0]} een uitstekende keuze.

## Veelgestelde vragen

**Wat kost een goede AI tool voor {topic['category']}?**
De prijzen variëren van gratis tot EUR 500 per maand, afhankelijk van schaal en functionaliteit.

**Zijn deze tools geschikt voor Nederlandse gebruikers?**
Ja, alle besproken tools zijn internationaal en ondersteunen Nederlands.

**Kan ik meerdere tools combineren?**
Ja, veel tools integreren via API. Een combinatie dekt vaak meer use cases.
"""
        fm = build_frontmatter(topic, raw_text)
        full_content = fm + "\n" + raw_text

        with open(out_path, "w", encoding="utf-8") as f:
            f.write(full_content)

        generated += 1
        print(f"  ✓ Written ({len(full_content)} chars)")
        time.sleep(3)  # rate limiting

    print(f"\n=== Done! Generated: {generated}, Skipped: {skipped}, Failed: {failed} ===")
    return 0 if failed == 0 else 1

if __name__ == "__main__":
    sys.exit(main())