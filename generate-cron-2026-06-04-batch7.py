#!/usr/bin/env python3
"""Generate 5 new Dutch AI tool articles in high-value gap categories:
DeepSeek vs ChatGPT vs Grok (comparison), free vs paid AI tools, mental health,
fashion/beauty, and sustainability/ESG."""

import os, json, time, sys, requests, re

sys.path.insert(0, os.path.dirname(__file__))

API_KEY = os.environ.get("GEMINI_API_KEY", "")
if not API_KEY:
    try:
        API_KEY = open(os.path.expanduser("~/.hermes/private/gemini-api-key")).read().strip()
    except FileNotFoundError:
        print("ERROR: No GEMINI_API_KEY found. Exiting.")
        sys.exit(1)

BASE_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-lite:generateContent"
OUT_DIR = "/workspace/kieskeuken/dutch-ai-tools/src/content/articles"

TOPICS = [
    # --- DeepSeek vs ChatGPT vs Grok (high-intent comparison, 0 existing) ---
    {
        "slug": "deepseek-vs-chatgpt-vs-grok-2026",
        "title": "DeepSeek vs ChatGPT vs Grok 2026: welke AI is het beste? Volledige vergelijking",
        "description": "Vergelijk DeepSeek, ChatGPT en Grok in 2026: prestaties, prijs, Nederlandse taal, contextvenster en unieke features. Welke AI-chatbot past bij jou?",
        "category": "productiviteit",
        "tools": [
            ("ChatGPT", 4.6, "EUR 0-25/mnd", "Veelzijdige AI met grootste ecosysteem"),
            ("DeepSeek", 4.4, "EUR 0-20/mnd", "Open-source LLM met lange context"),
            ("Grok (xAI)", 4.2, "EUR 0-30/mnd", "Real-time AI met X-integratie"),
        ],
        "prompt": """Schrijf een Nederlands artikel van 1300-1600 woorden: DeepSeek vs ChatGPT vs Grok in 2026.

Dit is een vergelijkingsartikel — geen top-7 tools, maar een diepgaande 1-op-1-op-1 vergelijking.

Behandel:
1. **ChatGPT (OpenAI)**: GPT-4o, contextvenster, multimodaal, plug-ins, GPTs, prijs
2. **DeepSeek (DeepSeek)**: open-source model, lange context, codeerprestaties, prijs
3. **Grok (xAI)**: X/Twitter-integratie, real-time data, humorvolle stijl, prijs

Vergelijk op deze dimensies in tabelvorm:
- Kwaliteit Nederlandse taal
- Contextvenster (hoeveel tokens)
- Multimodale mogelijkheden
- Codeerprestaties
- Prijs (gratis tier vs premium)
- API-beschikbaarheid
- Open-source vs closed-source

Speciale focus op Nederlandse gebruikers: welke past bij studenten, professionals, ontwikkelaars, ondernemers?
Besteed aandacht aan privacy: DeepSeek (China), ChatGPT (VS), Grok (VS) — dataresidency en AVG.
Vermeld dat DeepSeek opzien baarde in 2025 met zijn lage kosten en hoge kwaliteit.

Markdown tabel met kolommen: feature, ChatGPT, DeepSeek, Grok.
Conclusie met aanbeveling per type gebruiker. 3 FAQ.
## koppen. Nederlands. Geen YAML frontmatter."""
    },
    # --- Gratis AI tools vs betaalde AI tools 2026 (high-intent, 0 existing dedicated) ---
    {
        "slug": "gratis-ai-tools-vs-betaalde-ai-tools-2026",
        "title": "Gratis AI Tools vs Betaalde AI Tools 2026: wat is de beste keuze? Vergelijking",
        "description": "Vergelijk gratis en betaalde AI tools in 2026: ChatGPT gratis vs Plus, Gemini vs Gemini Advanced, Claude vs Claude Pro. Wat krijg je extra voor je geld?",
        "category": "productiviteit",
        "tools": [
            ("ChatGPT Gratis", 4.0, "EUR 0/mnd", "Basis AI assistent zonder kosten"),
            ("ChatGPT Plus", 4.6, "EUR 25/mnd", "VoLLEGE toegang tot GPT-4o, DALL-E"),
            ("Google Gemini Gratis", 4.1, "EUR 0/mnd", "Basis Gemini met Google-integratie"),
            ("Gemini Advanced", 4.5, "EUR 25/mnd", "Ultra-model met 1M context"),
            ("Claude Gratis (Sonnet)", 4.2, "EUR 0/mnd", "Beste gratis optie voor lange teksten"),
            ("Claude Pro", 4.7, "EUR 22/mnd", "Onbeperkt Opus, hogere limieten"),
            ("DeepSeek Gratis", 4.3, "EUR 0/mnd", "Open-source alternatief met lange context"),
        ],
        "prompt": """Schrijf een Nederlands artikel van 1200-1500 woorden: Gratis AI Tools vs Betaalde AI Tools in 2026.

Behandel deze 7 opties: ChatGPT Gratis, ChatGPT Plus, Google Gemini Gratis, Gemini Advanced, Claude Gratis (Sonnet), Claude Pro, DeepSeek Gratis.
Voor elke optie: naam, wat je krijgt in de gratis tier, wat je mist zonder betaling, prijs, verdict over prijs-kwaliteit.

Focus op de hamvraag: wat mis je écht door geen abonnement te nemen?
- Beperkingen in gratis tiers (aantal berichten, snelheid, contextvenster)
- Welke features zijn premium-only (DALL-E, multimodaal, bestanden uploaden, lange context)
- Voor wie is gratis voldoende? Voor wie is betalen de moeite waard?
- Hoeveel kost een redelijke AI-setup per maand in 2026?

Markdown vergelijkingstabel met kolommen: tool/abonnement, prijs, contextlimiet, speciale features, score.
Besteed aandacht aan Nederlandse context: welke tools ondersteunen Nederlands het beste in de gratis tier.
Conclusie met aanbeveling per gebruikerstype (student, professional, ondernemer, developer). 3 FAQ.
## koppen. Nederlands. Geen YAML frontmatter."""
    },
    # --- AI tools voor mental health & therapie (growing sector, 0 existing) ---
    {
        "slug": "beste-ai-tools-mentale-gezondheid-therapie-2026",
        "title": "Beste AI Tools voor Mentale Gezondheid & Therapie 2026: top 7 vergeleken",
        "description": "AI mentale gezondheid tools voor 2026: Woebot, Wysa, Youper, Replika, BetterHelp AI, Talkspace AI en MindDoc vergeleken voor mentaal welzijn en therapieondersteuning.",
        "category": "gezondheid",
        "tools": [
            ("Woebot", 4.4, "Gratis", "AI CBT-therapie chatbot"),
            ("Wysa", 4.5, "Gratis-50/mnd", "AI emotionele ondersteuning & coaching"),
            ("Youper", 4.3, "Gratis-20/mnd", "AI mood tracking & therapie"),
            ("Replika", 4.2, "Gratis-60/mnd", "AI companion voor eenzaamheid"),
            ("BetterHelp AI", 4.1, "EUR 60-90/wk", "AI matching + menselijke therapie"),
            ("Talkspace AI", 4.0, "EUR 50-80/wk", "AI triage + professionele therapie"),
            ("MindDoc", 4.3, "Gratis-15/mnd", "AI mood & symptoommonitoring"),
        ],
        "prompt": """Schrijf een Nederlands artikel van 1200-1500 woorden over de beste AI tools voor mentale gezondheid en therapie in 2026.

Behandel deze 7 tools: Woebot, Wysa, Youper, Replika, BetterHelp AI, Talkspace AI, MindDoc.
Voor elke tool: naam, AI-functionaliteit voor mentale gezondheid, prijsrange, beste use case (type probleem/behoefte), verdict.
Pluspunten en minpunten per tool. Markdown vergelijkingstabel met kolommen: tool, beste voor, AI feature, prijs, score (1-5).

BELANGRIJK: Vermeld duidelijk dat AI tools geen vervanging zijn voor professionele hulp.
Focus op: CBT-technieken, mood tracking, mindfulness, crisisondersteuning, dagboekfuncties, AI-gesprekken.
Besteed aandacht aan Nederlandse context: Nederlandstalige ondersteuning, Nederlandse ggz-wachttijden, 113 Zelfmoordpreventie.
Vermeld dat AI een brug kan zijn tijdens lange wachttijden in de Nederlandse ggz, maar geen diagnose stelt.
Speciale aandacht voor privacy — welke tools zijn AVG-compliant, welke delen data met derden.
Conclusie met aanbeveling per behoefte (lichte ondersteuning vs serieuze problemen). 3 FAQ.
## koppen. Nederlands. Geen YAML frontmatter."""
    },
    # --- AI tools voor fashion, schoonheid & styling (0 existing) ---
    {
        "slug": "beste-ai-tools-fashion-schoonheid-styling-2026",
        "title": "Beste AI Tools voor Fashion, Schoonheid & Styling 2026: top 7 vergeleken",
        "description": "AI fashion & beauty tools voor 2026: Zalon AI, DressX, Vue.ai, Perfect Corp, Threads Styling AI, Style DNA en L'Oreal AI vergeleken voor virtuele styling en schoonheidsadvies.",
        "category": "lifestyle",
        "tools": [
            ("Zalon AI", 4.3, "Gratis", "AI personal shopper voor kleding"),
            ("DressX AI", 4.1, "Gratis-30/mnd", "Virtuele digitale kleding & try-on"),
            ("Vue.ai", 4.4, "EUR 200-2000/mnd", "AI mode visual search & recommendation"),
            ("Perfect Corp", 4.5, "Gratis-50/mnd", "AI virtuele make-up try-on"),
            ("Threads Styling AI", 4.2, "EUR 10-50/mnd", "AI personal styling service"),
            ("Style DNA AI", 4.3, "Gratis-15/mnd", "AI kleur- & stijlanalyse"),
            ("L'Oreal AI", 4.4, "Gratis", "AI huidanalyse & beauty advies"),
        ],
        "prompt": """Schrijf een Nederlands artikel van 1200-1500 woorden over de beste AI tools voor fashion, schoonheid en styling in 2026.

Behandel deze 7 tools: Zalon AI, DressX AI, Vue.ai, Perfect Corp, Threads Styling AI, Style DNA AI, L'Oreal AI.
Voor elke tool: naam, AI-functionaliteit voor fashion/beauty, prijsrange, beste use case (type gebruiker/doel), verdict.
Pluspunten en minpunten per tool. Markdown vergelijkingstabel met kolommen: tool, beste voor, AI feature, prijs, score (1-5).

Focus op: virtuele try-on, personal styling, kleur- en stijlanalyse, AI beauty advies, mode-aanbevelingen, digitale kleding.
Besteed aandacht aan Nederlandse context: Nederlandse modemarkt (Wehkamp, Zalando, About You), Nederlandse beautymerken, Nederlandse maatvoering.
Speciale aandacht voor duurzaamheid: AI kan helpen bij betere koopbeslissingen, minder retourzendingen, kledingruil.
Conclusie met aanbeveling per budget en stijlbehoefte. 3 FAQ.
## koppen. Nederlands. Geen YAML frontmatter."""
    },
    # --- AI tools voor duurzaamheid & ESG (0 existing dedicated) ---
    {
        "slug": "beste-ai-tools-duurzaamheid-esg-milieu-2026",
        "title": "Beste AI Tools voor Duurzaamheid, ESG & Milieu 2026: top 7 vergeleken",
        "description": "AI duurzaamheid tools voor 2026: IBM Environmental Intelligence, Google Cloud Carbon Footprint AI, Persefoni AI, Plan A, Greenbird AI, Climatiq AI en Watershed vergeleken voor ESG-rapportage en milieu-impact.",
        "category": "business",
        "tools": [
            ("IBM Environmental Intelligence", 4.6, "EUR 500-5000/mnd", "AI klimaatrisico & duurzaamheidsanalyse"),
            ("Google Cloud Carbon Footprint AI", 4.3, "Gratis", "AI CO2-tracking voor cloudgebruik"),
            ("Persefoni AI", 4.5, "EUR 1000-10000/mnd", "AI ESG-rapportage & carbon accounting"),
            ("Plan A", 4.4, "EUR 200-2000/mnd", "AI carbon management & decarbonisatie"),
            ("Greenbird AI", 4.2, "EUR 100-1000/mnd", "AI energieoptimalisatie & smart grids"),
            ("Climatiq AI", 4.3, "Gratis-500/mnd", "AI carbon footprint API voor ontwikkelaars"),
            ("Watershed", 4.5, "EUR 1000-10000/mnd", "Enterprise ESG-platform met AI"),
        ],
        "prompt": """Schrijf een Nederlands artikel van 1200-1500 woorden over de beste AI tools voor duurzaamheid, ESG en milieu in 2026.

Behandel deze 7 tools: IBM Environmental Intelligence, Google Cloud Carbon Footprint AI, Persefoni AI, Plan A, Greenbird AI, Climatiq AI, Watershed.
Voor elke tool: naam, AI-functionaliteit voor duurzaamheid/ESG, prijsrange, beste use case (type bedrijf/scope), verdict.
Pluspunten en minpunten per tool. Markdown vergelijkingstabel.

Focus op: carbon accounting (scope 1,2,3), ESG-rapportage (CSRD), klimaatrisico-analyse, energieoptimalisatie, supply chain duurzaamheid, AI-gedreven CO2-reductie.
Besteed aandacht aan Nederlandse context: CSRD-rapportageplicht voor NL-bedrijven, Nederlandse klimaatdoelen (55% CO2-reductie 2030), energiesector, Nederlandse datacenters (Green Datacenter), duurzaam bouwen.
Speciale focus op MKB-vriendelijke opties — niet alleen enterprise.
Vermeld Nederlandse regelgeving: CSRD, CO2-prestatieladder, SBTi.
Conclusie met aanbeveling per bedrijfsgrootte. 3 FAQ.
## koppen. Nederlands. Geen YAML frontmatter."""
    },
]

AFFILIATE_MAP = {
    "beehiiv": "https://www.beehiiv.com/?via=anonymous-operator",
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
        tools_yaml_lines.append(f'    affiliateLink: "https://www.beehiiv.com/?via=anonymous-operator"')
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
  - https://www.beehiiv.com/?via=anonymous-operator
  - https://taskade.com/?via=55nfr2
  - https://writesonic.com/?via=aitoolsnl
date: 2026-06-04
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

        frontmatter = build_frontmatter(topic, raw_text)
        full_text = frontmatter + raw_text + "\n"

        with open(out_path, "w", encoding="utf-8") as f:
            f.write(full_text)

        generated += 1
        print(f"  ✓ Written to {out_path} ({len(full_text)} chars)")

        # Small delay between API calls
        if i < len(TOPICS) - 1:
            time.sleep(2)

    print(f"\n=== DONE ===")
    print(f"Generated: {generated}")
    print(f"Failed (fallback used): {failed}")
    print(f"Skipped (already existed): {skipped}")
    print(f"Total in {OUT_DIR}: {len([f for f in os.listdir(OUT_DIR) if f.endswith('.md')])}")


if __name__ == "__main__":
    main()