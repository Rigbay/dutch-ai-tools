#!/usr/bin/env python3
"""
Generate 5 high-value AI tool comparison articles for Dutch AI Tools.
Targets genuinely missing comparisons with high Dutch search volume.
Uses Gemini 2.5 Flash via REST API. Affiliate links via affiliate_resolver.
"""
import json
import os
import sys
import time
import subprocess
from datetime import date
from pathlib import Path

# Add scripts dir to path for affiliate_resolver import
sys.path.insert(0, str(Path(__file__).resolve().parent))

SITE_ROOT = Path(__file__).resolve().parent.parent
ARTICLES_DIR = SITE_ROOT / "src" / "content" / "articles"

# Read API key
GEMINI_API_KEY = None
API_KEY_FILE = os.path.expanduser("~/.hermes/private/gemini-api-key")
try:
    GEMINI_API_KEY = open(API_KEY_FILE).read().strip()
except Exception:
    pass

if not GEMINI_API_KEY:
    # Fallback: try .env
    env_file = os.path.expanduser("~/.hermes/.env")
    try:
        for line in open(env_file):
            if line.startswith("GEMINI_API_KEY="):
                GEMINI_API_KEY = line.split("=", 1)[1].strip().strip('"').strip("'")
                break
    except Exception:
        pass

if not GEMINI_API_KEY:
    print("ERROR: Cannot read GEMINI_API_KEY from either ~/.hermes/private/gemini-api-key or ~/.hermes/.env", file=sys.stderr)
    sys.exit(1)

GEMINI_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={GEMINI_API_KEY}"

today = date.today().isoformat()

