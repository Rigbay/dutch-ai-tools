#!/usr/bin/env python3
"""
Generate 4 new AI tools comparison articles using Gemini API.
Targets gaps in the dutch-ai-tools site.
"""
import json
import os
import sys
import time
from datetime import date
from pathlib import Path

SITE_ROOT = Path(__file__).resolve().parent.parent
ARTICLES_DIR = SITE_ROOT / "src" / "content" / "articles"

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")
if not GEMINI_API_KEY:
    print("ERROR: GEMINI_API_KEY not set", file=sys.stderr)
    sys.exit(1)

TOPICS = [
    {
        "slug": "beste-ai-tools-data-visualisatie-dashboards-2026",
        "category": "technologie",
        "title_prefix": "Beste AI Tools voor Data Visualisatie & Dashboards 2026",
        "featured": "Tableau AI",
        "tools": [
            {"name": "Tableau AI (Pulse)", "price": "EUR 75-150/mnd", "best_for": "Enterprise dashboards & visual analytics", "rating": 4.7, "verdict": "Krachtigste AI-visualisatieplatform voor zakelijke dashboards"},
            {"name": "Power BI Copilot", "price": "EUR 10-50/mnd", "best_for": "Microsoft-ecosysteem & self-service BI", "rating": 4.6, "verdict": "Beste keuze voor organisaties die al Microsoft 365 gebruiken"},
            {"name": "Looker Studio (Google)", "price": "Gratis", "best_for": "Google Analytics & marketing dashboards", "rating": 4.3, "verdict": "Uitstekende gratis optie voor marketingdatavisualisatie"},
            {"name": "Qlik Sense AI", "price": "EUR 30-150/mnd", "best_for": "Associatieve data-analyse & ontdekking", "rating": 4.4, "verdict": "Sterk in ongestructureerde data-analyse met AI-associaties"},
            {"name": "ThoughtSpot AI", "price": "EUR 60-200/mnd", "best_for": "Zoekgestuurde analytics & natuurlijke taalquery's", "rating": 4.5, "verdict": "Beste voor natuurlijke taal-query's en self-service analytics"},
            {"name": "Sisense AI", "price": "EUR 50-180/mnd", "best_for": "Embedded analytics & datatoepassingen", "rating": 4.2, "verdict": "Ideaal voor SaaS-bedrijven die analytics willen embedden"},
            {"name": "Domo AI", "price": "EUR 80-300/mnd", "best_for": "Business intelligence & datacultuur", "rating": 4.1, "verdict": "Alles-in-één BI-platform met AI-mogelijkheden"},
        ],
        "affiliate_link": "https://www.tableau.com/?ref=aitoolsnl",
    },
    {
        "slug": "beste-ai-tools-ux-design-user-research-2026",
        "category": "creatie",
        "title_prefix": "Beste AI Tools voor UX Design & User Research 2026",
        "featured": "Maze AI",
        "tools": [
            {"name": "Maze AI", "price": "EUR 50-300/mnd", "best_for": "User research & prototype testing", "rating": 4.6, "verdict": "Snelste tool voor AI-gedreven gebruikerstesten en inzichten"},
            {"name": "Figma AI", "price": "EUR 12-75/mnd", "best_for": "Design prototyping & UI-ontwerp", "rating": 4.7, "verdict": "Beste UI-design tool met AI-assistent voor generatie en prototyping"},
            {"name": "Hotjar AI", "price": "EUR 29-99/mnd", "best_for": "Gedragsanalyses & heatmaps", "rating": 4.4, "verdict": "Uitstekend voor AI-gedreven heatmaps en session recording analyse"},
            {"name": "UXtweak AI", "price": "EUR 30-200/mnd", "best_for": "Usability testing & tree testing", "rating": 4.3, "verdict": "Krachtige usability testing met AI-analyse"},
            {"name": "Dovetail AI", "price": "EUR 40-150/mnd", "best_for": "User research analyse & tagging", "rating": 4.5, "verdict": "Beste voor het analyseren van gebruikersonderzoek met AI-tagging"},
            {"name": "UserTesting AI", "price": "EUR 50-500/mnd", "best_for": "On-demand gebruikerstesten", "rating": 4.2, "verdict": "Grootschalige gebruikerstesten met AI-analyse"},
            {"name": "Attention Insight AI", "price": "EUR 30-100/mnd", "best_for": "Visual attention voorspelling", "rating": 4.1, "verdict": "AI die voorspelt waar gebruikers eerst naar kijken"},
        ],
        "affiliate_link": "https://maze.co/?ref=aitoolsnl",
    },
    {
        "slug": "beste-ai-tools-pr-communicatie-2026",
        "category": "marketing",
        "title_prefix": "Beste AI Tools voor PR & Communicatie 2026",
        "featured": "Meltwater AI",
        "tools": [
            {"name": "Meltwater AI", "price": "EUR 200-800/mnd", "best_for": "Media monitoring & PR-analyse", "rating": 4.6, "verdict": "Meest complete PR-platform met AI-mediainzicht en sentimentanalyse"},
            {"name": "Cision AI", "price": "EUR 300-1200/mnd", "best_for": "PR-distributie & influencer identificatie", "rating": 4.5, "verdict": "Beste voor PR-distributie en mediarelaties met AI-inzichten"},
            {"name": "Prowly AI", "price": "EUR 30-150/mnd", "best_for": "PR-campagnes & persberichten", "rating": 4.3, "verdict": "Gebruiksvriendelijk PR-platform met AI-schrijfondersteuning"},
            {"name": "Brand24 AI", "price": "EUR 49-399/mnd", "best_for": "Social listening & sentimentanalyse", "rating": 4.4, "verdict": "Krachtige social listening met AI-sentiment en trenddetectie"},
            {"name": "Muck Rack AI", "price": "EUR 150-500/mnd", "best_for": "Journalisten databases & PR-ROI", "rating": 4.2, "verdict": "Sterk in journalistendatabases en PR-campagnemeting"},
            {"name": "Notified AI", "price": "EUR 200-600/mnd", "best_for": "IR & investor relations", "rating": 4.1, "verdict": "Specialistisch platform voor investor relations met AI-analyse"},
            {"name": "Hootsuite Amplify AI", "price": "EUR 99-400/mnd", "best_for": "Social media PR & employee advocacy", "rating": 4.2, "verdict": "Effectieve AI voor employee advocacy en social PR"},
        ],
        "affiliate_link": "https://www.meltwater.com/?ref=aitoolsnl",
    },
    {
        "slug": "beste-ai-tools-audit-compliance-2026",
        "category": "business",
        "title_prefix": "Beste AI Tools voor Audit & Compliance 2026",
        "featured": "AuditBoard AI",
        "tools": [
            {"name": "AuditBoard AI", "price": "EUR 100-400/mnd", "best_for": "Audit management & risk compliance", "rating": 4.6, "verdict": "Meest complete AI-platform voor auditworkflows en compliance rapportage"},
            {"name": "OneTrust AI", "price": "EUR 200-800/mnd", "best_for": "Privacy & AVG-compliance", "rating": 4.5, "verdict": "Beste voor AI-gedreven privacy compliance en data mapping"},
            {"name": "MetricStream AI", "price": "EUR 150-500/mnd", "best_for": "Enterprise GRC & risicomanagement", "rating": 4.4, "verdict": "Enterprise-GRC met AI voor risicovoorspelling en compliance monitoring"},
            {"name": "Diligent AI", "price": "EUR 200-700/mnd", "best_for": "Board management & governance", "rating": 4.3, "verdict": "Ideaal voor bestuursrapportages en ESG-compliance met AI-inzichten"},
            {"name": "SaiGlobal AI", "price": "EUR 100-350/mnd", "best_for": "Interne audit & risicobeheer", "rating": 4.2, "verdict": "Sterk in interne auditworkflows en risico-identificatie"},
            {"name": "Vanta AI", "price": "EUR 100-500/mnd", "best_for": "SOC 2 & ISO 27001 compliance", "rating": 4.5, "verdict": "Beste voor automatisering van SOC 2- en ISO-certificeringen"},
            {"name": "Hyperproof AI", "price": "EUR 50-300/mnd", "best_for": "Compliance operations & controlebeheer", "rating": 4.1, "verdict": "Toegankelijk complianceplatform met AI voor controlebeheer"},
        ],
        "affiliate_link": "https://www.auditboard.com/?ref=aitoolsnl",
    },
]

