#!/usr/bin/env python3
"""Generate 5 new Dutch AI tools comparison articles: Ahrefs vs Semrush vs Moz,
Jira vs Linear vs ClickUp, Exact Online vs Moneybird vs Snelstart,
GitHub vs GitLab vs Bitbucket, Vercel vs Netlify vs Cloudflare Pages.
June 4, 2026 — Hermes cron batch 2 autonomous run."""
import os, json, time, sys, requests, yaml
from datetime import date

API_KEY = os.environ.get("GEMINI_API_KEY", os.environ.get("GOOGLE_API_KEY", "")).strip()
if not API_KEY:
    key_file = os.path.expanduser("~/.hermes/private/gemini-api-key")
    if os.path.exists(key_file):
        with open(key_file) as f:
            API_KEY = f.read().strip()
if not API_KEY:
    env_file = os.path.expanduser("~/.hermes/.env")
    if os.path.exists(env_file):
        with open(env_file) as f:
            for line in f:
                if line.startswith("GEMINI_API_KEY="):
                    API_KEY = line.split("=", 1)[1].strip().strip('"').strip("'")
                    break
                if line.startswith("GOOGLE_API_KEY="):
                    API_KEY = line.split("=", 1)[1].strip().strip('"').strip("'")
                    break

BASE_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent"
ARTICLES_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "src/content/articles")

ALL_SLUGS = [
    f.replace(".md", "") for f in sorted(os.listdir(ARTICLES_DIR)) if f.endswith(".md")
]

def pick_related(new_slug, pool, n=3):
    candidates = [s for s in pool if s != new_slug]
    return candidates[:n] if len(candidates) >= n else candidates