# 5 genuinely missing high-value comparisons
TOPICS = [
    {
        "slug": "notion-vs-clickup-2026",
        "title": "Notion vs ClickUp 2026: Welke All-in-One Werkplek Past bij Jou?",
        "description": "Notion en ClickUp in 2026 vergeleken: welke all-in-one werkplek is beter voor Nederlandse teams? Ontdek de scores, prijzen en verdicts in deze NL-vergelijking.",
        "category": "productiviteit",
        "featured": "Notion",
        "tools": [
            {"name": "Notion", "price": "EUR 0-18/mnd", "best_for": "Documentatie, wiki's en kennisbeheer", "rating": 4.6, "verdict": "Beste voor teams die documentatie en kennisbeheer centraal stellen — ongeëvenaarde flexibiliteit"},
            {"name": "ClickUp", "price": "EUR 0-12/mnd", "best_for": "Projectmanagement met ingebouwde docs", "rating": 4.5, "verdict": "Beste voor teams die projectmanagement én documentatie in één tool willen — meer features dan Notion"},
            {"name": "Notion AI", "price": "EUR 9-18/mnd extra", "best_for": "AI-schrijfassistent in je werkplek", "rating": 4.3, "verdict": "Sterke AI-integratie direct in Notion — genereert, vertaalt en vat samen zonder contextwissel"},
            {"name": "ClickUp AI", "price": "EUR 5-10/mnd extra", "best_for": "AI-projectmanagement en automatisering", "rating": 4.2, "verdict": "AI die projectupdates, standups en taken automatisch genereert — tijdbesparend voor managers"},
            {"name": "Notion Projects", "price": "Inbegrepen bij Plus", "best_for": "Licht projectmanagement in Notion", "rating": 4.0, "verdict": "Handig voor bestaande Notion-gebruikers die geen aparte PM-tool willen — maar minder krachtig dan ClickUp"},
            {"name": "ClickUp Docs", "price": "Inbegrepen bij Free", "best_for": "Documentatie binnen ClickUp", "rating": 4.1, "verdict": "Solide documentatie-functionaliteit — maar minder flexibel en mooi dan Notion's editor"},
        ],
        "extra_context": "Notion en ClickUp zijn de twee grootste all-in-one werkplekken in 2026. Notion is begonnen als notitie-app en uitgegroeid tot een flexibele werkplek met databases, wiki's en projectmanagement. ClickUp begon als projectmanagement-tool en heeft documentatie, whiteboards en doelen toegevoegd. Beide hebben nu AI. Het grote verschil: Notion is beter in documentatie en kennisbeheer, ClickUp is beter in projectmanagement en workflows. Nederlandse teams gebruiken beide — de keuze hangt af van of je primaire behoefte documentatie of projectmanagement is. Beide tools hebben Nederlandse interface-opties.",
        "affiliate_link": "https://www.notion.so/?ref=aitoolsnl",
    },
    {
        "slug": "chatgpt-vs-perplexity-2026",
        "title": "ChatGPT vs Perplexity 2026: AI-Chatbot of AI-Zoekmachine — Wat Heb Je Nodig?",
        "description": "ChatGPT en Perplexity AI in 2026 vergeleken: welke AI-assistent is beter voor Nederlandse gebruikers? Ontdek de scores, prijzen en verdicts in deze NL-vergelijking.",
        "category": "productiviteit",
        "featured": "ChatGPT",
        "tools": [
            {"name": "ChatGPT (GPT-4o)", "price": "EUR 0-22/mnd", "best_for": "Creatief schrijven, brainstormen en coderen", "rating": 4.7, "verdict": "Beste allround AI-assistent — ongeëvenaard in creatieve taken, programmeren en conversatie"},
            {"name": "Perplexity Pro", "price": "EUR 0-20/mnd", "best_for": "Onderzoek, fact-checking en actuele informatie", "rating": 4.6, "verdict": "Beste AI-zoekmachine — combineert realtime webzoekopdrachten met AI-samenvattingen en bronvermelding"},
            {"name": "ChatGPT Search", "price": "Inbegrepen bij Plus", "best_for": "Webzoekopdrachten binnen ChatGPT", "rating": 4.2, "verdict": "Handige toevoeging voor ChatGPT-gebruikers — maar minder diepgaand dan Perplexity's zoekfunctie"},
            {"name": "Perplexity Spaces", "price": "Inbegrepen bij Pro", "best_for": "Gepersonaliseerde AI-kennisbanken", "rating": 4.3, "verdict": "Unieke feature — upload je eigen documenten en Perplexity doorzoekt ze met AI, ideaal voor onderzoeksteams"},
            {"name": "ChatGPT Canvas", "price": "Inbegrepen bij Plus", "best_for": "Document- en codebewerking", "rating": 4.4, "verdict": "Realtime samenwerking aan documenten en code met AI — Perplexity heeft geen equivalent"},
            {"name": "Perplexity Pages", "price": "Inbegrepen bij Pro", "best_for": "AI-gegenereerde onderzoeksrapporten", "rating": 4.1, "verdict": "Genereert complete, bronverwezen artikelen — handig voor onderzoekers en studenten"},
        ],
        "extra_context": "ChatGPT en Perplexity vertegenwoordigen twee fundamenteel verschillende benaderingen van AI. ChatGPT is een conversationele AI die antwoorden genereert uit zijn trainingsdata (met optionele webzoekopdracht). Perplexity is een AI-zoekmachine die altijd het web doorzoekt en bronnen citeert. In 2026 zijn beide tools naar elkaar toe gegroeid: ChatGPT heeft Search toegevoegd, Perplexity heeft Spaces voor persoonlijke kennisbanken. Voor Nederlandse gebruikers: ChatGPT is beter in Nederlands begrip en creatieve taken, Perplexity is beter voor feitelijk onderzoek en actuele informatie. De keuze hangt af van of je wilt creëren (ChatGPT) of onderzoeken (Perplexity).",
        "affiliate_link": "https://chat.openai.com/?ref=aitoolsnl",
    },
    {
        "slug": "midjourney-vs-firefly-2026",
        "title": "Midjourney vs Adobe Firefly 2026: Welke AI Image Generator is de Beste?",
        "description": "Midjourney en Adobe Firefly in 2026 vergeleken: welke AI-beeldgenerator levert de beste kwaliteit voor Nederlandse creatieven? Ontdek de scores, prijzen en verdicts.",
        "category": "creatie",
        "featured": "Midjourney",
        "tools": [
            {"name": "Midjourney V7", "price": "EUR 10-60/mnd", "best_for": "Artistieke en fotorealistische beelden", "rating": 4.8, "verdict": "Beste AI-beeldgenerator voor pure beeldkwaliteit — ongeëvenaard in artistieke expressie en fotorealisme"},
            {"name": "Adobe Firefly", "price": "EUR 0-12/mnd (Creative Cloud)", "best_for": "Commercieel veilig beeldgebruik en Adobe-integratie", "rating": 4.5, "verdict": "Beste voor professionals die commercieel veilige beelden nodig hebben — getraind op gelicentieerde data"},
            {"name": "Midjourney Editor", "price": "Inbegrepen bij Standard+", "best_for": "Beeldbewerking en inpainting", "rating": 4.3, "verdict": "Krachtige editor voor het aanpassen van gegenereerde beelden — maar minder intuïtief dan Firefly"},
            {"name": "Firefly Generative Fill", "price": "Inbegrepen bij Photoshop", "best_for": "Naadloze beeldbewerking in Photoshop", "rating": 4.6, "verdict": "Ongeëvenaard in commerciële workflows — direct in Photoshop objecten toevoegen, verwijderen of aanpassen"},
            {"name": "Midjourney Style Reference", "price": "Inbegrepen bij alle tiers", "best_for": "Consistente visuele stijl over meerdere beelden", "rating": 4.4, "verdict": "Unieke feature — upload een referentiebeeld en Midjourney matcht de stijl, perfect voor branding"},
            {"name": "Firefly Text Effects", "price": "Inbegrepen bij Creative Cloud", "best_for": "AI-teksteffecten en typografie", "rating": 4.2, "verdict": "Unieke Adobe-feature — genereert professionele teksteffecten die Midjourney niet kan"},
        ],
        "extra_context": "Midjourney en Adobe Firefly zijn de twee grootste AI-beeldgenerators in 2026, maar met fundamenteel verschillende benaderingen. Midjourney is getraind op een enorme dataset van internetbeelden en levert de hoogste artistieke kwaliteit — maar de juridische status van trainingsdata blijft discutabel. Adobe Firefly is uitsluitend getraind op Adobe Stock-beelden en publiek domein — daardoor commercieel veilig, maar soms minder creatief. Voor Nederlandse gebruikers: Midjourney voor pure creativiteit en kunst, Firefly voor commerciële projecten en Adobe-workflows. Beide tools ondersteunen Nederlandse prompts, maar Midjourney's Discord-interface is minder toegankelijk dan Firefly's webinterface.",
        "affiliate_link": "https://www.midjourney.com/?ref=aitoolsnl",
    },
    {
        "slug": "elevenlabs-vs-playht-2026",
        "title": "ElevenLabs vs Play.ht 2026: Welke AI Text-to-Speech is het Beste voor Nederlands?",
        "description": "ElevenLabs en Play.ht in 2026 vergeleken: welke AI-stemgenerator levert de beste Nederlandse stemkwaliteit? Ontdek de scores, prijzen en verdicts in deze NL-vergelijking.",
        "category": "creatie",
        "featured": "ElevenLabs",
        "tools": [
            {"name": "ElevenLabs", "price": "EUR 0-99/mnd", "best_for": "Hoogste stemkwaliteit en Nederlands", "rating": 4.8, "verdict": "Beste AI-stemgenerator overall — Nederlandse stemmen klinken bijna menselijk, met uitstekende intonatie"},
            {"name": "Play.ht", "price": "EUR 0-49/mnd", "best_for": "Lange teksten en podcastproductie", "rating": 4.4, "verdict": "Beste voor lange audio — genereert uren aan spraak met consistente kwaliteit, ideaal voor luisterboeken"},
            {"name": "ElevenLabs Voice Cloning", "price": "EUR 22-99/mnd", "best_for": "Je eigen stem klonen", "rating": 4.7, "verdict": "Marktleider in stemklonen — kloon je eigen stem met slechts 1 minuut audio, resultaten zijn verbluffend"},
            {"name": "Play.ht Voice Cloning", "price": "EUR 29-49/mnd", "best_for": "High-fidelity stemklonen", "rating": 4.3, "verdict": "Solide stemkloon-functionaliteit — maar vereist meer audiomateriaal dan ElevenLabs voor vergelijkbare kwaliteit"},
            {"name": "ElevenLabs Projects", "price": "Inbegrepen bij Creator+", "best_for": "Lange audioboeken en podcasts", "rating": 4.2, "verdict": "Handige projectmodus voor lange content — maar Play.ht's editor is gebruiksvriendelijker"},
            {"name": "Play.ht Podcast Studio", "price": "Inbegrepen bij Pro", "best_for": "Complete podcastproductie", "rating": 4.5, "verdict": "Unieke feature — volledige podcastworkflow met meerdere AI-stemmen, muziek en sound effects"},
        ],
        "extra_context": "ElevenLabs en Play.ht zijn de twee grootste AI text-to-speech platforms in 2026. ElevenLabs is de onbetwiste marktleider in stemkwaliteit — hun Nederlandse stemmen zijn bijna niet van echt te onderscheiden. Play.ht is sterker in lange content en podcastproductie, met een gebruiksvriendelijkere editor. Beide bieden stemklonen aan. Voor Nederlandse gebruikers: ElevenLabs heeft de beste Nederlandse stemmen (vooral 'Matthias' en 'Laura'), Play.ht heeft een betere workflow voor lange projecten. De prijsverschillen zijn significant: ElevenLabs is duurder per karakter maar levert hogere kwaliteit, Play.ht is voordeliger voor bulkgebruik.",
        "affiliate_link": "https://elevenlabs.io/?ref=aitoolsnl",
    },
    {
        "slug": "figma-vs-framer-2026",
        "title": "Figma vs Framer 2026: Design Tool of No-Code Website Builder — Wat Past bij Jou?",
        "description": "Figma en Framer in 2026 vergeleken: welke tool is beter voor Nederlandse designers en developers? Ontdek de scores, prijzen en verdicts in deze NL-vergelijking.",
        "category": "creatie",
        "featured": "Figma",
        "tools": [
            {"name": "Figma", "price": "EUR 0-15/mnd", "best_for": "UI/UX design en prototyping", "rating": 4.8, "verdict": "Beste UI/UX design tool — industriestandaard voor design teams met ongeëvenaarde samenwerkingsfeatures"},
            {"name": "Framer", "price": "EUR 0-25/mnd", "best_for": "No-code websites met designkwaliteit", "rating": 4.5, "verdict": "Beste voor designers die direct live websites willen bouwen zonder code — van design naar publicatie in uren"},
            {"name": "Figma AI", "price": "Inbegrepen bij Professional", "best_for": "AI-designassistentie en auto-layout", "rating": 4.3, "verdict": "AI die designs genereert uit prompts en auto-layout toepast — versnelt het designproces aanzienlijk"},
            {"name": "Framer AI", "price": "Inbegrepen bij Pro", "best_for": "AI-websitegeneratie uit prompts", "rating": 4.4, "verdict": "Genereer complete websites uit een tekstbeschrijving — revolutionair voor snelle landingspagina's"},
            {"name": "Figma Dev Mode", "price": "EUR 25-45/mnd", "best_for": "Design-to-code handoff", "rating": 4.5, "verdict": "Brug tussen design en development — developers zien CSS, spacing en assets direct in Figma"},
            {"name": "Framer CMS", "price": "Inbegrepen bij Pro", "best_for": "Content-beheer op Framer-sites", "rating": 4.2, "verdict": "Ingebouwd CMS voor blogs en dynamische content — maar minder krachtig dan dedicated CMS-oplossingen"},
        ],
        "extra_context": "Figma en Framer zijn beide design-tools maar met fundamenteel verschillende doelen. Figma is een pure design- en prototypingtool — je ontwerpt er interfaces, maar bouwt geen live websites. Framer is een no-code website builder die aanvoelt als een designtool — je ontwerpt én publiceert live websites. In 2026 hebben beide AI toegevoegd: Figma AI genereert designs, Framer AI genereert complete websites. Voor Nederlandse gebruikers: Figma is de standaard voor UI/UX designers die samenwerken met developers, Framer is ideaal voor freelance designers en marketeers die zelf websites willen bouwen zonder code. De tools vullen elkaar aan — veel designers gebruiken Figma voor het ontwerp en Framer voor de live website.",
        "affiliate_link": "https://www.figma.com/?ref=aitoolsnl",
    },
]


