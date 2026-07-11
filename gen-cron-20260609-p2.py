#!/usr/bin/env python3
"""Generate remaining 4 articles one at a time (batch1 timed out)."""
import os, time, sys, requests, yaml
from datetime import date

key_file = os.path.expanduser("~/.hermes/private/gemini-api-key")
with open(key_file) as f:
    API_KEY = f.read().strip()

BASE_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent"
ARTICLES_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "src/content/articles")

def pick_related(new_slug, n=3):
    slugs = sorted([f.replace(".md", "") for f in os.listdir(ARTICLES_DIR) if f.endswith(".md")])
    candidates = [s for s in slugs if s != new_slug]
    return candidates[:n]

def call_gemini(prompt):
    url = f"{BASE_URL}?key={API_KEY}"
    payload = {"contents": [{"parts": [{"text": prompt}]}], "generationConfig": {"temperature": 0.7, "maxOutputTokens": 4096}}
    for attempt in range(8):
        try:
            resp = requests.post(url, json=payload, timeout=120, headers={"Content-Type": "application/json"})
            if resp.status_code == 429:
                print(f"  429 wait {35*(attempt+1)}s")
                time.sleep(35*(attempt+1))
                continue
            if resp.status_code in (503, 500):
                print(f"  {resp.status_code} retry in 30s")
                time.sleep(30)
                continue
            if resp.status_code != 200:
                print(f"  HTTP {resp.status_code}: {resp.text[:200]}")
                return None
            return resp.json()["candidates"][0]["content"]["parts"][0]["text"]
        except Exception as e:
            print(f"  Exception: {e}")
            time.sleep(15)
    return None

def build_article(defn, body_text):
    avg = round(sum(t["rating"] for t in defn["tools"]) / len(defn["tools"]), 1)
    data = {
        "title": defn["title"], "slug": defn["slug"], "description": defn["description"],
        "category": defn["category"], "rating": avg, "priceRange": "EUR 0-100/mnd",
        "pros": ["Uitgebreide 2026 vergelijking", "Duidelijke prijsranges en use cases", "Nederlandstalig"],
        "cons": ["Prijzen kunnen wijzigen", "AI-features in ontwikkeling", "Niet alles dagelijks getest"],
        "affiliateLinks": ["https://www.beehiiv.com/"],
        "date": str(date.today()), "modelYear": 2026,
        "featuredTool": defn["tools"][0]["name"], "readingTime": "8 min",
        "tools": defn["tools"], "related": pick_related(defn["slug"], 3),
        "draft": False,
        "faq": [
            {"q": "Wat is de beste tool?", "a": "Dat hangt af van je situatie. " + defn["tools"][0]["name"] + " is voor de meeste gebruikers een prima startpunt."},
            {"q": "Zijn er gratis alternatieven?", "a": "Ja, meerdere tools hebben gratis tiers. Perfect om te beginnen."},
            {"q": "Hoe kies ik de juiste tool?", "a": "Begin met je use case en budget. Filter de tabel op score en prijs."},
        ]
    }
    fm = yaml.dump(data, allow_unicode=True, default_flow_style=False, sort_keys=False, width=120)
    return f"---\n{fm}---\n{body_text}"

