#!/usr/bin/env python3
"""Generate 4 new Dutch AI comparison articles: Claude Code vs Cursor vs Windsurf,
Miro vs FigJam vs Mural, Klaviyo vs Mailchimp vs Brevo, Calendly vs Cal.com vs Doodle.
Batch 12 — May 27 2026. Uses Gemini 2.5 Flash, proper yaml.dump frontmatter."""
import os, time, sys, yaml
import requests
from pathlib import Path

# --- API Key ---
API_KEY = os.environ.get("GEMINI_API_KEY", "").strip()
if not API_KEY:
    key_file = os.path.expanduser("~/.hermes/private/gemini-api-key")
    if os.path.exists(key_file):
        with open(key_file) as f:
            API_KEY = f.read().strip()
if not API_KEY:
    print("FATAL: No GEMINI_API_KEY found")
    sys.exit(1)

BASE_URL_FLASH = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent"
ARTICLES_DIR = Path("/tmp/dutch-ai-tools/src/content/articles")

ALL_SLUGS = sorted(f.stem for f in ARTICLES_DIR.glob("*.md"))

def pick_related(new_slug, pool, n=3):
    return [s for s in pool if s != new_slug][:n]

def generate_one(prompt, attempt=1):
    url = BASE_URL_FLASH
    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {"temperature": 0.7, "maxOutputTokens": 4096}
    }
    resp = requests.post(f"{url}?key={API_KEY}", headers={"Content-Type": "application/json"}, json=payload, timeout=120)
    if resp.status_code == 503 and attempt <= 2:
        print(f"  503, retry {attempt+1}...")
        time.sleep(3)
        return generate_one(prompt, attempt + 1)
    if resp.status_code != 200:
        raise Exception(f"API error {resp.status_code}: {resp.text[:300]}")
    data = resp.json()
    text = data["candidates"][0]["content"]["parts"][0]["text"]
    return text, len(text.split())