def generate_article(topic, retries=3):
    prompt = f"""Je bent een Nederlandse techjournalist die objectieve, diepgaande vergelijkingsartikelen schrijft voor een Nederlandstalige AI-tools vergelijkingssite. Je schrijft vanuit kennis van de Nederlandse markt — inclusief prijzen in euro's, relevantie voor Nederlandse gebruikers, en Europese context.

Schrijf een compleet vergelijkingsartikel in het Nederlands over dit onderwerp:

TITEL: {topic['title']}
CATEGORIE: {topic['category']}
UITGELICHT PRODUCT: {topic['featured']}

VERGELIJK DEZE TOOLS (6 tools, deze volgorde aanhouden):
"""
    for i, t in enumerate(topic['tools']):
        prompt += f"\n{i+1}. {t['name']} — Prijs: {t['price']} — Beste voor: {t['best_for']} — Rating: {t['rating']}/5 — Oordeel: {t['verdict']}"

    prompt += f"""

EXTRA CONTEXT (verwerk in het artikel):
{topic['extra_context']}

STRUCTUUR VAN HET ARTIKEL:
- Begin met een pakkende introductie (2-3 alinea's) die de urgentie of relevantie van dit onderwerp voor Nederlandse gebruikers schetst
- Gebruik daarna een genummerde lijst (1 t/m 6) waarin je elke tool in detail bespreekt: wat het is, voor wie, plus- en minpunten, en de prijs in euro's
- Voeg een vergelijkingstabel toe met de 6 tools: Tool | Beste voor | Prijs | Score | Oordeel
- Sluit af met een 'Welke tool past bij jou?' sectie die gebruikers helpt kiezen op basis van hun situatie
- Voeg een conclusie toe over de algemene richting van deze tools in 2026

FORMAT: Schrijf in vloeiend, toegankelijk Nederlands. Gebruik tussenkopjes. Wees kritisch en eerlijk — niet elke tool is voor iedereen. Gebruik actuele 2026-informatie. Vermeld prijzen in euro's. Minimum 1200 woorden.

Schrijf nu het volledige artikel:"""

    for attempt in range(retries):
        try:
            payload = json.dumps({
                "contents": [{"parts": [{"text": prompt}]}],
                "generationConfig": {
                    "temperature": 0.7,
                    "maxOutputTokens": 8192,
                    "topP": 0.95,
                }
            })

            cmd = [
                "curl", "-s", "--max-time", "180",
                "-H", "Content-Type: application/json",
                "-d", payload,
                GEMINI_URL
            ]

            result = subprocess.run(cmd, capture_output=True, text=True, timeout=190)
            if result.returncode != 0:
                print(f"  curl error: {result.stderr}", file=sys.stderr)
                time.sleep(2)
                continue

            data = json.loads(result.stdout)

            if "error" in data:
                print(f"  API error: {data['error'].get('message', str(data['error']))}", file=sys.stderr)
                if attempt < retries - 1:
                    time.sleep(3)
                continue

            candidates = data.get("candidates", [])
            if not candidates:
                print(f"  No candidates in response", file=sys.stderr)
                time.sleep(2)
                continue

            text = candidates[0]["content"]["parts"][0]["text"]
            if not text or len(text) < 500:
                print(f"  Response too short ({len(text)} chars)", file=sys.stderr)
                time.sleep(2)
                continue

            return text

        except Exception as e:
            print(f"  Exception attempt {attempt+1}: {e}", file=sys.stderr)
            time.sleep(3)

    return None