def call_gemini(prompt):
    """Call Gemini API via native generateContent endpoint."""
    import urllib.request
    import urllib.error

    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={GEMINI_API_KEY}"
    headers = {"Content-Type": "application/json"}

    data = {
        "contents": [
            {
                "role": "user",
                "parts": [{"text": "Je bent een Nederlandse AI-tools journalist. Je schrijft eerlijke, vergelijkende artikelen in het Nederlands voor AI Tools NL, een site die AI tools vergelijkt voor Nederlandse ondernemers. Je artikelen zijn SEO-geoptimaliseerd, hebben een natuurlijke toon en bevatten praktische aanbevelingen. Gebruik markdown voor opmaak. Schrijf minstens 800 woorden per artikel. Gebruik geen generieke of oppervlakkige content.\n\n" + prompt}]
            }
        ],
        "generationConfig": {
            "temperature": 0.9,
            "maxOutputTokens": 6144
        }
    }

    req = urllib.request.Request(
        url,
        data=json.dumps(data).encode(),
        headers=headers,
        method="POST"
    )

    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            result = json.loads(resp.read())
            content = result["candidates"][0]["content"]["parts"][0]["text"]
            return content
    except Exception as e:
        print(f"ERROR calling Gemini: {e}", file=sys.stderr)
        if hasattr(e, 'read'):
            try:
                err_body = e.read().decode()
                print(f"Response body: {err_body}", file=sys.stderr)
            except:
                pass
        return None