ARTICLES = [
    {
        "slug": "claude-code-vs-cursor-vs-windsurf-2026",
        "title": "Claude Code vs Cursor vs Windsurf 2026: Beste AI Codeer Assistent Vergeleken",
        "description": "Claude Code, Cursor of Windsurf voor AI-gedreven softwareontwikkeling in 2026? Vergelijk contextvenster, codebegrip, integraties en prijs van de beste AI coding agents.",
        "category": "tools",
        "rating": 4.7,
        "priceRange": "EUR 0-50/mnd",
        "pros": ["Eerlijke vergelijking van de 3 populairste AI coding agents", "Praktisch: per taal, projectgrootte en ervaringsniveau", "NL-context met focus op zelfstandige developers en teams"],
        "cons": ["Tools ontwikkelen razendsnel — features kunnen verouderd zijn", "Prijzen wijzigen regelmatig", "Niet elke tool ondersteunt alle frameworks even goed"],
        "affiliateLinks": ["https://affiliate.notion.so/?via=aitoolsnl"],
        "date": "2026-05-27",
        "modelYear": 2026,
        "featuredTool": "Cursor",
        "readingTime": "9 min",
        "tools": [
            {"name": "Cursor", "verdict": "Beste allround AI-codeeromgeving — native AI-integratie in een fork van VS Code", "priceRange": "EUR 0-20/mnd", "bestFor": "Dagelijks codeerwerk", "rating": 4.7, "affiliateLink": "https://affiliate.notion.so/?via=aitoolsnl"},
            {"name": "Claude Code", "verdict": "Grootste contextvenster (200K tokens) — begrijpt hele codebases in één keer", "priceRange": "EUR 0-25/mnd", "bestFor": "Complexe refactors & architectuur", "rating": 4.6, "affiliateLink": "https://affiliate.notion.so/?via=aitoolsnl"},
            {"name": "Windsurf", "verdict": "Beste voor grote projecten — AI-agent die zelfstandig taken uitvoert in je IDE", "priceRange": "EUR 0-45/mnd", "bestFor": "Enterprise & monorepo's", "rating": 4.5, "affiliateLink": "https://affiliate.notion.so/?via=aitoolsnl"},
        ],
        "related": pick_related("claude-code-vs-cursor-vs-windsurf-2026", ALL_SLUGS, 3),
        "faq": [
            {"q": "Welke AI coding tool is het beste voor Nederlandse developers?",
             "a": "Voor de meeste Nederlandse developers is Cursor de beste allround keuze vanwege de naadloze VS Code-integratie. Claude Code blinkt uit in het begrijpen van grote legacy-codebases. Windsurf is ideaal voor teams die aan enterprise-projecten werken. Alle drie ondersteunen Nederlands in prompts en documentatie."},
            {"q": "Zijn AI coding agents veilig voor bedrijfscode?",
             "a": "Cursor en Windsurf bieden on-premise opties voor enterprise. Claude Code verwerkt prompts via API (Anthropic's servers). Voor gevoelige bedrijfscode: kies de enterprise-tier met dataverwerking in de EU, of gebruik lokale modellen zoals via Ollama."},
            {"q": "Kan ik gratis starten met AI coding tools?",
             "a": "Ja: Cursor heeft een gratis Hobby-plan (2000 completions/maand). Claude Code werkt met de gratis Claude-API-tier (beperkt). Windsurf biedt een gratis Community-versie met basisfunctionaliteit. Voor professioneel gebruik is een betaald plan aanbevolen."},
        ],
        "prompt": """Schrijf een Nederlands artikel van 1300-1600 woorden over Claude Code vs Cursor vs Windsurf — de 3 beste AI coding agents van 2026.

Structuur:
- Introductie: AI coding agents gaan in 2026 veel verder dan autocomplete. Claude Code (Anthropic), Cursor en Windsurf zijn de top 3. Ze begrijpen volledige codebases, schrijven complexe functies en refactoren hele projecten. Welke past bij jouw workflow?
- Hoofdsectie per tool (## koppen): Cursor, Claude Code, Windsurf. Per tool: hoe werkt het, contextvenster (tokens), IDE-integratie, prijs (EUR), sterke/zwakke punten, beste use case, verdict (1-2 zinnen).
- Vergelijkingstabel (markdown): tool, contextvenster, IDE, git-integratie, multi-file refactor, prijs gratis, prijs pro (EUR/mnd), beste-voor, score
- Conclusie: welke tool voor welke developer — solo freelance developer, startup team, enterprise team, hobbyist/student, iemand die veel met legacy code werkt
- Sluit af met FAQ (## Veelgestelde Vragen) met exact 3 vragen en antwoorden

Focus op de Nederlandse/Europese developermarkt. Prijzen in EUR. Schrijf in vloeiend, nuchter Nederlands. Vermeld dat Cursor en Windsurf forks van VS Code zijn, Claude Code een CLI-tool is die in elke editor werkt.""",
    },
    {
        "slug": "miro-vs-figjam-vs-mural-2026",
        "title": "Miro vs FigJam vs Mural 2026: Beste AI Whiteboard voor Teams Vergeleken",
        "description": "Miro, FigJam of Mural voor online whiteboards met AI in 2026? Vergelijk brainstormfuncties, templates, realtime samenwerking, integraties en prijs voor Nederlandse teams.",
        "category": "tools",
        "rating": 4.5,
        "priceRange": "EUR 0-20/mnd",
        "pros": ["Praktische vergelijking van de 3 grootste online whiteboards", "AI-features specifiek benoemd (samenvatten, sticky notes, diagrammen)", "NL-context met focus op hybride teams"],
        "cons": ["Gratis versies hebben beperkingen in teamgrootte", "AI-functies verschillen per abonnementsvorm", "Exporteerbaarheid is niet altijd perfect"],
        "affiliateLinks": ["https://affiliate.notion.so/?via=aitoolsnl"],
        "date": "2026-05-27",
        "modelYear": 2026,
        "featuredTool": "Miro",
        "readingTime": "8 min",
        "tools": [
            {"name": "Miro", "verdict": "Meest complete whiteboard — 300+ templates, beste AI-assistent, grootste integratiemarkt", "priceRange": "EUR 0-20/mnd", "bestFor": "Grote teams & workshops", "rating": 4.7, "affiliateLink": "https://affiliate.notion.so/?via=aitoolsnl"},
            {"name": "FigJam", "verdict": "Naadloos met Figma — beste voor design teams die al Figma gebruiken", "priceRange": "EUR 0-5/mnd", "bestFor": "Design & product teams", "rating": 4.4, "affiliateLink": "https://affiliate.notion.so/?via=aitoolsnl"},
            {"name": "Mural", "verdict": "Sterkste facilitator-tools — ingebouwde timers, stemrondes en privacyzones", "priceRange": "EUR 10-20/mnd", "bestFor": "Consultants & facilitators", "rating": 4.3, "affiliateLink": "https://affiliate.notion.so/?via=aitoolsnl"},
        ],
        "related": pick_related("miro-vs-figjam-vs-mural-2026", ALL_SLUGS, 3),
        "faq": [
            {"q": "Welk whiteboard is het beste voor Nederlandse teams met hybride werken?",
             "a": "Miro is de beste keuze voor hybride teams: de AI-assistent (Miro Assist) helpt met samenvatten van brainstormsessies, en de uitgebreide integraties (Slack, Teams, Jira) passen in de meeste Nederlandse bedrijfsworkflows. FigJam is ideaal als je team al Figma gebruikt."},
            {"q": "Kan ik gratis een whiteboard gebruiken met mijn team?",
             "a": "Ja: Miro gratis biedt 3 editable boards. FigJam gratis is onbeperkt voor teams tot 3 editors. Mural gratis biedt 3 murals + 1 room. Voor serieus teamgebruik is een betaald plan (vanaf EUR 5-10/mnd/pp) aanbevolen."},
            {"q": "Werken deze tools in het Nederlands?",
             "a": "De UI van alle drie is in het Engels. AI-functies zoals Miro Assist begrijpen Nederlandse prompts goed. Templates en sticky notes kunnen gewoon in het Nederlands. Specifieke NL-sjablonen zijn beperkt — je maakt ze zelf op maat."},
        ],
        "prompt": """Schrijf een Nederlands artikel van 1300-1600 woorden over Miro vs FigJam vs Mural — de 3 beste online AI-whiteboards van 2026.

Structuur:
- Introductie: Online whiteboards zijn onmisbaar voor hybride teams in 2026. Miro, FigJam (van Figma) en Mural hebben AI geïntegreerd voor slimmere brainstorms, automatische samenvattingen en snellere workshopvoorbereiding. Welke past bij jouw team?
- Hoofdsectie per tool (## koppen): Miro, FigJam, Mural. Per tool: kernfunctie, AI-features, hoeveel templates, integraties (Slack, Teams, Jira, etc.), prijs in EUR, plus/minpunten, beste use case, verdict.
- Vergelijkingstabel (markdown): tool, AI-assistent, templates, integraties, gratis limiet, prijs (EUR/mnd/pp), beste-voor, score
- Conclusie: welke voor wie — design team, consultancy die workshops faciliteert, groot bedrijf met 50+ gebruikers, startup, docent/onderwijs
- Sluit af met FAQ (## Veelgestelde Vragen) met exact 3 vragen en antwoorden

Prijzen in EUR per gebruiker per maand. Schrijf nuchter Nederlands. Noem dat FigJam een apart product van Figma is en naadloos integreert met Figma-designbestanden.""",
    },
    {
        "slug": "klaviyo-vs-mailchimp-vs-brevo-2026",
        "title": "Klaviyo vs Mailchimp vs Brevo 2026: Beste AI E-mailmarketing Tool voor E-commerce",
        "description": "Klaviyo, Mailchimp of Brevo (voorheen Sendinblue) voor AI-gedreven e-mailmarketing in 2026? Vergelijk automations, AI-segmentatie, prijs en GDPR-compliance voor Nederlandse webshops.",
        "category": "tools",
        "rating": 4.6,
        "priceRange": "EUR 0-50/mnd",
        "pros": ["Specifiek voor e-commerce — geen generieke e-mailmarketing", "Brevo is Frans/EU = betere GDPR-compliance", "Praktische prijsvergelijking op contacten, niet features"],
        "cons": ["Prijzen stijgen snel bij groeiende contactlijsten", "AI-functies verschillen sterk per tier", "Migreren tussen platforms is tijdrovend"],
        "affiliateLinks": ["https://affiliate.notion.so/?via=aitoolsnl"],
        "date": "2026-05-27",
        "modelYear": 2026,
        "featuredTool": "Klaviyo",
        "readingTime": "9 min",
        "tools": [
            {"name": "Klaviyo", "verdict": "Specifiek gebouwd voor e-commerce — beste AI-segmentatie en productaanbevelingen", "priceRange": "EUR 0-45/mnd", "bestFor": "Webshops & Shopify", "rating": 4.8, "affiliateLink": "https://affiliate.notion.so/?via=aitoolsnl"},
            {"name": "Mailchimp", "verdict": "Meest veelzijdig — sterke AI-contentgenerator, breedste integraties, ook voor niet-e-commerce", "priceRange": "EUR 0-30/mnd", "bestFor": "Allround marketing", "rating": 4.3, "affiliateLink": "https://affiliate.notion.so/?via=aitoolsnl"},
            {"name": "Brevo", "verdict": "Beste Europese keuze — Franse servers, sterke GDPR-tools, SMS + e-mail in één platform", "priceRange": "EUR 0-49/mnd", "bestFor": "GDPR-compliance & EU", "rating": 4.4, "affiliateLink": "https://affiliate.notion.so/?via=aitoolsnl"},
        ],
        "related": pick_related("klaviyo-vs-mailchimp-vs-brevo-2026", ALL_SLUGS, 3),
        "faq": [
            {"q": "Welke e-mailmarketingtool is het beste voor Nederlandse webshops?",
             "a": "Klaviyo is specifiek gebouwd voor e-commerce en integreert diep met Shopify, WooCommerce en Magento. De AI voorspelt koopgedrag en segmenteert klanten automatisch. Voor GDPR-compliance: Brevo (Franse servers, AVG-proof). Mailchimp is de beste allrounder als je ook nieuwsbrieven en landingspagina's wilt."},
            {"q": "Wat kost e-mailmarketing voor 1000 contacten?",
             "a": "Klaviyo: EUR 20/mnd (500 contacten gratis). Mailchimp: EUR 13/mnd (500 contacten gratis). Brevo: EUR 25/mnd (onbeperkt contacten, betaalt per email-volume). Brevo is vaak voordeliger bij grote lijsten met lage verzendfrequentie."},
            {"q": "Hoe zit het met AVG/GDPR bij deze tools?",
             "a": "Brevo is de veiligste keuze: Franse servers, volledig AVG-compliant, DPA standaard beschikbaar. Mailchimp verwerkt data in de VS (Privacy Shield-gecertificeerd). Klaviyo biedt EU-serveropties in hogere plannen. Voor strikte GDPR: Brevo of Klaviyo met EU-datacenter."},
        ],
        "prompt": """Schrijf een Nederlands artikel van 1300-1600 woorden over Klaviyo vs Mailchimp vs Brevo — de 3 beste AI-e-mailmarketingtools van 2026 voor e-commerce.

Structuur:
- Introductie: AI verandert e-mailmarketing in 2026. Klaviyo, Mailchimp en Brevo gebruiken AI voor segmentatie, productaanbevelingen en slimme automations. Welke past bij jouw Nederlandse webshop?
- Hoofdsectie per tool (## koppen): Klaviyo, Mailchimp, Brevo. Per tool: hoe AI helpt, e-commerce features, integraties (Shopify, WooCommerce), prijs (EUR), GDPR/AVG-status, plus/minpunten, verdict.
- Vergelijkingstabel (markdown): tool, AI-segmentatie, e-commerce focus, integraties, gratis tot (contacten), prijs (EUR/mnd voor 2500 contacten), AVG, score
- Conclusie: welke voor wie — Shopify webshop, WooCommerce webshop, fysieke winkel met nieuwsbrief, startup met klein budget, enterprise met 50K+ contacten
- Sluit af met FAQ (## Veelgestelde Vragen) met exact 3 vragen en antwoorden

Focus op de Nederlandse e-commercemarkt. Prijzen in EUR. Schrijf nuchter Nederlands. Brevo is Frans en heette voorheen Sendinblue — vermeld dat. Leg uit waarom AI-segmentatie (RFM-analyse, voorspelde lifetime value) belangrijk is voor webshops.""",
    },
    {
        "slug": "calendly-vs-cal-com-vs-doodle-2026",
        "title": "Calendly vs Cal.com vs Doodle 2026: Beste AI Planningstool Vergeleken",
        "description": "Calendly, Cal.com of Doodle voor slim afspraken plannen met AI in 2026? Vergelijk automatische agenda's, teamplanning, integraties, privacy en prijs voor Nederlandse professionals.",
        "category": "tools",
        "rating": 4.4,
        "priceRange": "EUR 0-16/mnd",
        "pros": ["Praktische vergelijking op prijs, privacy en integraties", "Cal.com is open-source — uniek voor developers en privacy-bewuste teams", "NL-context: alle drie ondersteunen Nederlandse UI en tijdzones"],
        "cons": ["Gratis versies hebben forse beperkingen", "AI-functies (zoals slimme suggesties) nog in ontwikkeling", "Verschillen in agenda-integraties (Google, Outlook, iCloud)"],
        "affiliateLinks": ["https://affiliate.notion.so/?via=aitoolsnl"],
        "date": "2026-05-27",
        "modelYear": 2026,
        "featuredTool": "Calendly",
        "readingTime": "8 min",
        "tools": [
            {"name": "Calendly", "verdict": "De standaard — grootste gebruikersbasis, meeste integraties, beste AI-suggesties voor optimale tijden", "priceRange": "EUR 0-16/mnd", "bestFor": "Individuen & teams", "rating": 4.7, "affiliateLink": "https://affiliate.notion.so/?via=aitoolsnl"},
            {"name": "Cal.com", "verdict": "Open-source alternatief — self-host optie, beste privacy, groeiend ecosysteem", "priceRange": "EUR 0-15/mnd", "bestFor": "Privacy & developers", "rating": 4.3, "affiliateLink": "https://affiliate.notion.so/?via=aitoolsnl"},
            {"name": "Doodle", "verdict": "Beste voor groepsplanning — polls voor meetings met 5+ deelnemers, geen accounts nodig", "priceRange": "EUR 0-9/mnd", "bestFor": "Groepsafspraken", "rating": 4.2, "affiliateLink": "https://affiliate.notion.so/?via=aitoolsnl"},
        ],
        "related": pick_related("calendly-vs-cal-com-vs-doodle-2026", ALL_SLUGS, 3),
        "faq": [
            {"q": "Welke planningstool is het beste voor Nederlandse ZZP'ers?",
             "a": "Calendly is de beste keuze voor ZZP'ers: eenvoudig in te stellen, gratis tot 1 agenda, integreert met Google/Outlook, en ondersteunt Nederlandse tijdsweergave. Cal.com is ideaal als je waarde hecht aan privacy en open-source. Doodle is het beste voor eenmalige groepsafspraken zoals vriendenuitjes of vrijwilligersoverleg."},
            {"q": "Is Calendly gratis genoeg?",
             "a": "De gratis versie van Calendly biedt 1 actieve meeting type, onbeperkt meetings en basisintegraties. Voor de meeste ZZP'ers is dit voldoende. Betaalde plannen (vanaf EUR 10/mnd) bieden extra: meerdere meeting types, teamplanning, AI-suggesties en herinnerings-SMS. Cal.com gratis biedt méér features maar is technischer."},
            {"q": "Hoe veilig zijn mijn agenda-gegevens?",
             "a": "Cal.com is het veiligst: open-source, self-host mogelijk, GDPR-compliant met EU-servers. Calendly verwerkt data in de VS (SOC2-gecertificeerd). Doodle's dataverwerking is deels in Zwitserland (sterke privacywetten). Voor vertrouwelijke agenda's van bijv. therapeuten of juristen is Cal.com met self-hosting de beste keuze."},
        ],
        "prompt": """Schrijf een Nederlands artikel van 1300-1600 woorden over Calendly vs Cal.com vs Doodle — de 3 beste AI-planningstools van 2026.

Structuur:
- Introductie: Slim plannen met AI bespaart uren heen-en-weer mailen. Calendly, Cal.com en Doodle zijn de top 3 in 2026. Ze gebruiken AI voor optimale tijdsuggesties, automatische herinneringen en naadloze agenda-integratie. Welke past bij jou?
- Hoofdsectie per tool (## koppen): Calendly, Cal.com, Doodle. Per tool: type planning (1-op-1 vs groep), AI-features, agenda-integraties (Google, Outlook, iCloud), prijs (EUR), privacy/GDPR, plus/minpunten, verdict.
- Vergelijkingstabel (markdown): tool, type, AI-suggesties, agenda's, gratis limiet, prijs pro (EUR/mnd), GDPR, beste-voor, score
- Conclusie: welke voor wie — ZZP'er, verkoopteam (round-robin), consultant die betaalde sessies plant, teamleider die groepsmeetings organiseert, developer die self-host wil
- Sluit af met FAQ (## Veelgestelde Vragen) met exact 3 vragen en antwoorden

Focus op Nederlandse professionals. Prijzen in EUR. Schrijf vloeiend, toegankelijk Nederlands. Cal.com is open-source en heette voorheen Calendso — vermeld dat kort. Doodle is Zwitsers qua oorsprong.""",
    },
]

for i, article in enumerate(ARTICLES):
    print(f"[{i+1}/4] {article['slug']}...")
    try:
        text, wc = generate_one(article.pop("prompt"))
        fm = {k: v for k, v in article.items()}
        yaml_str = yaml.dump(fm, allow_unicode=True, sort_keys=False, width=200)
        content = f"---\n{yaml_str}---\n\n{text}\n"
        path = ARTICLES_DIR / f"{article['slug']}.md"
        path.write_text(content, encoding="utf-8")
        print(f"  OK: {wc} words -> {path}")
        time.sleep(1)
    except Exception as e:
        print(f"  FAIL: {e}")
        sys.exit(1)

print("\nDone: 4/4 OK")