def build_frontmatter(topic):
    """Build YAML frontmatter matching the site's schema."""
    tools_yaml = []
    for t in topic["tools"]:
        tools_yaml.append(f"""- name: {t['name']}
  verdict: {t['verdict']}
  priceRange: {t['price']}
  bestFor: {t['best_for']}
  rating: {t['rating']}
  affiliateLink: {topic['affiliate_link']}""")

    tools_block = "\n".join(tools_yaml)

    pros_block = """- Directe 2026 vergelijking van de populairste tools in dit segment
- Duidelijke prijsranges, scores en verdicts per tool
- Nederlandstalig en praktijkgericht advies met FAQ"""

    cons_block = """- Prijzen kunnen wijzigen — check altijd de actuele aanbieder
- Niet elke tool is dagelijks getest met intensief gebruik
- Sommige AI features zijn nog in beta of development"""

    # Generate related slugs from existing articles
    related = []
    for t in topic["tools"][:3]:
        name_slug = t['name'].lower().replace(' ', '-').replace('(', '').replace(')', '')
        related.append(f"beste-ai-tools-{topic['category']}-2026")

    # Deduplicate
    related = list(dict.fromkeys(related))[:3]

    related_block = "\n".join(f"  - {r}" for r in related)

    faq_block = f"""- q: "Wat is het belangrijkste verschil tussen {topic['tools'][0]['name']} en {topic['tools'][1]['name']} in 2026?"
  a: '{topic['tools'][0]['name']} is beter voor {topic['tools'][0]['best_for'].lower()}, terwijl {topic['tools'][1]['name']} uitblinkt in {topic['tools'][1]['best_for'].lower()}. De keuze hangt af van je primaire usecase.'
- q: "Welke tool is het beste voor Nederlandse gebruikers?"
  a: 'Beide tools ondersteunen Nederlands, maar {topic['tools'][0]['name']} heeft over het algemeen betere Nederlandstalige ondersteuning. Check de actuele features — dit verandert snel in 2026.'
- q: "Zijn er gratis versies beschikbaar?"
  a: 'Ja, zowel {topic['tools'][0]['name']} als {topic['tools'][1]['name']} bieden gratis tiers. De gratis versies hebben beperkingen in features en gebruik, maar zijn voldoende om de tools uit te proberen.'"""

    fm = f"""---
title: '{topic['title']}'
slug: {topic['slug']}
description: '{topic['description']}'
category: {topic['category']}
rating: {topic['tools'][0]['rating']}
priceRange: {topic['tools'][0]['price']}
pros:
{pros_block}
cons:
{cons_block}
affiliateLinks:
  - {topic['affiliate_link']}
date: {today}
modelYear: 2026
featuredTool: {topic['featured']}
readingTime: 8 min
tools:
{tools_block}
related:
{related_block}
draft: false
faq:
{faq_block}
---"""
    return fm