def build_prompt(topic):
    """Build generation prompt for a topic."""
    tools_list = "\n".join([
        f"- {t['name']}: prijs {t['price']}, beste voor {t['best_for']}, score {t['rating']}/5"
        for t in topic['tools']
    ])

    return f"""Schrijf een compleet artikel in het Nederlands over {topic['title_prefix']}.

Gebruik de volgende structuur:
1. **Inleiding** (2 alinea's) — Waarom dit onderwerp relevant is in 2026 voor Nederlandse ondernemers.
2. **Tabel: De 7 beste {topic['title_prefix'].lower()}** — Een duidelijke vergelijkingstabel.
3. **Reviews per tool** — Korte review per tool (2-3 zinnen) met wie het beste past.
4. **Vergelijking: wel past bij welk type bedrijf?** — 3-4 scenario's.
5. **Waar op letten bij kiezen?** — 3-4 alinea's met criteria.
6. **Veelgestelde vragen** — 3 FAQ's met antwoorden.
7. **Conclusie** — Wie moet welke tool kiezen.

Gebruik deze tools in het artikel:
{tools_list}

Affiliate link voor de toonaangevende tool: {topic['affiliate_link']}

Eisen:
- Schrijf minstens 1000 woorden
- Gebruik concrete voorbeelden en scenario's
- SEO-vriendelijk met natuurlijke zoekwoorden
- Geef eerlijke voor- en nadelen
- Gebruik markdown opmaak
- Alles in het Nederlands
- GEEN YAML frontmatter, ALLEEN het artikel body
- Voeg geen titel/heading toe — schrijf direct de inleiding"""


def format_tool_yaml(topic):
    """Format tools section as YAML lines."""
    lines = []
    for t in topic['tools']:
        lines.append('  - name: "' + t['name'] + '"')
        lines.append('    verdict: "' + t['verdict'] + '"')
        lines.append('    priceRange: "' + t['price'] + '"')
        lines.append('    bestFor: "' + t['best_for'] + '"')
        lines.append('    rating: ' + str(t['rating']))
        lines.append('    affiliateLink: "' + topic['affiliate_link'] + '"')
    return '\n'.join(lines)


