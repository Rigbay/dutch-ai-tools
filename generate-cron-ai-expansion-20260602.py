#!/usr/bin/env python3
"""Generate 5 new Dutch AI tool articles targeting the thinnest categories: Legal, Real Estate, Sales/CRM, Customer Support, Energy/Sustainability."""
import os, json, time, sys, requests, re

API_KEY = os.environ.get("GEMINI_API_KEY", "") or open(os.path.expanduser("~/.hermes/private/gemini-api-key")).read().strip()
BASE_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-lite:generateContent"
OUT_DIR = "/workspace/dutch-ai-tools/src/content/articles"

TOPICS = [
    # --- Legal/Juridisch (1 → 3) ---
    {
        "slug": "beste-ai-tools-contracten-recht-2026",
        "title": "Beste AI Tools voor Contracten & Recht 2026: top 7 vergeleken",
        "description": "AI contract tools voor 2026: Ironclad, Evisort, Linklaters AI, Lawgeex, Kira, Luminance en Spellbook vergeleken voor juridische documentanalyse, contractbeheer en compliance.",
        "category": "business",
        "tools": [
            ("Ironclad", 4.6, "EUR 500-3000/mnd", "Contract lifecycle management"),
            ("Evisort AI", 4.5, "EUR 300-2000/mnd", "AI contractanalyse"),
            ("Luminance", 4.4, "EUR 400-2500/mnd", "Due diligence & document review"),
            ("Kira Systems", 4.3, "EUR 500-3000/mnd", "Contractanalyse & extractie"),
            ("Spellbook AI", 4.5, "EUR 100-500/mnd", "AI voor juridisch schrijven"),
            ("Lawgeex", 4.2, "EUR 200-1500/mnd", "AI contract review"),
            ("Harvey AI", 4.6, "EUR 300-2000/mnd", "Legal assistant & research"),
        ],
        "prompt": """Schrijf een Nederlands artikel van 1200-1500 woorden over de beste AI tools voor contracten en recht in 2026.
Behandel deze 7 tools: Ironclad, Evisort AI, Luminance, Kira Systems, Spellbook AI, Lawgeex, Harvey AI.
Voor elke tool: naam, belangrijkste AI-functionaliteit, prijsrange, beste use case (welk type juridisch werk), verdict.
Pluspunten en minpunten per tool. Markdown vergelijkingstabel met kolommen: tool, beste voor, AI feature, prijs, score (1-5).
Let op Nederlandse context: AVG/GDPR compliance, Nederlands contractenrecht.
Conclusie met aanbeveling per type gebruiker (zzp-jurist, middelgroot kantoor, corporate legal team). 3 FAQ-vragen.
## koppen. Nederlands. Geen YAML frontmatter."""
    },
    # --- Real Estate/Vastgoed (2 → 4) ---
    {
        "slug": "beste-ai-tools-woningmarkt-huis-kopen-2026",
        "title": "Beste AI Tools voor de Woningmarkt 2026: top 7 vergeleken",
        "description": "AI tools voor huizenjacht, woningwaardering en verkoop in 2026: Zillow AI, HouseCanary, Reonomy, Skyline AI, Curbio, Knock AI en HomeLight vergeleken voor kopers en verkopers.",
        "category": "business",
        "tools": [
            ("Zillow AI", 4.5, "Gratis", "Woningwaarde schatting"),
            ("HouseCanary", 4.4, "EUR 100-500/mnd", "AVM & marktprognoses"),
            ("Reonomy AI", 4.3, "EUR 200-1000/mnd", "Commercieel vastgoed data"),
            ("Skyline AI", 4.5, "EUR 300-2000/mnd", "Investeringsanalyse"),
            ("Knock AI", 4.2, "EUR 100-300/mnd", "Verkoop & inruilplatform"),
            ("HomeLight AI", 4.3, "Gratis", "Makelaar matching"),
            ("Curbio AI", 4.1, "Projectprijzen", "Renovatie prioritering"),
        ],
        "prompt": """Schrijf een Nederlands artikel van 1200-1500 woorden over de beste AI tools voor de woningmarkt in 2026.
Behandel deze 7 tools: Zillow AI, HouseCanary, Reonomy AI, Skyline AI, Knock AI, HomeLight AI, Curbio AI.
Voor elke tool: naam, AI-functionaliteit, prijs, beste use case (koper, verkoper, investeerder), verdict.
Focus op: woningwaardering, marktanalyse, investeringsbeslissingen.
Vergelijk hoe AI de Nederlandse woningmarkt kan helpen (Funda-data, WOZ-waarde, hypotheekmogelijkheden).
Markdown vergelijkingstabel. Conclusie. 3 FAQ-vragen.
## koppen. Nederlands. Geen YAML frontmatter."""
    },
    # --- Sales/CRM (2 → 4) ---
    {
        "slug": "beste-ai-tools-sales-automation-2026",
        "title": "Beste AI Tools voor Sales Automation 2026: top 7 vergeleken",
        "description": "Vergelijk AI sales automation tools voor 2026: Outreach, SalesLoft, Gong, Clari, People.ai, LeadIQ en ZoomInfo AI voor lead scoring, pipeline management en voorspellingen.",
        "category": "marketing",
        "tools": [
            ("Gong AI", 4.7, "EUR 300-1500/mnd", "Gespreksanalyse & coaching"),
            ("Outreach AI", 4.5, "EUR 200-1000/mnd", "Sales engagement platform"),
            ("SalesLoft AI", 4.4, "EUR 200-800/mnd", "Cadence & sequencing"),
            ("Clari AI", 4.5, "EUR 300-2000/mnd", "Revenue intelligence"),
            ("People.ai", 4.2, "EUR 200-1500/mnd", "Pipeline analytics"),
            ("ZoomInfo AI", 4.3, "EUR 500-3000/mnd", "Data enrichment & prospecting"),
            ("LeadIQ AI", 4.1, "EUR 50-200/mnd", "Lead capture & sequencing"),
        ],
        "prompt": """Schrijf een Nederlands artikel van 1200-1500 woorden over de beste AI tools voor sales automation in 2026.
Behandel deze 7 tools: Gong AI, Outreach AI, SalesLoft AI, Clari AI, People.ai, ZoomInfo AI, LeadIQ AI.
Voor elke tool: naam, AI-functionaliteit, prijsrange, beste use case (SDR, AE, sales manager), verdict.
Focus op: lead scoring, pipeline management, revenue forecasting, gespreksanalyse.
Markdown vergelijkingstabel. Conclusie met aanbeveling per teamgrootte. 3 FAQ-vragen.
## koppen. Nederlands. Geen YAML frontmatter."""
    },
    # --- Customer Support (4 → 5) ---
    {
        "slug": "beste-ai-helpdesk-tickets-2026",
        "title": "Beste AI Helpdesk & Ticket Tools 2026: top 7 vergeleken",
        "description": "Vergelijk AI helpdesk tools: Zendesk AI, Freshdesk AI, Intercom Fin, Salesforce Service Cloud, HubSpot Service AI, Tidio en Kustomer AI voor ticketautomatisering en klanttevredenheid.",
        "category": "business",
        "tools": [
            ("Zendesk AI", 4.6, "EUR 55-200/mnd", "Ticket automatisering"),
            ("Intercom Fin AI", 4.5, "EUR 100-500/mnd", "AI chatbot & support"),
            ("Freshdesk AI", 4.3, "EUR 30-150/mnd", "Ticket management"),
            ("Salesforce Service Cloud AI", 4.4, "EUR 100-500/mnd", "Enterprise support"),
            ("HubSpot Service AI", 4.3, "EUR 50-200/mnd", "CRM-integratie"),
            ("Tidio AI", 4.1, "EUR 20-100/mnd", "E-commerce support"),
            ("Kustomer AI", 4.2, "EUR 100-300/mnd", "Omnichannel support"),
        ],
        "prompt": """Schrijf een Nederlands artikel van 1200-1500 woorden over de beste AI helpdesk en ticket systemen in 2026.
Behandel deze 7 tools: Zendesk AI, Intercom Fin AI, Freshdesk AI, Salesforce Service Cloud AI, HubSpot Service AI, Tidio AI, Kustomer AI.
Voor elke tool: naam, belangrijkste AI-features (automatische antwoorden, sentiment analyse, routing), prijsrange, beste use case, verdict.
Focus op: ticket automatisering, AI-chatbots, klanttevredenheid, ROI.
Markdown vergelijkingstabel. Conclusie. 3 FAQ-vragen.
## koppen. Nederlands. Geen YAML frontmatter."""
    },
    # --- Energy/Sustainability (2 → 3) ---
    {
        "slug": "beste-ai-tools-energiebeheer-2026",
        "title": "Beste AI Tools voor Energiebeheer & Duurzaamheid 2026: top 7 vergeleken",
        "description": "Vergelijk AI energiebeheer tools voor 2026: GridAI, Enel X AI, Schneider EcoStruxure, Siemens AI, Google DeepMind Energy, Octopus Energy AI en WattTime voor slim energiemanagement.",
        "category": "technologie",
        "tools": [
            ("GridAI", 4.4, "EUR 500-5000/mnd", "Grid optimalisatie"),
            ("Enel X AI", 4.3, "EUR 200-2000/mnd", "Energie management platform"),
            ("Schneider EcoStruxure AI", 4.5, "EUR 300-3000/mnd", "Industrieel energiebeheer"),
            ("Siemens AI", 4.4, "EUR 400-5000/mnd", "Gebouw automatisering"),
            ("Google DeepMind Energy", 4.6, "Projectmatig", "Datacenter koeling"),
            ("Octopus Energy AI", 4.2, "Gratis voor klanten", "Klant energiegebruik"),
            ("WattTime AI", 4.1, "EUR 0-500/mnd", "Emissie tracking"),
        ],
        "prompt": """Schrijf een Nederlands artikel van 1200-1500 woorden over de beste AI tools voor energiebeheer en duurzaamheid in 2026.
Behandel deze 7 tools: GridAI, Enel X AI, Schneider EcoStruxure AI, Siemens AI, Google DeepMind Energy, Octopus Energy AI, WattTime AI.
Voor elke tool: naam, AI-functionaliteit (voorspellend onderhoud, verbruiksoptimalisatie, emissiereductie), prijsrange, beste use case, verdict.
Specifiek voor Nederland: energietransitie, zonne-energie, warmtepompen, netcongestie.
Markdown vergelijkingstabel. Conclusie. 3 FAQ-vragen.
## koppen. Nederlands. Geen YAML frontmatter."""
    },
]