def main():
    print(f"=== Generating {len(TOPICS)} AI tool comparison articles ===")
    print(f"Date: {today}")
    print(f"API: gemini-2.5-flash")
    print()

    generated = 0
    for i, topic in enumerate(TOPICS):
        slug = topic['slug']
        filepath = ARTICLES_DIR / f"{slug}.md"

        if filepath.exists():
            print(f"[{i+1}/{len(TOPICS)}] SKIP: {slug} already exists")
            continue

        print(f"[{i+1}/{len(TOPICS)}] Generating: {slug} ...")
        body = generate_article(topic)

        if not body:
            print(f"  FAILED after all retries")
            continue

        # Clean up body — remove any markdown code fences if Gemini wrapped it
        body = body.strip()
        if body.startswith("```"):
            lines = body.split("\n")
            if lines[0].startswith("```"):
                lines = lines[1:]
            if lines and lines[-1].startswith("```"):
                lines = lines[:-1]
            body = "\n".join(lines)

        # Build full article
        frontmatter = build_frontmatter(topic)
        full_article = frontmatter + "\n\n" + body + "\n"

        # Write
        filepath.parent.mkdir(parents=True, exist_ok=True)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(full_article)

        print(f"  ✓ Written: {len(full_article)} chars, {len(body.split())} words")
        generated += 1

        # Rate limit
        if i < len(TOPICS) - 1:
            time.sleep(2)

    print(f"\n=== Done: {generated}/{len(TOPICS)} articles generated ===")
    return generated


if __name__ == "__main__":
    main()
