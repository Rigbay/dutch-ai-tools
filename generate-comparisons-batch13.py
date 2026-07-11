#!/usr/bin/env python3
"""Generate 5 comparison articles for Dutch AI Tools using Gemini API."""

import os
import json
import re
from datetime import date
from openai import OpenAI

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    # Try reading from ~/.hermes/.env
    env_path = os.path.expanduser("~/.hermes/.env")
    if os.path.exists(env_path):
        with open(env_path) as f:
            for line in f:
                if line.startswith("GEMINI_API_KEY="):
                    GEMINI_API_KEY = line.split("=", 1)[1].strip().strip('"').strip("'")
                    break
if not GEMINI_API_KEY:
    raise RuntimeError("GEMINI_API_KEY not set")

client = OpenAI(
    api_key=GEMINI_API_KEY,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai"
)

TODAY = date.today().isoformat()
ARTICLES_DIR = "src/content/articles"

# 5 comparison topics — non-overlapping with existing 24 comparisons
ARTICLES = [
    {
        "slug": "bolt-new-vs-v0-dev-vs-lovable-2026",
        "title": "Bolt.new vs v0.dev vs Lovable 2026: de beste AI app builders voor niet-developers",
        "description": "Vergelijk Bolt.new, v0.dev en Lovable in 2026: welke AI tool bouwt de beste apps zonder code? Complete koopgids met prijzen en use cases.",
        "category": "ontwikkeling",
        "featuredTool": "Bolt.new",
        "affiliateLinks": ["https://www.beehiiv.com/"],
        "priceRange": "EUR 0-50/mnd",
        "tools": [
            {"name": "Bolt.new", "verdict": "Beste allround AI app builder met StackBlitz integratie en directe deployment", "priceRange": "EUR 0-50/mnd", "bestFor": "Full-stack apps", "rating": 4.6, "affiliateLink": "https://bolt.new/?ref=aitoolsnl"},
            {"name": "v0.dev", "verdict": "Vercel's AI builder met naadloze Next.js integratie en prachtige UI output", "priceRange": "EUR 0-20/mnd", "bestFor": "React/Next.js UI", "rating": 4.5, "affiliateLink": "https://v0.dev/?ref=aitoolsnl"},
            {"name": "Lovable", "verdict": "Gebruiksvriendelijkste AI app builder met GPT-4 en snelle iteratie cycli", "priceRange": "EUR 0-50/mnd", "bestFor": "Snelle prototypes", "rating": 4.7, "affiliateLink": "https://lovable.dev/?ref=aitoolsnl"},
            {"name": "Replit AI", "verdict": "Complete cloud IDE met AI agent die volledige apps kan bouwen en deployen", "priceRange": "EUR 0-25/mnd", "bestFor": "Beginners & studenten", "rating": 4.4, "affiliateLink": "https://replit.com/?ref=aitoolsnl"},
            {"name": "Cursor Composer", "verdict": "AI code editor met agent-modus voor complexere applicaties", "priceRange": "EUR 20/mnd", "bestFor": "Ontwikkelaars met ervaring", "rating": 4.8, "affiliateLink": "https://cursor.com/?ref=aitoolsnl"},
            {"name": "Tempo Labs", "verdict": "AI builder gefocust op React componenten met visuele editor", "priceRange": "EUR 0-30/mnd", "bestFor": "React developers", "rating": 4.3, "affiliateLink": "https://www.tempolabs.ai/?ref=aitoolsnl"},
            {"name": "GPT Engineer", "verdict": "Open-source tool die op basis van prompts complete applicaties genereert", "priceRange": "Gratis (open-source)", "bestFor": "Open-source fans", "rating": 4.2, "affiliateLink": "https://gptengineer.app/?ref=aitoolsnl"},
        ],
        "prompt": """Schrijf een uitgebreid Nederlands artikel (1500-2000 woorden) dat Bolt.new, v0.dev en Lovable vergelijkt als AI app builders in 2026. 

Structuur:
- Intro: waarom AI app builders in 2026 een gamechanger zijn voor ondernemers zonder technische achtergrond
- Bolt.new: StackBlitz integratie, full-stack mogelijkheden, deployment, prijs, plus/minpunten
- v0.dev: Vercel ecosysteem, Next.js/React focus, UI kwaliteit, prijs, plus/minpunten  
- Lovable: gebruiksvriendelijkheid, GPT-4 onder de motorkap, prijs, plus/minpunten
- Ook de moeite waard: Replit AI, Cursor Composer, Tempo Labs, GPT Engineer (kort)
- Vergelijkingstabel (prijs, beste voor, leercurve, deployment, Nederlandse taal)
- Conclusie: welke voor wie
- FAQ: Kun je echt apps bouwen zonder code? Welke is het beste voor Nederlandse gebruikers? Wat kost het?

Gebruik concrete voorbeelden, prijzen in euro's, en focus op de Nederlandse gebruiker. Geen Amerikaanse voorbeelden waar mogelijk. Schrijf in vloeiend Nederlands op B1/B2 niveau. Gebruik ## koppen."""
    },
    {
        "slug": "photoshop-ai-vs-affinity-photo-vs-luminar-neo-2026",
        "title": "Photoshop AI vs Affinity Photo vs Luminar Neo 2026: beste AI fotobewerking",
        "description": "Vergelijk Adobe Photoshop AI, Affinity Photo en Luminar Neo in 2026. Welke AI fotobewerkingstool past bij jouw workflow en budget?",
        "category": "creatie",
        "featuredTool": "Adobe Photoshop",
        "affiliateLinks": ["https://www.beehiiv.com/"],
        "priceRange": "EUR 0-70/mnd",
        "tools": [
            {"name": "Adobe Photoshop", "verdict": "Industriestandaard met Generative Fill en de krachtigste AI features", "priceRange": "EUR 26-70/mnd", "bestFor": "Professionals", "rating": 4.8, "affiliateLink": "https://www.adobe.com/products/photoshop.html?ref=aitoolsnl"},
            {"name": "Affinity Photo 2", "verdict": "Eenmalige aankoop met indrukwekkende AI selectietools en HDR merge", "priceRange": "EUR 75 (eenmalig)", "bestFor": "Budget professionals", "rating": 4.5, "affiliateLink": "https://affinity.serif.com/photo/?ref=aitoolsnl"},
            {"name": "Luminar Neo", "verdict": "Beste AI-gestuurde foto-editor met slimme presets en luchtvervanging", "priceRange": "EUR 0-15/mnd", "bestFor": "Snelle resultaten", "rating": 4.6, "affiliateLink": "https://skylum.com/luminar?ref=aitoolsnl"},
            {"name": "Canva Pro", "verdict": "Toegankelijke AI foto-editor met achtergrondverwijderaar en Magic Edit", "priceRange": "EUR 13/mnd", "bestFor": "Social media", "rating": 4.4, "affiliateLink": "https://www.canva.com/?ref=aitoolsnl"},
            {"name": "DxO PhotoLab 8", "verdict": "Beste AI ruisonderdrukking en lenscorrecties op de markt", "priceRange": "EUR 139-229 (eenmalig)", "bestFor": "RAW fotografie", "rating": 4.5, "affiliateLink": "https://www.dxo.com/dxo-photolab/?ref=aitoolsnl"},
            {"name": "Pixelmator Pro", "verdict": "Uitstekende Mac-only editor met ML Super Resolution en slimme selecties", "priceRange": "EUR 60 (eenmalig)", "bestFor": "Mac gebruikers", "rating": 4.5, "affiliateLink": "https://www.pixelmator.com/pro/?ref=aitoolsnl"},
            {"name": "Photopea", "verdict": "Gratis browser-gebaseerde editor met AI plugins, Photoshop-lookalike", "priceRange": "Gratis", "bestFor": "Geen budget", "rating": 4.2, "affiliateLink": "https://www.photopea.com/?ref=aitoolsnl"},
        ],
        "prompt": """Schrijf een uitgebreid Nederlands artikel (1500-2000 woorden) dat Adobe Photoshop AI, Affinity Photo en Luminar Neo vergelijkt als AI fotobewerkingstools in 2026.

Structuur:
- Intro: AI heeft fotobewerking getransformeerd — van uren werk naar één klik
- Adobe Photoshop AI: Generative Fill, Neural Filters, prijsmodel (abonnement), plus/minpunten
- Affinity Photo 2: eenmalige aankoop, AI selectietools, HDR merge, plus/minpunten
- Luminar Neo: AI Sky Replacement, portrait enhancement, slimme presets, plus/minpunten
- Ook de moeite waard: Canva Pro, DxO PhotoLab, Pixelmator Pro, Photopea (kort)
- Vergelijkingstabel (prijs, abonnement/eenmalig, platform, AI features, leercurve)
- Conclusie: welke voor welke gebruiker (professional, hobbyist, social media manager)
- FAQ: Is Photoshop het abonnement nog waard in 2026? Kan Affinity Photo Photoshop vervangen? Welke tool heeft de beste AI?

Gebruik concrete voorbeelden, prijzen in euro's, en focus op de Nederlandse gebruiker. Schrijf in vloeiend Nederlands op B1/B2 niveau. Gebruik ## koppen."""
    },
    {
        "slug": "todoist-vs-ticktick-vs-things-2026",
        "title": "Todoist vs TickTick vs Things 3 2026: beste AI taakbeheer voor productiviteit",
        "description": "Vergelijk Todoist, TickTick en Things 3 in 2026. Welke taken-app met AI features past het beste bij jouw workflow? Complete gids.",
        "category": "productiviteit",
        "featuredTool": "Todoist",
        "affiliateLinks": ["https://www.beehiiv.com/"],
        "priceRange": "EUR 0-8/mnd",
        "tools": [
            {"name": "Todoist", "verdict": "Beste allround taakbeheer met AI scheduling en natuurlijke taal invoer", "priceRange": "EUR 0-5/mnd", "bestFor": "Algemene productiviteit", "rating": 4.7, "affiliateLink": "https://todoist.com/?ref=aitoolsnl"},
            {"name": "TickTick", "verdict": "Meeste features voor je geld met ingebouwde kalender, Pomodoro en Eisenhower matrix", "priceRange": "EUR 0-3/mnd", "bestFor": "Feature-rijke workflow", "rating": 4.6, "affiliateLink": "https://ticktick.com/?ref=aitoolsnl"},
            {"name": "Things 3", "verdict": "Mooiste en meest intuïtieve taken-app, maar alleen Apple en geen AI features", "priceRange": "EUR 10-60 (eenmalig)", "bestFor": "Apple gebruikers", "rating": 4.5, "affiliateLink": "https://culturedcode.com/things/?ref=aitoolsnl"},
            {"name": "Motion", "verdict": "AI die je agenda automatisch vult op basis van prioriteiten en deadlines", "priceRange": "EUR 19-34/mnd", "bestFor": "AI agenda planning", "rating": 4.4, "affiliateLink": "https://www.usemotion.com/?ref=aitoolsnl"},
            {"name": "Akiflow", "verdict": "Time blocking tool met snelle invoer en kalenderintegratie voor power users", "priceRange": "EUR 19/mnd", "bestFor": "Time blocking", "rating": 4.3, "affiliateLink": "https://akiflow.com/?ref=aitoolsnl"},
            {"name": "Microsoft To Do", "verdict": "Gratis en diep geïntegreerd in Microsoft 365 ecosysteem met AI suggesties", "priceRange": "Gratis", "bestFor": "Microsoft gebruikers", "rating": 4.2, "affiliateLink": "https://todo.microsoft.com/?ref=aitoolsnl"},
            {"name": "Superlist", "verdict": "Nieuwe uitdager met prachtige UI, notities en taken in één", "priceRange": "EUR 0-10/mnd", "bestFor": "Design-liefhebbers", "rating": 4.1, "affiliateLink": "https://www.superlist.com/?ref=aitoolsnl"},
        ],
        "prompt": """Schrijf een uitgebreid Nederlands artikel (1500-2000 woorden) dat Todoist, TickTick en Things 3 vergelijkt als AI taakbeheer tools in 2026.

Structuur:
- Intro: productiviteitstools met AI veranderen hoe we werken — welke past bij jou?
- Todoist: natuurlijke taal invoer, AI scheduling, Karma systeem, samenwerking, prijs, plus/minpunten
- TickTick: ingebouwde kalender, Pomodoro timer, Eisenhower matrix, habits tracker, prijs, plus/minpunten
- Things 3: Apple-only, prachtig design, GTD workflow, maar geen AI features — is dat een dealbreaker?
- Ook de moeite waard: Motion (AI agenda), Akiflow, Microsoft To Do, Superlist (kort)
- Vergelijkingstabel (prijs, platformen, AI features, samenwerking, agenda-integratie)
- Conclusie: welke voor wie (Apple gebruiker, budget, teams, power user)
- FAQ: Is Todoist het abonnement waard? Kan TickTick Todoist vervangen? Is Things 3 nog relevant zonder AI?

Gebruik concrete voorbeelden, prijzen in euro's, en focus op de Nederlandse gebruiker. Schrijf in vloeiend Nederlands op B1/B2 niveau. Gebruik ## koppen."""
    },
    {
        "slug": "framer-ai-vs-webflow-vs-wix-studio-2026",
        "title": "Framer AI vs Webflow vs Wix Studio 2026: beste AI website builder",
        "description": "Vergelijk Framer AI, Webflow en Wix Studio in 2026. Welke AI website builder levert de mooiste, snelste website zonder code?",
        "category": "creatie",
        "featuredTool": "Framer AI",
        "affiliateLinks": ["https://www.beehiiv.com/"],
        "priceRange": "EUR 0-40/mnd",
        "tools": [
            {"name": "Framer AI", "verdict": "Beste AI website builder met prachtige designs en prompt-to-website feature", "priceRange": "EUR 0-25/mnd", "bestFor": "Design portfolio's", "rating": 4.7, "affiliateLink": "https://www.framer.com/?ref=aitoolsnl"},
            {"name": "Webflow", "verdict": "Krachtigste visuele builder met CMS, maar steilere leercurve", "priceRange": "EUR 0-40/mnd", "bestFor": "Professionele sites", "rating": 4.6, "affiliateLink": "https://webflow.com/?ref=aitoolsnl"},
            {"name": "Wix Studio", "verdict": "Meest complete alles-in-één platform met AI design assistent", "priceRange": "EUR 0-35/mnd", "bestFor": "Alles-in-één", "rating": 4.5, "affiliateLink": "https://www.wix.com/studio?ref=aitoolsnl"},
            {"name": "Hostinger AI Builder", "verdict": "Goedkoopste AI builder met hosting inbegrepen, verrassend goede output", "priceRange": "EUR 3-8/mnd", "bestFor": "Klein budget", "rating": 4.3, "affiliateLink": "https://www.hostinger.com/ai-website-builder?ref=aitoolsnl"},
            {"name": "10Web", "verdict": "AI WordPress builder die bestaande sites kan kopiëren en verbeteren", "priceRange": "EUR 6-20/mnd", "bestFor": "WordPress fans", "rating": 4.4, "affiliateLink": "https://10web.io/?ref=aitoolsnl"},
            {"name": "Dorik AI", "verdict": "Nieuwe AI builder met verrassend mooie templates en snelle performance", "priceRange": "EUR 0-15/mnd", "bestFor": "Snelle lancering", "rating": 4.2, "affiliateLink": "https://dorik.com/?ref=aitoolsnl"},
            {"name": "Relume", "verdict": "AI wireframing en sitemap tool die perfect integreert met Webflow en Figma", "priceRange": "EUR 0-30/mnd", "bestFor": "Designers & agencies", "rating": 4.5, "affiliateLink": "https://www.relume.io/?ref=aitoolsnl"},
        ],
        "prompt": """Schrijf een uitgebreid Nederlands artikel (1500-2000 woorden) dat Framer AI, Webflow en Wix Studio vergelijkt als AI website builders in 2026.

Structuur:
- Intro: AI maakt websites bouwen in 2026 toegankelijk voor iedereen — van prompt naar live site
- Framer AI: prompt-to-website, designer-kwaliteit output, CMS, prijs, plus/minpunten
- Webflow: visuele precisie, Webflow AI assistant, CMS kracht, leercurve, prijs, plus/minpunten  
- Wix Studio: AI design assistent, alles-in-één inclusief hosting/domein/email, prijs, plus/minpunten
- Ook de moeite waard: Hostinger AI Builder, 10Web, Dorik AI, Relume (kort)
- Vergelijkingstabel (prijs, leercurve, design kwaliteit, SEO, e-commerce, hosting)
- Conclusie: welke voor welk type site (portfolio, webshop, bedrijfssite, landing page)
- FAQ: Kan AI echt een professionele website bouwen? Wat is goedkoper: Framer of Wix op jaarbasis? Welke is het beste voor SEO?

Gebruik concrete voorbeelden, prijzen in euro's, en focus op de Nederlandse gebruiker. Schrijf in vloeiend Nederlands op B1/B2 niveau. Gebruik ## koppen."""
    },
    {
        "slug": "gemini-workspace-vs-copilot-365-vs-notion-ai-2026",
        "title": "Gemini in Workspace vs Copilot voor Microsoft 365 vs Notion AI 2026: AI op je werk",
        "description": "Vergelijk Google Gemini in Workspace, Microsoft 365 Copilot en Notion AI in 2026. Welke AI assistent maakt jouw werkdag het productiefst?",
        "category": "productiviteit",
        "featuredTool": "Microsoft 365 Copilot",
        "affiliateLinks": ["https://www.beehiiv.com/"],
        "priceRange": "EUR 0-30/mnd",
        "tools": [
            {"name": "Microsoft 365 Copilot", "verdict": "Diepste integratie in Word, Excel, PowerPoint, Teams en Outlook", "priceRange": "EUR 28/mnd (add-on)", "bestFor": "Microsoft bedrijven", "rating": 4.7, "affiliateLink": "https://www.microsoft.com/microsoft-365/copilot?ref=aitoolsnl"},
            {"name": "Google Gemini in Workspace", "verdict": "Naadloos in Gmail, Docs, Sheets en Meet met sterke Nederlandse ondersteuning", "priceRange": "EUR 0-22/mnd", "bestFor": "Google bedrijven", "rating": 4.6, "affiliateLink": "https://workspace.google.com/solutions/ai/?ref=aitoolsnl"},
            {"name": "Notion AI", "verdict": "Beste AI in een notitie-app: schrijft, vat samen, vertaalt en automatiseert", "priceRange": "EUR 0-10/mnd (add-on)", "bestFor": "Kennismanagement", "rating": 4.5, "affiliateLink": "https://www.notion.so/product/ai?ref=aitoolsnl"},
            {"name": "Slack AI", "verdict": "AI die je Slack threads, kanalen en gesprekken samenvat en doorzoekbaar maakt", "priceRange": "EUR 0-5/mnd", "bestFor": "Slack teams", "rating": 4.3, "affiliateLink": "https://slack.com/ai?ref=aitoolsnl"},
            {"name": "ClickUp AI", "verdict": "AI projectmanager die taken aanmaakt, stand-ups schrijft en documenten genereert", "priceRange": "EUR 0-7/mnd (add-on)", "bestFor": "Projectteams", "rating": 4.4, "affiliateLink": "https://clickup.com/ai?ref=aitoolsnl"},
            {"name": "Confluence AI (Atlassian)", "verdict": "AI voor je complete Atlassian stack: Jira issues, Confluence docs, Bitbucket PRs", "priceRange": "EUR 0-10/mnd", "bestFor": "Atlassian teams", "rating": 4.2, "affiliateLink": "https://www.atlassian.com/software/artificial-intelligence?ref=aitoolsnl"},
            {"name": "Coda AI", "verdict": "Flexibele doc-as-app met AI kolommen en workflow automatisering", "priceRange": "EUR 0-12/mnd", "bestFor": "Power users", "rating": 4.3, "affiliateLink": "https://coda.io/product/ai?ref=aitoolsnl"},
        ],
        "prompt": """Schrijf een uitgebreid Nederlands artikel (1500-2000 woorden) dat Google Gemini in Workspace, Microsoft 365 Copilot en Notion AI vergelijkt als AI werkassistenten in 2026.

Structuur:
- Intro: AI zit inmiddels in je mail, documenten en spreadsheets — maar welke is de slimste collega?
- Microsoft 365 Copilot: integratie in Word/Excel/PowerPoint/Teams/Outlook, enterprise focus, prijs, plus/minpunten
- Google Gemini in Workspace: Gmail/Docs/Sheets/Meet, Nederlandse taal, prijs, plus/minpunten
- Notion AI: schrijfassistent, Q&A over je eigen documenten, automations, prijs, plus/minpunten
- Ook de moeite waard: Slack AI, ClickUp AI, Confluence AI, Coda AI (kort)
- Vergelijkingstabel (prijs, apps, Nederlandse taal, samenwerking, privacy/EU data)
- Conclusie: welke voor wie (zzp'er, MKB, enterprise, Google vs Microsoft ecosysteem)
- FAQ: Is Copilot het extra abonnement waard? Werkt Gemini goed in het Nederlands? Kan Notion AI mijn hele kennisbank doorzoeken?

Gebruik concrete voorbeelden, prijzen in euro's, en focus op de Nederlandse gebruiker. Schrijf in vloeiend Nederlands op B1/B2 niveau. Gebruik ## koppen."""
    },
]