# Remaining 4 topics
TOPICS = [
    {
        "slug": "datadog-vs-grafana-vs-new-relic-vs-dynatrace-2026",
        "title": "Datadog vs Grafana vs New Relic vs Dynatrace 2026: beste monitoring en observability tools",
        "description": "Datadog, Grafana, New Relic of Dynatrace in 2026? Vergelijk de beste monitoring- en observability-platforms op features, prijs, AIOps en geschiktheid voor Nederlandse DevOps teams.",
        "category": "development",
        "prompt": """Schrijf een Nederlands artikel van 1200-1500 woorden over Datadog vs Grafana vs New Relic vs Dynatrace in 2026. Behandel precies 7 tools: Datadog, Grafana Cloud, New Relic, Dynatrace, Honeycomb, SigNoz, Checkmk.

Structuur:
- Introductie: monitoring 2026 — OpenTelemetry standaard, AIOps, FinOps, cloud-native observability
- Per tool een ## kop: beschrijving, prijs (EUR/maand bij typisch gebruik), beste use case, plus- en minpunten, verdict
- Markdown vergelijkingstabel: naam, prijsmodel, beste voor, OpenTelemetry support, AIOps, score (1-5)
- Conclusie: welke voor startup, scale-up, enterprise, SRE-team, budget-bewust, full-stack, EU-data-residency
- 3 FAQ's

Focus op Nederlandse/Europese relevantie — EU hosting, AVG. SigNoz als open-source alternatief, Checkmk als Europees. Prijzen ook in EUR noemen waar mogelijk. Vloeiend Nederlands.""",
        "tools": [
            {"name": "Datadog", "verdict": "Breedste observability-platform — 800+ integraties, AI-driven alerts en dashboards", "priceRange": "EUR $15-45/host/mnd", "bestFor": "Full-stack & Enterprise", "rating": 4.7, "affiliateLink": "https://datadoghq.com/?ref=aitoolsnl"},
            {"name": "Grafana Cloud", "verdict": "Beste open-source ecosysteem met Loki/Mimir/Tempo — meest flexibel", "priceRange": "EUR 0-29/gebruiker/mnd", "bestFor": "Open-source & Maatwerk", "rating": 4.5, "affiliateLink": "https://grafana.com/?ref=aitoolsnl"},
            {"name": "New Relic", "verdict": "Beste all-in-one met 100GB gratis — sterk in APM en AI-analyse", "priceRange": "EUR 0-49/gebruiker/mnd", "bestFor": "APM & Full-stack teams", "rating": 4.4, "affiliateLink": "https://newrelic.com/?ref=aitoolsnl"},
            {"name": "Dynatrace", "verdict": "Beste AIOps met Davis AI-engine — automatische root-cause analyse", "priceRange": "EUR 60-120/host/mnd", "bestFor": "Enterprise & AIOps", "rating": 4.6, "affiliateLink": "https://dynatrace.com/?ref=aitoolsnl"},
            {"name": "Honeycomb", "verdict": "Beste voor high-cardinality data en SRE-teams — event-driven observability", "priceRange": "EUR 130-400/mnd", "bestFor": "SRE & Microservices", "rating": 4.3, "affiliateLink": "https://honeycomb.io/?ref=aitoolsnl"},
            {"name": "SigNoz", "verdict": "Beste open-source Datadog-alternatief — OpenTelemetry-native, zelf te hosten", "priceRange": "EUR 0 (self-host) of $199/mnd cloud", "bestFor": "Open-source & Budget", "rating": 4.0, "affiliateLink": "https://signoz.io/?ref=aitoolsnl"},
            {"name": "Checkmk", "verdict": "Duitse monitoring met sterke IT-infrastructuur focus — AVG-compliant", "priceRange": "EUR 0-60/host/mnd", "bestFor": "EU Compliance & IT Ops", "rating": 4.1, "affiliateLink": "https://checkmk.com/?ref=aitoolsnl"},
        ],
    },
    {
        "slug": "auth0-vs-clerk-vs-supabase-auth-vs-firebase-auth-2026",
        "title": "Auth0 vs Clerk vs Supabase Auth vs Firebase Auth 2026: beste authenticatie voor developers",
        "description": "Auth0, Clerk, Supabase Auth of Firebase Auth in 2026? Vergelijk de beste auth-platforms op prijs, features, developer experience en AVG-compliance voor Nederlandse ontwikkelaars.",
        "category": "development",
        "prompt": """Schrijf een Nederlands artikel van 1200-1500 woorden over Auth0 vs Clerk vs Supabase Auth vs Firebase Auth in 2026. Behandel precies 7 tools: Auth0 (Okta), Clerk, Supabase Auth, Firebase Auth, WorkOS, Kinde, Keycloak.

Structuur:
- Introductie: authenticatie 2026 — passkeys, passwordless, SSO, social login, EU data residency
- Per tool een ## kop: beschrijving, prijs (EUR/maand bij 1000-5000 MAU), beste use case, plus- en minpunten, verdict
- Markdown vergelijkingstabel: naam, gratis MAU, prijs vanaf, passkeys, SSO/SAML, EU-hosting, score (1-5)
- Conclusie: voor side project, startup, scale-up, enterprise B2B SaaS, e-commerce, EU-privacy-first, budget
- 3 FAQ's

Belangrijk voor NL devs: AVG, EU data residency, DigiD/eHerkenning mogelijkheden. Keycloak als EU open-source alternatief. Vloeiend Nederlands.""",
        "tools": [
            {"name": "Auth0 (Okta)", "verdict": "Meest complete enterprise auth — 25k gratis MAU, alle protocollen, uitgebreide security", "priceRange": "EUR 0-23/maand (tot 25k MAU)", "bestFor": "Enterprise & B2B SaaS", "rating": 4.6, "affiliateLink": "https://auth0.com/?ref=aitoolsnl"},
            {"name": "Clerk", "verdict": "Beste DX voor React/Next.js — drop-in components, mooie UI, snel setup", "priceRange": "EUR 0-25/maand (tot 10k MAU)", "bestFor": "React/Next.js apps", "rating": 4.7, "affiliateLink": "https://clerk.com/?ref=aitoolsnl"},
            {"name": "Supabase Auth", "verdict": "Naadloos met PostgreSQL en Row Level Security — beste voor full-stack apps", "priceRange": "EUR 0-25/maand (tot 100k MAU)", "bestFor": "Full-stack & Supabase", "rating": 4.5, "affiliateLink": "https://supabase.com/?ref=aitoolsnl"},
            {"name": "Firebase Auth", "verdict": "Gratis en schaalt oneindig — perfect voor mobile/web apps met Google-ecosysteem", "priceRange": "EUR 0 (gratis, onbeperkt)", "bestFor": "Mobile & Google Cloud", "rating": 4.4, "affiliateLink": "https://firebase.google.com/?ref=aitoolsnl"},
            {"name": "WorkOS", "verdict": "Enterprise SSO in een dag — SAML, SCIM, audit logs voor B2B SaaS", "priceRange": "EUR 0-99/maand", "bestFor": "B2B SaaS Enterprise", "rating": 4.3, "affiliateLink": "https://workos.com/?ref=aitoolsnl"},
            {"name": "Kinde", "verdict": "Moderne auth met gratis onbeperkte MAU — sterke developer-focus", "priceRange": "EUR 0-25/maand (onbeperkte MAU)", "bestFor": "Startups & Indie devs", "rating": 4.2, "affiliateLink": "https://kinde.com/?ref=aitoolsnl"},
            {"name": "Keycloak", "verdict": "Beste open-source self-host auth — volledige controle, AVG-proof, EU-made", "priceRange": "EUR 0 (self-host, open-source)", "bestFor": "Self-host & EU Privacy", "rating": 4.0, "affiliateLink": "https://keycloak.org/?ref=aitoolsnl"},
        ],
    },
    {
        "slug": "launchdarkly-vs-configcat-vs-flagsmith-vs-growthbook-2026",
        "title": "LaunchDarkly vs ConfigCat vs Flagsmith vs GrowthBook 2026: beste feature flags en feature management",
        "description": "LaunchDarkly, ConfigCat, Flagsmith of GrowthBook in 2026? Vergelijk de beste feature flag-platforms op prijs, features, integraties en AVG-compliance voor Nederlandse dev teams.",
        "category": "development",
        "prompt": """Schrijf een Nederlands artikel van 1200-1500 woorden over LaunchDarkly vs ConfigCat vs Flagsmith vs GrowthBook in 2026. Behandel precies 7 tools: LaunchDarkly, ConfigCat, Flagsmith, GrowthBook, Unleash, PostHog Feature Flags, Split.io.

Structuur:
- Introductie: feature flags 2026 — trunk-based development, progressive delivery, canary releases, A/B testing integratie
- Per tool een ## kop: beschrijving, prijs (EUR/maand bij typisch team), beste use case, plus- en minpunten, verdict
- Markdown vergelijkingstabel: naam, gratis seats, prijs vanaf, self-host optie, A/B testing, EU-hosting, score (1-5)
- Conclusie: voor startup, scale-up, enterprise, EU-compliance, open-source, experiment-driven, budget
- 3 FAQ's

Europese alternatieven benadrukken: ConfigCat (Hongaars), Flagsmith (UK, self-host), Unleash (Noors). AVG en EU data residency relevant. Vloeiend Nederlands.""",
        "tools": [
            {"name": "LaunchDarkly", "verdict": "Beste enterprise feature management — streaming updates, workflows, experimentatie op schaal", "priceRange": "EUR 0-50/seat/mnd", "bestFor": "Enterprise & Experimentatie", "rating": 4.7, "affiliateLink": "https://launchdarkly.com/?ref=aitoolsnl"},
            {"name": "ConfigCat", "verdict": "Beste EU-alternatief — Hongaars, AVG-compliant, eenvoudige prijsstelling", "priceRange": "EUR 0-25/maand (onbeperkte seats)", "bestFor": "EU Compliance & Teams", "rating": 4.5, "affiliateLink": "https://configcat.com/?ref=aitoolsnl"},
            {"name": "Flagsmith", "verdict": "Beste open-source met remote config — volledige self-host of cloud", "priceRange": "EUR 0-45/maand (onbeperkte seats)", "bestFor": "Open-source & Maatwerk", "rating": 4.4, "affiliateLink": "https://flagsmith.com/?ref=aitoolsnl"},
            {"name": "GrowthBook", "verdict": "Beste feature flags + A/B testing in één — data-gedreven experimentatie", "priceRange": "EUR 0-20/seat/mnd (self-host gratis)", "bestFor": "A/B Testing & Data teams", "rating": 4.3, "affiliateLink": "https://growthbook.io/?ref=aitoolsnl"},
            {"name": "Unleash", "verdict": "Beste open-source enterprise — Noors, 10k+ sterren GitHub, sterke community", "priceRange": "EUR 0 (self-host) of $80/mnd cloud", "bestFor": "Enterprise Self-host", "rating": 4.4, "affiliateLink": "https://getunleash.io/?ref=aitoolsnl"},
            {"name": "PostHog Feature Flags", "verdict": "Flags + analytics in één — perfect voor product teams met bestaande PostHog", "priceRange": "EUR 0 (tot 1M events/mnd)", "bestFor": "Product Analytics teams", "rating": 4.2, "affiliateLink": "https://posthog.com/?ref=aitoolsnl"},
            {"name": "Split.io", "verdict": "Feature flags met sterke impact analyse — enterprise experimentatie platform", "priceRange": "EUR 33-60/seat/mnd", "bestFor": "Enterprise Experimentatie", "rating": 4.1, "affiliateLink": "https://split.io/?ref=aitoolsnl"},
        ],
    },
    {
        "slug": "optimizely-vs-vwo-vs-ab-tasty-vs-convert-2026",
        "title": "Optimizely vs VWO vs AB Tasty vs Convert 2026: beste A/B testing en CRO tools",
        "description": "Optimizely, VWO, AB Tasty of Convert in 2026? Vergelijk de beste A/B testing en conversie-optimalisatie platforms op features, prijs, AI en AVG-compliance voor Nederlandse marketeers.",
        "category": "business",
        "prompt": """Schrijf een Nederlands artikel van 1200-1500 woorden over Optimizely vs VWO vs AB Tasty vs Convert in 2026. Behandel precies 7 tools: Optimizely, VWO, AB Tasty, Convert Experiences, Crazy Egg, Kameleoon, PostHog Experiments.

Structuur:
- Introductie: A/B testing 2026 — AI-gestuurde personalisatie, server-side testing, cookieloze tracking, NL/EU privacy
- Per tool een ## kop: beschrijving, prijs (EUR/maand bij start), beste use case, plus- en minpunten, verdict
- Markdown vergelijkingstabel: naam, prijs vanaf, beste voor, AI-personalisatie, server-side, AVG-compliant, score (1-5)
- Conclusie: voor startup webshop, MKB marketingteam, enterprise e-commerce, budget-bewust, AI-first, privacy-first
- 3 FAQ's

Let op: Google Optimize is gestopt (2023). Europese tools benadrukken: AB Tasty (Frans), Kameleoon (Frans). AVG/cookieloze tracking relevant. Server-side testing voor betrouwbare data. Vloeiend Nederlands.""",
        "tools": [
            {"name": "Optimizely", "verdict": "Beste enterprise experimentatieplatform — full-stack, feature flags + web testing", "priceRange": "EUR 36.000+/jaar", "bestFor": "Enterprise & Full-stack", "rating": 4.6, "affiliateLink": "https://optimizely.com/?ref=aitoolsnl"},
            {"name": "VWO", "verdict": "Beste all-in-one CRO platform — testing + heatmaps + session recordings + surveys", "priceRange": "EUR 200-500/mnd", "bestFor": "MKB Marketing teams", "rating": 4.5, "affiliateLink": "https://vwo.com/?ref=aitoolsnl"},
            {"name": "AB Tasty", "verdict": "Beste EU-alternatief — Frans, AVG-compliant, sterke AI-personalisatie", "priceRange": "EUR 300-1500/mnd", "bestFor": "EU E-commerce", "rating": 4.4, "affiliateLink": "https://abtasty.com/?ref=aitoolsnl"},
            {"name": "Convert Experiences", "verdict": "Beste prijs-kwaliteit — onbeperkte tests, privacy-first, geen data-sharing", "priceRange": "EUR 99-499/mnd", "bestFor": "Budget & Privacy", "rating": 4.2, "affiliateLink": "https://convert.com/?ref=aitoolsnl"},
            {"name": "Crazy Egg", "verdict": "Beste visuele analyse — heatmaps, scrollmaps en confetti reports op schaal", "priceRange": "EUR 29-99/mnd", "bestFor": "Visuele Analyse & MKB", "rating": 4.0, "affiliateLink": "https://crazyegg.com/?ref=aitoolsnl"},
            {"name": "Kameleoon", "verdict": "Frans AI-first platform — realtime personalisatie, sterke EU-compliance", "priceRange": "EUR 500-2000/mnd", "bestFor": "AI-personalisatie", "rating": 4.3, "affiliateLink": "https://kameleoon.com/?ref=aitoolsnl"},
            {"name": "PostHog Experiments", "verdict": "Open-source Google Optimize alternatief — feature flags + A/B testing + analytics", "priceRange": "EUR 0 (tot 1M events/mnd)", "bestFor": "Google Optimize vervanger", "rating": 4.1, "affiliateLink": "https://posthog.com/?ref=aitoolsnl"},
        ],
    },
]

gen = 0
for i, d in enumerate(TOPICS):
    out = os.path.join(ARTICLES_DIR, f"{d['slug']}.md")
    print(f"[{i+1}/4] {d['slug']}")
    if os.path.exists(out):
        print(f"  Skip — exists")
        continue
    body = call_gemini(d["prompt"])
    if body is None:
        print(f"  FAILED")
        continue
    full = build_article(d, body)
    with open(out, "w", encoding="utf-8") as f:
        f.write(full)
    gen += 1
    print(f"  OK — {len(body.split())} words")
    if i < len(TOPICS) - 1:
        time.sleep(12)

print(f"\n=== {gen}/4 generated ===")
