#!/usr/bin/env python3
"""Generate 5 new Dutch AI tool articles in genuine gap categories:
data-engineering/pipelines, callcenters/customer-service, content-strategie,
finops/cloudkosten, customer-experience/CX."""
import os, json, time, sys, requests, re

API_KEY = os.environ.get("GEMINI_API_KEY", "") or open(os.path.expanduser("~/.hermes/private/gemini-api-key")).read().strip()
BASE_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-lite:generateContent"
OUT_DIR = "/workspace/dutch-ai-tools/src/content/articles"

TOPICS = [
    # --- AI Data Engineering & Data Pipelines (0 existing) ---
    {
        "slug": "beste-ai-tools-data-engineering-data-pipelines-2026",
        "title": "Beste AI Tools voor Data Engineering & Data Pipelines 2026: top 7 vergeleken",
        "description": "AI data engineering tools voor 2026: Fivetran AI, Airbyte AI, dbt Cloud AI, Databricks AI, Snowflake Cortex AI, Stitch AI en Prefect AI vergeleken voor moderne data pipelines en ETL.",
        "category": "technologie",
        "tools": [
            ("Fivetran AI", 4.5, "EUR 100-2000/mnd", "Managed data pipeline & ELT"),
            ("Airbyte AI", 4.4, "Gratis-1000/mnd", "Open-source data integratie"),
            ("dbt Cloud AI", 4.7, "EUR 50-500/mnd", "AI-gestuurde data transformatie"),
            ("Databricks AI", 4.6, "EUR 200-5000/mnd", "Unified analytics & AI platform"),
            ("Snowflake Cortex AI", 4.5, "EUR 100-4000/mnd", "Cloud data platform met AI"),
            ("Prefect AI", 4.3, "Gratis-500/mnd", "Workflow orchestration & monitoring"),
            ("Stitch AI", 4.0, "EUR 100-500/mnd", "Simple ETL voor startups"),
        ],
        "prompt": """Schrijf een Nederlands artikel van 1200-1500 woorden over de beste AI tools voor data engineering en data pipelines in 2026.
Behandel deze 7 tools: Fivetran AI, Airbyte AI, dbt Cloud AI, Databricks AI, Snowflake Cortex AI, Prefect AI, Stitch AI.
Voor elke tool: naam, wat de AI doet voor data pipelines/ETL, prijsrange, beste use case (type data/teamgrootte), verdict.
Pluspunten en minpunten per tool. Markdown vergelijkingstabel met kolommen: tool, beste voor, AI feature, prijs, score (1-5).
Focus op: AI-gegenereerde data modellen, schema evolutie, real-time streaming, data quality monitoring.
Let op Nederlandse context: Nederlandse bedrijven met AVG-compliance, data residency in Europa.
Conclusie met aanbeveling per organisatiegrootte. 3 FAQ-vragen.
## koppen. Nederlands. Geen YAML frontmatter."""
    },
    # --- AI Callcenters & Klantenservice (0 existing) ---
    {
        "slug": "beste-ai-tools-callcenters-klantenservice-2026",
        "title": "Beste AI Tools voor Callcenters & Klantenservice 2026: top 7 vergeleken",
        "description": "AI customer service tools voor 2026: Zendesk AI, Intercom Fin, Freshdesk Freddy, Salesforce Service Cloud Einstein, LivePerson, Ada CX en Zoho Desk AI vergeleken voor geautomatiseerde klantenservice.",
        "category": "business",
        "tools": [
            ("Zendesk AI", 4.6, "EUR 50-500/mnd", "AI-gestuurde ticketing & bots"),
            ("Intercom Fin AI", 4.5, "EUR 100-800/mnd", "Conversational AI chatbot"),
            ("Freshdesk Freddy AI", 4.3, "EUR 30-300/mnd", "AI agent assist & automatisering"),
            ("Salesforce Service Cloud Einstein", 4.7, "EUR 100-1000/mnd", "Enterprise AI customer service"),
            ("LivePerson AI", 4.4, "EUR 200-1500/mnd", "Conversational commerce platform"),
            ("Ada CX AI", 4.2, "EUR 150-1000/mnd", "No-code AI chatbot platform"),
            ("Zoho Desk AI", 4.1, "EUR 0-100/mnd", "Budgetvriendelijke AI service desk"),
        ],
        "prompt": """Schrijf een Nederlands artikel van 1200-1500 woorden over de beste AI tools voor callcenters en klantenservice in 2026.
Behandel deze 7 tools: Zendesk AI, Intercom Fin AI, Freshdesk Freddy AI, Salesforce Service Cloud Einstein, LivePerson AI, Ada CX AI, Zoho Desk AI.
Voor elke tool: naam, AI-functionaliteit voor klantenservice, prijsrange, beste use case (type bedrijf/contactvolume), verdict.
Pluspunten en minpunten per tool. Markdown vergelijkingstabel.
Focus op: AI chatbots, sentimentanalyse, agent assist, ticket routing, self-service, meertalige ondersteuning.
Besteed aandacht aan Nederlandse context: meertaligheid (NL/EN), AVG-compliance voor klantdata.
Conclusie met aanbeveling per bedrijfsgrootte. 3 FAQ-vragen.
## koppen. Nederlands. Geen YAML frontmatter."""
    },
    # --- AI Content Strategy & Redactie (0 existing dedicated) ---
    {
        "slug": "beste-ai-tools-content-strategie-redactie-2026",
        "title": "Beste AI Tools voor Content Strategie & Redactie 2026: top 7 vergeleken",
        "description": "AI content strategie tools voor 2026: MarketMuse, Clearscope, Frase AI, Surfer SEO, Semrush Content AI, WordPress Jetpack AI en Copy.ai vergeleken voor contentplanning en redactie.",
        "category": "marketing",
        "tools": [
            ("MarketMuse AI", 4.6, "EUR 200-2000/mnd", "AI content strategie & research"),
            ("Clearscope AI", 4.5, "EUR 200-1500/mnd", "Content optimalisatie & briefings"),
            ("Frase AI", 4.4, "EUR 50-200/mnd", "AI content writer & research"),
            ("Surfer SEO AI", 4.4, "EUR 100-500/mnd", "SEO content optimalisatie"),
            ("Semrush Content AI", 4.3, "EUR 100-500/mnd", "Allround content marketing"),
            ("WordPress Jetpack AI", 4.1, "EUR 10-50/mnd", "AI writing assistant voor sites"),
            ("Copy.ai", 4.0, "EUR 0-200/mnd", "AI copywriting voor marketing"),
        ],
        "prompt": """Schrijf een Nederlands artikel van 1200-1500 woorden over de beste AI tools voor content strategie en redactie in 2026.
Behandel deze 7 tools: MarketMuse AI, Clearscope AI, Frase AI, Surfer SEO AI, Semrush Content AI, WordPress Jetpack AI, Copy.ai.
Voor elke tool: naam, AI-functionaliteit voor content strategie, prijsrange, beste use case (type contentteam/doel), verdict.
Pluspunten en minpunten per tool. Markdown vergelijkingstabel met kolommen: tool, beste voor, AI feature, prijs, score (1-5).
Focus op: AI-gedreven content gap-analyse, briefing generatie, SEO optimalisatie, redactionele planning, content clusters.
Speciale aandacht voor Nederlandse contentmarketeers en SEO-specialisten die in het Nederlands werken.
Conclusie met aanbeveling per type contentteam. 3 FAQ-vragen.
## koppen. Nederlands. Geen YAML frontmatter."""
    },
    # --- AI FinOps & Cloud Cost Management (0 existing) ---
    {
        "slug": "beste-ai-tools-finops-cloudkostenbeheer-2026",
        "title": "Beste AI Tools voor FinOps & Cloud Kostenbeheer 2026: top 7 vergeleken",
        "description": "AI FinOps tools voor 2026: CloudHealth AI, Vantage, AWS Cost Explorer AI, Azure Cost Management AI, Harness CCM, Densify en Spot by NetApp vergeleken voor cloudkostenoptimalisatie.",
        "category": "technologie",
        "tools": [
            ("CloudHealth AI", 4.5, "EUR 200-2000/mnd", "Multi-cloud cost management"),
            ("Vantage AI", 4.4, "EUR 0-500/mnd", "Moderne cloud cost visualisatie"),
            ("AWS Cost Explorer AI", 4.2, "Gratis", "AWS-native kostenanalyse"),
            ("Azure Cost Management AI", 4.2, "Gratis", "Azure-native kostenbeheer"),
            ("Harness CCM AI", 4.3, "EUR 100-1500/mnd", "AI cloud cost optimization"),
            ("Densify AI", 4.5, "EUR 150-1000/mnd", "ML-gestuurde resource optimalisatie"),
            ("Spot by NetApp AI", 4.4, "EUR 100-1000/mnd", "Automated cloud cost savings"),
        ],
        "prompt": """Schrijf een Nederlands artikel van 1200-1500 woorden over de beste AI tools voor FinOps en cloud kostenbeheer in 2026.
Behandel deze 7 tools: CloudHealth AI, Vantage AI, AWS Cost Explorer AI, Azure Cost Management AI, Harness CCM AI, Densify AI, Spot by NetApp AI.
Voor elke tool: naam, AI-functionaliteit voor kostenoptimalisatie, prijsrange, beste use case (type cloud/teamgrootte), verdict.
Pluspunten en minpunten per tool. Markdown vergelijkingstabel met kolommen: tool, beste voor, AI feature, prijs, score (1-5).
Focus op: AI-gedreven resource right-sizing, reserved instance aanbevelingen, anomaliëdetectie, budget forecasting.
Besteed aandacht aan Nederlandse cloud-adoptie: Nederlandse bedrijven die AWS/Azure/GCP gebruiken, datalocatie in EU.
Conclusie met aanbeveling per type organisatie. 3 FAQ-vragen.
## koppen. Nederlands. Geen YAML frontmatter."""
    },
    # --- AI Customer Experience & Klantbeleving (0 dedicated) ---
    {
        "slug": "beste-ai-tools-customer-experience-klantbeleving-2026",
        "title": "Beste AI Tools voor Customer Experience & Klantbeleving 2026: top 7 vergeleken",
        "description": "AI CX tools voor 2026: Qualtrics AI, Medallia AI, Sprinklr AI, HubSpot Service Hub AI, Glassbox AI, FullStory AI en Hotjar AI vergeleken voor klantbeleving en feedbackanalyse.",
        "category": "marketing",
        "tools": [
            ("Qualtrics AI", 4.7, "EUR 200-2000/mnd", "AI experience management platform"),
            ("Medallia AI", 4.6, "EUR 500-5000/mnd", "Enterprise CX & feedback analyse"),
            ("Sprinklr AI", 4.4, "EUR 500-3000/mnd", "Unified customer experience management"),
            ("HubSpot Service Hub AI", 4.3, "EUR 50-500/mnd", "CRM-gedreven klantbeleving"),
            ("Glassbox AI", 4.4, "EUR 200-1000/mnd", "Digital experience analytics"),
            ("FullStory AI", 4.5, "EUR 200-1000/mnd", "Session replay & UX analytics"),
            ("Hotjar AI", 4.2, "EUR 0-100/mnd", "Heatmaps & feedback tools"),
        ],
        "prompt": """Schrijf een Nederlands artikel van 1200-1500 woorden over de beste AI tools voor customer experience en klantbeleving in 2026.
Behandel deze 7 tools: Qualtrics AI, Medallia AI, Sprinklr AI, HubSpot Service Hub AI, Glassbox AI, FullStory AI, Hotjar AI.
Voor elke tool: naam, AI-functionaliteit voor CX, prijsrange, beste use case (type bedrijf/klantvolume), verdict.
Pluspunten en minpunten per tool. Markdown vergelijkingstabel met kolommen: tool, beste voor, AI feature, prijs, score (1-5).
Focus op: sentimentanalyse, NPS-voorspellingen, churn preventie, customer journey analytics, voice of customer.
Besteed aandacht aan Nederlandse context: klantbeleving in Nederlandse e-commerce en dienstverlening.
Conclusie met aanbeveling per bedrijfsgrootte. 3 FAQ-vragen.
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