NEW_ARTICLES = [
    {
        "slug": "ahrefs-vs-semrush-vs-moz-2026",
        "title": "Ahrefs vs Semrush vs Moz 2026: beste SEO-tools vergeleken",
        "description": "Ahrefs, Semrush of Moz in 2026? Vergelijk de beste SEO-tools op keyword research, backlink-analyse, rank tracking, prijs en gebruiksvriendelijkheid voor Nederlandse websites.",
        "category": "marketing",
        "prompt": """Schrijf een Nederlands artikel van 1200-1500 woorden over Ahrefs vs Semrush vs Moz in 2026. Behandel precies 7 tools: Ahrefs, Semrush, Moz Pro, SE Ranking, Majestic, Sistrix, Ubersuggest.

Structuur:
- Introductie: SEO in 2026 — AI-gegenereerde content, SGE, EEAT, het Nederlandse SEO-landschap
- Per tool een ## kop met: beschrijving, prijsrange (EUR/maand), beste use case (keyword research, backlinks, technische SEO, concurrentieanalyse), plus- en minpunten, verdict (1-2 zinnen)
- Een markdown-vergelijkingstabel met alle 7 tools: naam, prijs vanaf (EUR), beste voor, Backlink-index grootte, score (1-5)
- Conclusie: welke SEO-tool voor wie (freelancer, MKB, e-commerce, enterprise, niche-blogger, bureau, startende marketeer)
- 3 FAQ-vragen over SEO-tools in 2026

Focus op Nederlandse markt. Sistrix als Duitse/Europese speler specifiek benoemen met sterke NL/EU data. Prijzen in EUR. Vloeiend Nederlands. Praktische koopadviezen met budgetindicaties.""",
        "tools": [
            {"name": "Ahrefs", "verdict": "Beste backlink-database en content gap analyse — onmisbaar voor serieuze linkbuilding", "priceRange": "EUR 99-999/mnd", "bestFor": "Backlinks & Contentstrategie", "rating": 4.8, "affiliateLink": "https://ahrefs.com/?ref=aitoolsnl"},
            {"name": "Semrush", "verdict": "Meest complete all-in-one SEO-suite met sterke concurrentieanalyse en PPC-data", "priceRange": "EUR 120-450/mnd", "bestFor": "All-in-one SEO & PPC", "rating": 4.7, "affiliateLink": "https://semrush.com/?ref=aitoolsnl"},
            {"name": "Moz Pro", "verdict": "Gebruiksvriendelijk met sterke lokale SEO-tools en de vertrouwde Domain Authority metric", "priceRange": "EUR 99-599/mnd", "bestFor": "Lokale SEO & Beginners", "rating": 4.3, "affiliateLink": "https://moz.com/?ref=aitoolsnl"},
            {"name": "SE Ranking", "verdict": "Beste prijs-kwaliteitverhouding met white-label rapportages — ideaal voor bureaus", "priceRange": "EUR 40-150/mnd", "bestFor": "Budget & Agencies", "rating": 4.4, "affiliateLink": "https://seranking.com/?ref=aitoolsnl"},
            {"name": "Majestic", "verdict": "Meest gespecialiseerde backlink-tool met unieke Trust Flow en Citation Flow metrics", "priceRange": "EUR 42-400/mnd", "bestFor": "Backlink-specialisten", "rating": 4.1, "affiliateLink": "https://majestic.com/?ref=aitoolsnl"},
            {"name": "Sistrix", "verdict": "Europese SEO-krachtpatser met sterke NL/BE data en zichtbaarheidsindex", "priceRange": "EUR 99-499/mnd", "bestFor": "Europese SEO & Enterprise", "rating": 4.3, "affiliateLink": "https://sistrix.com/?ref=aitoolsnl"},
            {"name": "Ubersuggest", "verdict": "Beste instapmodel van Neil Patel — eenvoudig, betaalbaar en verrassend compleet", "priceRange": "EUR 12-40/mnd", "bestFor": "Starters & ZZP", "rating": 4.0, "affiliateLink": "https://neilpatel.com/ubersuggest/?ref=aitoolsnl"},
        ],
        "related": pick_related("ahrefs-vs-semrush-vs-moz-2026", ALL_SLUGS, 3)
    },
    {
        "slug": "jira-vs-linear-vs-clickup-2026",
        "title": "Jira vs Linear vs ClickUp 2026: beste projectmanagement voor ontwikkelteams",
        "description": "Jira, Linear of ClickUp in 2026? Vergelijk de beste projectmanagement tools voor developers op snelheid, sprints, GitHub-integratie, prijs en gebruiksvriendelijkheid.",
        "category": "development",
        "prompt": """Schrijf een Nederlands artikel van 1200-1500 woorden over Jira vs Linear vs ClickUp in 2026. Behandel precies 7 tools: Jira, Linear, ClickUp, Asana, Monday Dev, Shortcut, Plane (open-source).

Structuur:
- Introductie: projectmanagement voor developers in 2026 — AI-sprintplanning, dev-first UX, integraties met GitHub/GitLab, de opkomst van snelle alternatieven
- Per tool een ## kop met: beschrijving, prijsrange (EUR/gebruiker/maand), beste use case (klein team, scale-up, enterprise, open-source), plus- en minpunten, verdict (1-2 zinnen)
- Een markdown-vergelijkingstabel met alle 7 tools: naam, prijs vanaf (EUR), beste voor, GitHub-integratie kwaliteit, score (1-5)
- Conclusie: welke tool voor wie (startup 2-10 devs, scale-up 10-50, enterprise, open-source team, remote team, solo developer)
- 3 FAQ-vragen over projectmanagement voor developers

Focus op Nederlandse/Belgische tech-teams. Plane als open-source Jira-alternatief benoemen. Prijzen in EUR. Vloeiend Nederlands. Concrete setup-tips.""",
        "tools": [
            {"name": "Linear", "verdict": "Snelste en meest developer-vriendelijke interface — gebouwd voor moderne tech-teams met toetsenbord-first UX", "priceRange": "EUR 0-13/gebruiker/mnd", "bestFor": "Startups & Scale-ups", "rating": 4.8, "affiliateLink": "https://linear.app/?ref=aitoolsnl"},
            {"name": "Jira", "verdict": "De onbetwiste enterprise-standaard met ongeëvenaarde workflows en Atlassian-ecosysteem", "priceRange": "EUR 0-15/gebruiker/mnd", "bestFor": "Enterprise & Grote teams", "rating": 4.3, "affiliateLink": "https://atlassian.com/jira/?ref=aitoolsnl"},
            {"name": "ClickUp", "verdict": "Meest veelzijdige all-in-one met docs, whiteboards en time tracking naast projectmanagement", "priceRange": "EUR 0-12/gebruiker/mnd", "bestFor": "All-in-one teams", "rating": 4.5, "affiliateLink": "https://clickup.com/?ref=aitoolsnl"},
            {"name": "Asana", "verdict": "Beste voor cross-functionele teams die developers en niet-developers samenbrengen", "priceRange": "EUR 0-25/gebruiker/mnd", "bestFor": "Cross-functioneel", "rating": 4.4, "affiliateLink": "https://asana.com/?ref=aitoolsnl"},
            {"name": "Monday Dev", "verdict": "Visueel sterk platform met developer-specifieke boards en GitHub/GitLab integraties", "priceRange": "EUR 10-20/gebruiker/mnd", "bestFor": "Visuele teams", "rating": 4.2, "affiliateLink": "https://monday.com/dev/?ref=aitoolsnl"},
            {"name": "Shortcut", "verdict": "Voormalig Clubhouse — gebouwd door developers voor developers met focus op eenvoud en snelheid", "priceRange": "EUR 0-10/gebruiker/mnd", "bestFor": "Agile startups", "rating": 4.3, "affiliateLink": "https://shortcut.com/?ref=aitoolsnl"},
            {"name": "Plane", "verdict": "Open-source Jira-alternatief met moderne UI — self-hosten of cloud, groeiende Europese community", "priceRange": "EUR 0/mnd (gratis/open-source)", "bestFor": "Open-source & Privacy", "rating": 4.0, "affiliateLink": "https://plane.so/?ref=aitoolsnl"},
        ],
        "related": pick_related("jira-vs-linear-vs-clickup-2026", ALL_SLUGS, 3)
    },
    {
        "slug": "exact-online-vs-moneybird-vs-snelstart-2026",
        "title": "Exact Online vs Moneybird vs Snelstart 2026: beste Nederlandse boekhoudsoftware",
        "description": "Exact Online, Moneybird of Snelstart in 2026? Vergelijk de beste Nederlandse boekhoudpakketten op prijs, gebruiksgemak, koppeling Belastingdienst, e-facturatie en geschiktheid voor ZZP, MKB en accountants.",
        "category": "business",
        "prompt": """Schrijf een Nederlands artikel van 1200-1500 woorden over Exact Online vs Moneybird vs Snelstart in 2026. Behandel precies 7 tools: Exact Online, Moneybird, Snelstart, e-Boekhouden, Jortt, Visma eAccounting, InformerOnline.

Structuur:
- Introductie: boekhoudsoftware in 2026 — verplichte e-facturatie (Peppol), AI-boekhouders, btw-aangifte automatisering, het Nederlandse boekhoudlandschap
- Per tool een ## kop met: beschrijving, prijsrange (EUR/maand), beste use case (ZZP, MKB tot 10 man, MKB 10+, accountant, starter), plus- en minpunten, verdict (1-2 zinnen)
- Een markdown-vergelijkingstabel met alle 7 tools: naam, prijs vanaf (EUR/maand), beste voor, koppeling Belastingdienst/Peppol, score (1-5)
- Conclusie: welke boekhoudsoftware voor wie (ZZP/freelancer, klein MKB 2-10, groeiend MKB 10-50, e-commerce, internationaal, administratiekantoor, prijsbewuste starter)
- 3 FAQ-vragen over Nederlandse boekhoudsoftware

ESSENTIEEL: Focus puur op Nederlandse markt. Benoem Peppol e-facturatie deadline. Alle prijzen in EUR/maand. Vloeiend Nederlands. Specifieke Belastingdienst-koppelingen benoemen per tool. Geef concrete adviezen voor de Nederlandse ZZP'er en MKB'er.""",
        "tools": [
            {"name": "Exact Online", "verdict": "Meest complete MKB-oplossing met sterke rapportages, multi-currency en accountantskoppeling", "priceRange": "EUR 30-110/mnd", "bestFor": "MKB 5-100+ medewerkers", "rating": 4.5, "affiliateLink": "https://exact.com/?ref=aitoolsnl"},
            {"name": "Moneybird", "verdict": "Beste UX en automatisering voor ZZP en klein MKB — facturen, bankkoppeling en btw in één strakke interface", "priceRange": "EUR 14-42/mnd", "bestFor": "ZZP & Klein MKB", "rating": 4.7, "affiliateLink": "https://moneybird.com/?ref=aitoolsnl"},
            {"name": "Snelstart", "verdict": "Betrouwbare veteraan met sterke accountantsnetwerk en uitgebreide functionaliteit voor groeiende bedrijven", "priceRange": "EUR 25-60/mnd", "bestFor": "MKB & Accountants", "rating": 4.3, "affiliateLink": "https://snelstart.nl/?ref=aitoolsnl"},
            {"name": "e-Boekhouden", "verdict": "Beste prijs-kwaliteit voor starters met volledige functionaliteit tegen lage kosten", "priceRange": "EUR 7-30/mnd", "bestFor": "Starters & Budget", "rating": 4.4, "affiliateLink": "https://e-boekhouden.nl/?ref=aitoolsnl"},
            {"name": "Jortt", "verdict": "Eenvoudigste boekhoudsoftware met gratis variant — ideaal voor ZZP'ers die net beginnen", "priceRange": "EUR 0-20/mnd", "bestFor": "Startende ZZP'ers", "rating": 4.2, "affiliateLink": "https://jortt.nl/?ref=aitoolsnl"},
            {"name": "Visma eAccounting", "verdict": "Scandinavische kracht met groeiende Nederlandse aanwezigheid — sterk in automatisering en AI", "priceRange": "EUR 20-60/mnd", "bestFor": "Automatisering & Groei", "rating": 4.1, "affiliateLink": "https://visma.com/eaccounting/?ref=aitoolsnl"},
            {"name": "InformerOnline", "verdict": "Cloud-gebaseerd met realtime dashboards en sterke integraties met banken en webshops", "priceRange": "EUR 20-50/mnd", "bestFor": "E-commerce & Realtime", "rating": 4.0, "affiliateLink": "https://informer.nl/?ref=aitoolsnl"},
        ],
        "related": pick_related("exact-online-vs-moneybird-vs-snelstart-2026", ALL_SLUGS, 3)
    },
    {
        "slug": "github-vs-gitlab-vs-bitbucket-2026",
        "title": "GitHub vs GitLab vs Bitbucket 2026: beste code-hosting en CI/CD platform voor developers",
        "description": "GitHub, GitLab of Bitbucket in 2026? Vergelijk de beste DevSecOps-platforms op code hosting, CI/CD, AI-coding agents, prijs en geschiktheid voor Nederlandse ontwikkelteams.",
        "category": "development",
        "prompt": """Schrijf een Nederlands artikel van 1200-1500 woorden over GitHub vs GitLab vs Bitbucket in 2026. Behandel precies 7 tools: GitHub, GitLab, Bitbucket, Azure DevOps, Gitea, SourceForge, Codeberg.

Structuur:
- Introductie: code-hosting in 2026 — AI-coding agents (Copilot, Duo, etc.), geïntegreerde CI/CD, DevSecOps, EU-soevereiniteit en privacy-overwegingen
- Per tool een ## kop met: beschrijving, prijsrange (EUR/gebruiker/maand), beste use case (startup, enterprise, open-source, privacy-bewust, Microsoft-ecosysteem), plus- en minpunten, verdict (1-2 zinnen)
- Een markdown-vergelijkingstabel met alle 7 tools: naam, prijs vanaf (EUR), beste voor, AI-assistent beschikbaar, EU-hosting optie, score (1-5)
- Conclusie: welk platform voor wie (solo developer, startup 2-10, scale-up, enterprise, open-source project, EU-privacy-bewust team, Microsoft-shop)
- 3 FAQ-vragen over code-hosting en CI/CD

Focus op Nederlandse/Europese context. Codeberg als Duits/EU privacy-alternatief benoemen. Azure DevOps voor Microsoft-teams. Vloeiend Nederlands. Prijzen in EUR.""",
        "tools": [
            {"name": "GitHub", "verdict": "De wereldstandaard met GitHub Copilot, Actions en het grootste ecosysteem — onmisbaar in 2026", "priceRange": "EUR 0-20/gebruiker/mnd", "bestFor": "Open-source & Alle teams", "rating": 4.8, "affiliateLink": "https://github.com/?ref=aitoolsnl"},
            {"name": "GitLab", "verdict": "Beste geïntegreerde DevSecOps-platform met eigen CI/CD, container registry en GitLab Duo AI", "priceRange": "EUR 0-29/gebruiker/mnd", "bestFor": "DevSecOps & Self-host", "rating": 4.6, "affiliateLink": "https://gitlab.com/?ref=aitoolsnl"},
            {"name": "Bitbucket", "verdict": "Naadloze Atlassian-integratie met Jira en Confluence — sterk voor bestaande Atlassian-teams", "priceRange": "EUR 0-6/gebruiker/mnd", "bestFor": "Atlassian-ecosysteem", "rating": 4.2, "affiliateLink": "https://bitbucket.org/?ref=aitoolsnl"},
            {"name": "Azure DevOps", "verdict": "Enterprise-grade met diepe Microsoft-stack integratie, geavanceerde boards en testplannen", "priceRange": "EUR 0-50/gebruiker/mnd", "bestFor": "Enterprise & Microsoft", "rating": 4.3, "affiliateLink": "https://azure.microsoft.com/devops/?ref=aitoolsnl"},
            {"name": "Gitea", "verdict": "Lichtgewicht open-source Git-service — zelf te hosten op een Raspberry Pi of kleine VPS", "priceRange": "EUR 0/mnd (self-host)", "bestFor": "Self-host & Privacy", "rating": 4.1, "affiliateLink": "https://gitea.com/?ref=aitoolsnl"},
            {"name": "SourceForge", "verdict": "Grootste open-source mirror network — nog steeds relevant voor binary releases en mirrors", "priceRange": "EUR 0/mnd (gratis)", "bestFor": "Open-source Mirroring", "rating": 3.3, "affiliateLink": "https://sourceforge.net/?ref=aitoolsnl"},
            {"name": "Codeberg", "verdict": "Duits/EU privacy-alternatief voor GitHub — non-profit, geen tracking, volledig AVG-compliant", "priceRange": "EUR 0/mnd (gratis/donatie)", "bestFor": "EU Privacy & AVG", "rating": 3.8, "affiliateLink": "https://codeberg.org/?ref=aitoolsnl"},
        ],
        "related": pick_related("github-vs-gitlab-vs-bitbucket-2026", ALL_SLUGS, 3)
    },
    {
        "slug": "vercel-vs-netlify-vs-cloudflare-pages-2026",
        "title": "Vercel vs Netlify vs Cloudflare Pages 2026: beste hosting voor moderne webapps",
        "description": "Vercel, Netlify of Cloudflare Pages in 2026? Vergelijk de beste Jamstack en serverless hostingplatforms op snelheid, prijs, edge-functies, AI-integraties en developer experience.",
        "category": "development",
        "prompt": """Schrijf een Nederlands artikel van 1200-1500 woorden over Vercel vs Netlify vs Cloudflare Pages in 2026. Behandel precies 7 tools: Vercel, Netlify, Cloudflare Pages, Railway, Render, Fly.io, Deno Deploy.

Structuur:
- Introductie: webhosting in 2026 — edge computing, serverless, AI-gestuurde deploys, de evolutie van Jamstack naar volledige full-stack frameworks
- Per tool een ## kop met: beschrijving, prijsrange (EUR/maand), beste use case (Next.js apps, statische sites, API's, full-stack, hobby-projecten, enterprise), plus- en minpunten, verdict (1-2 zinnen)
- Een markdown-vergelijkingstabel met alle 7 tools: naam, gratis tier, prijs vanaf (EUR), beste voor, edge-functies beschikbaar, score (1-5)
- Conclusie: welke hosting voor wie (hobby-dev, startup MVP, scale-up, enterprise Next.js, API-heavy app, budget-bewuste developer, performance-freak)
- 3 FAQ-vragen over moderne webhosting

Focus op Nederlandse/Europese developers. Edge-locaties in EU benoemen. Prijzen in EUR. Vloeiend Nederlands. Concrete vergelijkingen van cold start tijden en gratis tier limieten.""",
        "tools": [
            {"name": "Vercel", "verdict": "Beste developer experience voor Next.js en SvelteKit met v8 isolates, AI SDK en onverslaanbare edge-functies", "priceRange": "EUR 0-20/mnd (pro)", "bestFor": "Next.js & Frontend teams", "rating": 4.8, "affiliateLink": "https://vercel.com/?ref=aitoolsnl"},
            {"name": "Netlify", "verdict": "Beste voor Jamstack-sites met Netlify Functions, Forms en een volwassen add-on ecosysteem", "priceRange": "EUR 0-19/mnd (pro)", "bestFor": "Jamstack & Statische sites", "rating": 4.5, "affiliateLink": "https://netlify.com/?ref=aitoolsnl"},
            {"name": "Cloudflare Pages", "verdict": "Beste prijs-kwaliteit met unlimited bandwidth, Workers integratie en Cloudflare's edge-netwerk", "priceRange": "EUR 0-5/mnd (pro)", "bestFor": "Performance & Budget", "rating": 4.6, "affiliateLink": "https://pages.cloudflare.com/?ref=aitoolsnl"},
            {"name": "Railway", "verdict": "Eenvoudigste full-stack hosting met databases — deploys van repos en Docker met één klik", "priceRange": "EUR 0-20/mnd (starter)", "bestFor": "Full-stack & Databases", "rating": 4.4, "affiliateLink": "https://railway.app/?ref=aitoolsnl"},
            {"name": "Render", "verdict": "Beste PaaS-alternatief voor Heroku met managed PostgreSQL, Redis en cron jobs", "priceRange": "EUR 0-19/mnd (starter)", "bestFor": "PaaS & Managed services", "rating": 4.3, "affiliateLink": "https://render.com/?ref=aitoolsnl"},
            {"name": "Fly.io", "verdict": "Apps dichtbij gebruikers met edge-deployments op 6 continenten — ideaal voor latency-gevoelige apps", "priceRange": "EUR 0-30/mnd (pay-as-you-go)", "bestFor": "Global & Low-latency", "rating": 4.2, "affiliateLink": "https://fly.io/?ref=aitoolsnl"},
            {"name": "Deno Deploy", "verdict": "Supersnelle edge-functies met native TypeScript en Web API's — perfect voor API's en microservices", "priceRange": "EUR 0-10/mnd (starter)", "bestFor": "Edge API's & Microservices", "rating": 4.1, "affiliateLink": "https://deno.com/deploy/?ref=aitoolsnl"},
        ],
        "related": pick_related("vercel-vs-netlify-vs-cloudflare-pages-2026", ALL_SLUGS, 3)
    },
]