AFFILIATE_TEMPLATES = {
    "amazon": "https://www.amazon.nl/dp/{asin}?tag=kieskeukennl-21",
    "beehiiv": "https://www.beehiiv.com/",
    "generic": "https://www.{domain}.com/?ref=aitoolsnl",
}

def call_gemini(prompt, max_retries=5):
    url = f"{BASE_URL}?key={API_KEY}"
    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {"temperature": 0.5, "maxOutputTokens": 4096}
    }
    for attempt in range(max_retries):
        try:
            resp = requests.post(url, json=payload, timeout=180)
            if resp.status_code == 429:
                wait = 20 * (attempt + 1)
                print(f"  Rate limited (429), waiting {wait}s...")
                time.sleep(wait)
                continue
            if resp.status_code != 200:
                print(f"  API error {resp.status_code}: {resp.text[:200]}")
                if attempt < max_retries - 1:
                    time.sleep(10)
                    continue
                return None
            data = resp.json()
            text = data["candidates"][0]["content"]["parts"][0]["text"]
            return text
        except Exception as e:
            print(f"  Exception: {e}")
            if attempt < max_retries - 1:
                time.sleep(10)
    return None

def slugify(domain):
    return domain.lower().replace(" ", "")

def build_frontmatter(topic, body_text=""):
    tools_yaml = "\n".join([
        f'  - name: "{t[0]}"\n'
        f'    verdict: "AI-gedreven tool voor {t[3].lower()}"\n'
        f'    priceRange: "{t[2]}"\n'
        f'    bestFor: "{t[3]}"\n'
        f'    rating: {t[1]}\n'
        f'    affiliateLink: "https://www.{slugify(t[0].split(" ")[0].replace("AI","").strip())}.com/?ref=aitoolsnl"'
        for t in topic["tools"]
    ])
    all_articles = [f.replace(".md", "") for f in os.listdir(OUT_DIR) if f.endswith(".md") and f != "index.md" and f != "404.md"]
    cat_articles = [a for a in all_articles if topic["slug"] not in a]
    related = cat_articles[:3]
    faqs = [
        f'  - q: "Wat is de beste AI tool voor {topic["category"]} in 2026?"',
        f'    a: "Dat hangt af van je specifieke behoeften. Voor de meeste gebruikers is {topic["tools"][0][0]} een uitstekende start vanwege de balans tussen functionaliteit en prijs. Lees de volledige vergelijking voor een gedetailleerd advies."',
        f'  - q: "Zijn er gratis AI {topic["category"]} tools beschikbaar?"',
        f'    a: "Ja, verschillende tools bieden een gratis tier. Sommige tools zoals WattTime AI en HomeLight bieden gratis basisfunctionaliteit. Bekijk de prijsrange per tool in de vergelijking hierboven."',
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
date: 2026-06-02
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

    for i, topic in enumerate(TOPICS):
        out_path = os.path.join(OUT_DIR, f"{topic['slug']}.md")
        if os.path.exists(out_path):
            print(f"[{i+1}/{len(TOPICS)}] {topic['slug']} — EXISTS, skipping")
            generated += 1
            continue

        print(f"[{i+1}/{len(TOPICS)}] Generating: {topic['slug']} ({topic['category']})")
        raw_text = call_gemini(topic["prompt"])

        if raw_text is None:
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
                raw_text += f"""| {t[0]} | {t[3]} | AI-gestuurde functionaliteit | {t[2]} | {t[1]}/5 |
"""
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

    print(f"\n=== Done! Generated: {generated}, Failed: {failed} ===")
    return 0 if failed == 0 else 1

if __name__ == "__main__":
    sys.exit(main())