def generate_article(article_config):
    """Generate an article body using Gemini API."""
    response = client.chat.completions.create(
        model="gemini-2.5-pro",
        messages=[
            {"role": "system", "content": "Je bent een Nederlandse tech copywriter gespecialiseerd in AI tools. Je schrijft heldere, informatieve artikelen op B1/B2 niveau. Je gebruikt concrete prijzen in euro's, Nederlandse voorbeelden, en een objectieve vergelijkende toon. Je output is ALLEEN de markdown body van het artikel — geen YAML frontmatter, geen titel, geen metadata. Begin direct met de eerste ## koppen."},
            {"role": "user", "content": article_config["prompt"]}
        ],
        temperature=0.8,
        max_tokens=4096,
    )
    return response.choices[0].message.content


def build_frontmatter(config):
    """Build YAML frontmatter for an article."""
    lines = ["---"]
    lines.append(f"title: '{config['title']}'")
    lines.append(f"slug: {config['slug']}")
    lines.append(f"description: '{config['description']}'")
    lines.append(f"category: {config['category']}")
    lines.append(f"rating: 4.5")
    lines.append(f"priceRange: {config['priceRange']}")
    lines.append("pros:")
    lines.append(f"- Vergelijking van de top AI tools in deze categorie in 2026")
    lines.append(f"- Focus op Nederlandse gebruikers met prijzen in euro's")
    lines.append(f"- Praktische use cases en concrete aanbevelingen per type gebruiker")
    lines.append("cons:")
    lines.append(f"- Prijzen kunnen wijzigen, check altijd de actuele aanbieder")
    lines.append(f"- Sommige AI features verschillen per abonnementsniveau")
    lines.append(f"- Tools ontwikkelen snel — check de laatste versies voor aankoop")
    lines.append("affiliateLinks:")
    for link in config["affiliateLinks"]:
        lines.append(f"  - {link}")
    lines.append(f"date: '{TODAY}'")
    lines.append(f"modelYear: 2026")
    lines.append(f"featuredTool: {config['featuredTool']}")
    lines.append(f"readingTime: 9 min")
    lines.append("tools:")
    for tool in config["tools"]:
        lines.append(f"- name: {tool['name']}")
        lines.append(f"  verdict: {tool['verdict']}")
        lines.append(f"  priceRange: {tool['priceRange']}")
        lines.append(f"  bestFor: {tool['bestFor']}")
        lines.append(f"  rating: {tool['rating']}")
        lines.append(f"  affiliateLink: {tool['affiliateLink']}")
    lines.append("related:")
    # Add some generic related articles
    lines.append(f"- beste-ai-chatbots-2026")
    lines.append(f"- beste-gratis-ai-tools-2026")
    lines.append("draft: false")
    lines.append("faq:")
    lines.append("- q: Wat is momenteel de beste tool in deze categorie?")
    lines.append(f"  a: Op basis van onze analyse in 2026 is {config['featuredTool']} de meest complete keuze voor de meeste Nederlandse gebruikers. De specifieke beste keuze hangt af van je budget, ecosysteem en specifieke behoeften — lees de volledige vergelijking voor een persoonlijk advies.")
    lines.append("- q: Zijn er goede gratis alternatieven?")
    lines.append("  a: Ja, meerdere tools in deze categorie bieden stevige gratis versies of eenmalige aankopen zonder abonnement. Bekijk de prijskolom in onze vergelijkingstabel voor de exacte instapkosten per tool.")
    lines.append("- q: Werken deze tools goed in het Nederlands?")
    lines.append("  a: De meeste moderne AI tools hebben uitstekende ondersteuning voor de Nederlandse taal, al verschilt de kwaliteit per platform. In het artikel lees je per tool hoe goed het Nederlands wordt ondersteund.")
    lines.append("---")
    return "\n".join(lines)


def main():
    for i, config in enumerate(ARTICLES):
        print(f"\n[{i+1}/5] Generating: {config['slug']}")
        
        # Generate body
        body = generate_article(config)
        
        # Clean up: remove any leading "---" or "# " that Gemini might add
        body = body.strip()
        body = re.sub(r'^---\s*\n', '', body)  # Remove YAML frontmatter if generated
        body = re.sub(r'^#\s+.*\n', '', body)   # Remove H1 title if generated
        
        # Assemble full article
        frontmatter = build_frontmatter(config)
        full_article = f"{frontmatter}\n\n{body.strip()}\n"
        
        # Write
        output_path = os.path.join(ARTICLES_DIR, f"{config['slug']}.md")
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(full_article)
        
        # Word count
        word_count = len(body.split()) if body else 0
        print(f"  ✓ Written {word_count} words to {output_path}")
    
    print(f"\n✅ All 5 articles generated successfully.")


if __name__ == "__main__":
    main()