def call_gemini(prompt, max_retries=5):
    url = f"{BASE_URL}?key={API_KEY}"
    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {"temperature": 0.7, "maxOutputTokens": 4096}
    }
    for attempt in range(max_retries):
        try:
            resp = requests.post(url, json=payload, timeout=120,
                                 headers={"Content-Type": "application/json"})
            if resp.status_code == 429:
                wait = 20 * (attempt + 1)
                print(f"  Rate-limited (429), waiting {wait}s...")
                time.sleep(wait)
                continue
            if resp.status_code == 503:
                print(f"  503 overload (attempt {attempt+1})")
                time.sleep(20)
                continue
            if resp.status_code != 200:
                print(f"  HTTP {resp.status_code}: {resp.text[:200]}")
                if attempt < max_retries - 1:
                    time.sleep(10)
                    continue
                return None
            data = resp.json()
            return data["candidates"][0]["content"]["parts"][0]["text"]
        except Exception as e:
            print(f"  Exception: {e}")
            if attempt < max_retries - 1:
                time.sleep(8)
    return None


def build_article(defn, body_text):
    avg_rating = round(sum(t["rating"] for t in defn["tools"]) / len(defn["tools"]), 1)
    data = {
        "title": defn["title"],
        "slug": defn["slug"],
        "description": defn["description"],
        "category": defn["category"],
        "rating": avg_rating,
        "priceRange": "EUR 0-100/mnd",
        "pros": [
            "Uitgebreide vergelijking van de beste tools in deze categorie voor 2026",
            "Duidelijke prijsranges, verdicts en praktische use cases per tool",
            "Nederlandstalig en relevant voor de Nederlandse markt",
        ],
        "cons": [
            "Prijzen en features kunnen wijzigen — check de actuele aanbieder",
            "Niet elke tool is dagelijks getest in de Nederlandse praktijk",
            "Sommige AI-features zijn nog in actieve ontwikkeling of beta",
        ],
        "affiliateLinks": [
            "https://www.beehiiv.com/?via=anonymous-operator",
        ],
        "date": str(date.today()),
        "modelYear": 2026,
        "featuredTool": defn["tools"][0]["name"],
        "readingTime": "8 min",
        "tools": defn["tools"],
        "related": defn["related"],
        "draft": False,
        "faq": [
            {"q": f"Wat is de beste tool in {defn['title'].split(':')[0].strip()} in 2026?",
             "a": f"Dat hangt af van je specifieke behoeften en budget. Voor de meeste gebruikers is {defn['tools'][0]['name']} een uitstekende start vanwege de balans tussen functionaliteit, prijs en gebruiksvriendelijkheid. Lees de volledige vergelijking hierboven voor een gedetailleerd advies per tool."},
            {"q": "Zijn er gratis alternatieven beschikbaar in 2026?",
             "a": "Ja, verschillende tools in onze vergelijking hebben gratis tiers of freemium modellen. Deze zijn perfect om mee te beginnen en te testen voordat je upgrade naar een betaald abonnement."},
            {"q": "Hoe kies ik de juiste tool voor mijn situatie?",
             "a": "Begin met je primaire use case, budget en aantal gebruikers. Gebruik de vergelijkingstabel hierboven om te filteren op score, prijs en 'beste voor' — dan vind je snel de tool die bij jouw situatie past."},
        ]
    }
    fm = yaml.dump(data, allow_unicode=True, default_flow_style=False, sort_keys=False, width=120)
    return f"---\n{fm}---\n{body_text}"