def create_article_file(topic, body):
    """Create the markdown article file."""
    tools_yaml_str = format_tool_yaml(topic)

    description_map = {
        "beste-ai-tools-data-visualisatie-dashboards-2026": "Vergelijk de beste AI tools voor data visualisatie & dashboards in 2026. Tableau AI, Power BI Copilot, Looker, Qlik, ThoughtSpot, Sisense en Domo voor BI en dashboards.",
        "beste-ai-tools-ux-design-user-research-2026": "Vergelijk de beste AI tools voor UX design & user research in 2026. Maze, Figma AI, Hotjar, UXtweak, Dovetail, UserTesting en Attention Insight voor UX-optimalisatie.",
        "beste-ai-tools-pr-communicatie-2026": "Vergelijk de beste AI tools voor PR & communicatie in 2026. Meltwater, Cision, Prowly, Brand24, Muck Rack, Notified en Hootsuite voor media monitoring en PR.",
        "beste-ai-tools-audit-compliance-2026": "Vergelijk de beste AI tools voor audit & compliance in 2026. AuditBoard, OneTrust, MetricStream, Diligent, SaiGlobal, Vanta en Hyperproof voor compliance automatisering.",
    }

    desc = description_map.get(topic['slug'], 'Vergelijk de beste AI tools voor dit segment in 2026.')

    lines = []
    lines.append("---")
    lines.append("title: '" + topic['title_prefix'] + ": top 7 vergeleken'")
    lines.append("slug: " + topic['slug'])
    lines.append('description: "' + desc + '"')
    lines.append("category: " + topic['category'])
    lines.append("rating: 4.4")
    lines.append("priceRange: EUR 0-1200/mnd")
    lines.append("pros:")
    lines.append("  - Up-to-date vergelijking van de beste AI tools in dit segment")
    lines.append("  - Met focus op Nederlandse markt en ondernemers")
    lines.append("  - Duidelijke aanbevelingen per use case en budget")
    lines.append("cons:")
    lines.append("  - Prijzen kunnen wijzigen, check altijd de aanbieder")
    lines.append("  - Sommige AI-functies zijn nog in beta of early access")
    lines.append("  - Niet elke tool is intensief getest in Nederlandse praktijk")
    lines.append("affiliateLinks:")
    lines.append("  - " + topic['affiliate_link'])
    lines.append("date: " + date.today().isoformat())
    lines.append("modelYear: 2026")
    lines.append('featuredTool: "' + topic['featured'] + '"')
    lines.append("readingTime: 9 min")
    lines.append("tools:")
    lines.append(tools_yaml_str)
    lines.append("---")
    lines.append("")
    lines.append(body.strip())
    lines.append("")

    return "\n".join(lines)


def main():
    os.makedirs(ARTICLES_DIR, exist_ok=True)
    total = len(TOPICS)
    success = 0

    for i, topic in enumerate(TOPICS, 1):
        slug = topic['slug']
        article_path = ARTICLES_DIR / f"{slug}.md"

        if article_path.exists():
            print(f"[{i}/{total}] SKIP {slug} — already exists")
            success += 1
            continue

        print(f"[{i}/{total}] Generating {slug}...")
        prompt = build_prompt(topic)
        body = call_gemini(prompt)

        if not body:
            print(f"  FAILED: Gemini returned no content", file=sys.stderr)
            continue

        # Remove code fences if present
        body = body.replace("```markdown", "").replace("```", "").strip()

        if len(body) < 200:
            print(f"  FAILED: Body too short ({len(body)} chars)", file=sys.stderr)
            continue

        content = create_article_file(topic, body)
        article_path.write_text(content, encoding='utf-8')
        print(f"  OK: {slug} — {len(body)} chars, {len(body.split())} words")
        success += 1

        # Rate limit — sleep between calls
        if i < total:
            time.sleep(3)

    print(f"\nDone: {success}/{total} articles generated")
    if success > 0:
        print(f"Articles directory: {ARTICLES_DIR}")
        print("Next step: git add + commit + push")

if __name__ == "__main__":
    main()