def main():
    global ALL_SLUGS
    # Refresh slug list in case previous article generation added new ones
    ALL_SLUGS = [f.replace(".md", "") for f in sorted(os.listdir(ARTICLES_DIR)) if f.endswith(".md")]

    os.makedirs(ARTICLES_DIR, exist_ok=True)
    generated = 0
    failed = 0
    skipped = 0

    for i, defn in enumerate(NEW_ARTICLES):
        print(f"[{i+1}/5] {defn['slug']}")

        out_path = os.path.join(ARTICLES_DIR, f"{defn['slug']}.md")
        if os.path.exists(out_path):
            print(f"  Already exists, skipping")
            skipped += 1
            continue

        body = call_gemini(defn["prompt"])
        if body is None:
            print(f"  FAILED — API exhausted")
            failed += 1
            # Refresh ALL_SLUGS for next article (if any)
            ALL_SLUGS = [f.replace(".md", "") for f in sorted(os.listdir(ARTICLES_DIR)) if f.endswith(".md")]
            continue

        # Recompute related with potentially new slugs
        defn["related"] = pick_related(defn["slug"], ALL_SLUGS, 3)

        full = build_article(defn, body)
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(full)

        generated += 1
        word_count = len(body.split())
        print(f"  Written: {out_path} ({len(full)} chars, ~{word_count} words)")

        # Refresh slug list after each write
        ALL_SLUGS = [f.replace(".md", "") for f in sorted(os.listdir(ARTICLES_DIR)) if f.endswith(".md")]

        if i < len(NEW_ARTICLES) - 1:
            time.sleep(5)

    print(f"\n=== SUMMARY ===")
    print(f"Generated: {generated}, Skipped: {skipped}, Failed: {failed}")
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
