#!/usr/bin/env python3
"""Generate Optimizely article via Gemini API."""
import os, json, requests, yaml, sys
from datetime import date

# Read API key
with open(os.path.expanduser("~/.hermes/private/gemini-api-key")) as f:
    API_KEY = f.read().strip()

BASE_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent"
ARTICLES_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "src/content/articles")

prompt = """Schrijf een Nederlands artikel van 1200-1500 woorden over Optimizely vs VWO vs AB Tasty vs Convert in 2026. Behandel precies 7 tools: Optimizely, VWO, AB Tasty, Convert Experiences, Crazy Egg, Kameleoon, PostHog Experiments.

Structuur:
- Introductie: A/B testing 2026 — AI-gestuurde personalisatie, server-side testing, cookieloze tracking, NL/EU privacy
- Per tool een ## kop: beschrijving, prijs (EUR/maand bij start), beste use case, plus- en minpunten, verdict
- Markdown vergelijkingstabel: naam, prijs vanaf, beste voor, AI-personalisatie, server-side, AVG-compliant, score (1-5)
- Conclusie: voor startup webshop, MKB marketingteam, enterprise e-commerce, budget-bewust, AI-first, privacy-first
- 3 FAQ's

Let op: Google Optimize is gestopt (2023). Europese tools benadrukken: AB Tasty (Frans), Kameleoon (Frans). AVG/cookieloze tracking relevant. Server-side testing voor betrouwbare data. Vloeiend Nederlands."""

url = f"{BASE_URL}?key={API_KEY}"
payload = {
    "contents": [{"parts": [{"text": prompt}]}],
    "generationConfig": {"temperature": 0.7, "maxOutputTokens": 8192}
}

print("Calling Gemini API...")
resp = requests.post(url, json=payload, timeout=180, headers={"Content-Type": "application/json"})
if resp.status_code != 200:
    print(f"HTTP {resp.status_code}: {resp.text[:500]}")
    sys.exit(1)

data = resp.json()
body = data["candidates"][0]["content"]["parts"][0]["text"]
print(f"Got {len(body.split())} words")

# Build frontmatter
slugs = sorted([f.replace(".md","") for f in os.listdir(ARTICLES_DIR) if f.endswith(".md")])
related = [s for s in slugs if s != "optimizely-vs-vwo-vs-ab-tasty-vs-convert-2026"][:3]
print(f"Related: {related}")

tools_data = [
    {"name": "Optimizely", "verdict": "Beste enterprise experimentatieplatform", "priceRange": "EUR 36.000+/jaar", "bestFor": "Enterprise & Full-stack", "rating": 4.6, "affiliateLink": "https://optimizely.com/?ref=aitoolsnl"},
    {"name": "VWO", "verdict": "Beste all-in-one CRO platform", "priceRange": "EUR 200-500/mnd", "bestFor": "MKB Marketing teams", "rating": 4.5, "affiliateLink": "https://vwo.com/?ref=aitoolsnl"},
    {"name": "AB Tasty", "verdict": "Beste EU-alternatief — AVG-compliant", "priceRange": "EUR 300-1500/mnd", "bestFor": "EU E-commerce", "rating": 4.4, "affiliateLink": "https://abtasty.com/?ref=aitoolsnl"},
    {"name": "Convert Experiences", "verdict": "Beste prijs-kwaliteit", "priceRange": "EUR 99-499/mnd", "bestFor": "Budget & Privacy", "rating": 4.2, "affiliateLink": "https://convert.com/?ref=aitoolsnl"},
    {"name": "Crazy Egg", "verdict": "Beste visuele analyse", "priceRange": "EUR 29-99/mnd", "bestFor": "Visuele Analyse", "rating": 4.0, "affiliateLink": "https://crazyegg.com/?ref=aitoolsnl"},
    {"name": "Kameleoon", "verdict": "Frans AI-first platform", "priceRange": "EUR 500-2000/mnd", "bestFor": "AI-personalisatie", "rating": 4.3, "affiliateLink": "https://kameleoon.com/?ref=aitoolsnl"},
    {"name": "PostHog Experiments", "verdict": "Open-source Google Optimize vervanger", "priceRange": "EUR 0 (tot 1M events/mnd)", "bestFor": "Budget & Analytics", "rating": 4.1, "affiliateLink": "https://posthog.com/?ref=aitoolsnl"},
]

avg = round(sum(t["rating"] for t in tools_data) / len(tools_data), 1)

article = {
    "title": "Optimizely vs VWO vs AB Tasty vs Convert 2026: beste A/B testing en CRO tools",
    "slug": "optimizely-vs-vwo-vs-ab-tasty-vs-convert-2026",
    "description": "Optimizely, VWO, AB Tasty of Convert in 2026? Vergelijk de beste A/B testing en conversie-optimalisatie platforms op features, prijs, AI en AVG-compliance voor Nederlandse marketeers.",
    "category": "business", "rating": avg, "priceRange": "EUR 0-100/mnd",
    "pros": ["Uitgebreide 2026 vergelijking", "Duidelijke prijsranges en use cases", "Nederlandstalig"],
    "cons": ["Prijzen kunnen wijzigen", "AI-features in ontwikkeling", "Niet alles dagelijks getest"],
    "affiliateLinks": ["https://www.beehiiv.com/?via=anonymous-operator"],
    "date": str(date.today()), "modelYear": 2026,
    "featuredTool": "Optimizely", "readingTime": "8 min",
    "tools": tools_data, "related": related, "draft": False,
    "faq": [
        {"q": "Wat is de beste tool?", "a": "Dat hangt af van je situatie. Optimizely is voor de meeste gebruikers een prima startpunt."},
        {"q": "Zijn er gratis alternatieven?", "a": "Ja, meerdere tools hebben gratis tiers. Perfect om te beginnen."},
        {"q": "Hoe kies ik de juiste tool?", "a": "Begin met je use case en budget. Filter de tabel op score en prijs."},
    ]
}

fm = yaml.dump(article, allow_unicode=True, default_flow_style=False, sort_keys=False, width=120)
out = os.path.join(ARTICLES_DIR, "optimizely-vs-vwo-vs-ab-tasty-vs-convert-2026.md")
with open(out, "w", encoding="utf-8") as f:
    f.write(f"---\n{fm}---\n{body}")

# Verify
with open(out) as f:
    content = f.read()
word_count = len(content.split())
print(f"Written: {out} ({word_count} words)")
print(f"Heading count: {content.count('## ')}")

# Also regenerate auth0 (truncated)
print("\n--- Regenerating Auth0 article ---")
auth0_prompt = """Schrijf een Nederlands artikel van 1200-1500 woorden over Auth0 vs Clerk vs Supabase Auth vs Firebase Auth in 2026. Behandel precies 7 tools: Auth0 (Okta), Clerk, Supabase Auth, Firebase Auth, WorkOS, Kinde, Keycloak.

Structuur:
- Introductie: authenticatie 2026 — passkeys, passwordless, SSO, social login, EU data residency
- Per tool een ## kop: beschrijving, prijs (EUR/maand bij 1000-5000 MAU), beste use case, plus- en minpunten, verdict
- Markdown vergelijkingstabel: naam, gratis MAU, prijs vanaf, passkeys, SSO/SAML, EU-hosting, score (1-5)
- Conclusie: voor side project, startup, scale-up, enterprise B2B SaaS, e-commerce, EU-privacy-first, budget
- 3 FAQ's

Belangrijk voor NL devs: AVG, EU data residency, DigiD/eHerkenning mogelijkheden. Keycloak als EU open-source alternatief. Vloeiend Nederlands."""

payload["contents"][0]["parts"][0]["text"] = auth0_prompt
resp2 = requests.post(url, json=payload, timeout=180, headers={"Content-Type": "application/json"})
if resp2.status_code == 200:
    data2 = resp2.json()
    body2 = data2["candidates"][0]["content"]["parts"][0]["text"]
    print(f"Auth0 body: {len(body2.split())} words")

    auth0_tools = [
        {"name": "Auth0 (Okta)", "verdict": "Meest complete enterprise auth", "priceRange": "EUR 0-23/maand (tot 25k MAU)", "bestFor": "Enterprise & B2B SaaS", "rating": 4.6, "affiliateLink": "https://auth0.com/?ref=aitoolsnl"},
        {"name": "Clerk", "verdict": "Beste DX voor React/Next.js", "priceRange": "EUR 0-25/maand (tot 10k MAU)", "bestFor": "React/Next.js apps", "rating": 4.7, "affiliateLink": "https://clerk.com/?ref=aitoolsnl"},
        {"name": "Supabase Auth", "verdict": "Naadloos met PostgreSQL RLS", "priceRange": "EUR 0-25/maand (tot 100k MAU)", "bestFor": "Full-stack & Supabase", "rating": 4.5, "affiliateLink": "https://supabase.com/?ref=aitoolsnl"},
        {"name": "Firebase Auth", "verdict": "Gratis en schaalt oneindig", "priceRange": "EUR 0 (gratis, onbeperkt)", "bestFor": "Mobile & Google Cloud", "rating": 4.4, "affiliateLink": "https://firebase.google.com/?ref=aitoolsnl"},
        {"name": "WorkOS", "verdict": "Enterprise SSO in een dag", "priceRange": "EUR 0-99/maand", "bestFor": "B2B SaaS Enterprise", "rating": 4.3, "affiliateLink": "https://workos.com/?ref=aitoolsnl"},
        {"name": "Kinde", "verdict": "Moderne auth met gratis onbeperkte MAU", "priceRange": "EUR 0-25/maand", "bestFor": "Startups & Indie devs", "rating": 4.2, "affiliateLink": "https://kinde.com/?ref=aitoolsnl"},
        {"name": "Keycloak", "verdict": "Beste open-source self-host auth", "priceRange": "EUR 0 (self-host)", "bestFor": "Self-host & EU Privacy", "rating": 4.0, "affiliateLink": "https://keycloak.org/?ref=aitoolsnl"},
    ]
    auth0_avg = round(sum(t["rating"] for t in auth0_tools) / len(auth0_tools), 1)
    auth0_related = [s for s in slugs if s != "auth0-vs-clerk-vs-supabase-auth-vs-firebase-auth-2026"][:3]

    auth0_article = {
        "title": "Auth0 vs Clerk vs Supabase Auth vs Firebase Auth 2026: beste authenticatie voor developers",
        "slug": "auth0-vs-clerk-vs-supabase-auth-vs-firebase-auth-2026",
        "description": "Auth0, Clerk, Supabase Auth of Firebase Auth in 2026? Vergelijk de beste auth-platforms op prijs, features, developer experience en AVG-compliance voor Nederlandse ontwikkelaars.",
        "category": "development", "rating": auth0_avg, "priceRange": "EUR 0-100/mnd",
        "pros": ["Uitgebreide 2026 vergelijking", "Duidelijke prijsranges en use cases", "Nederlandstalig"],
        "cons": ["Prijzen kunnen wijzigen", "AI-features in ontwikkeling", "Niet alles dagelijks getest"],
        "affiliateLinks": ["https://www.beehiiv.com/?via=anonymous-operator"],
        "date": str(date.today()), "modelYear": 2026,
        "featuredTool": "Clerk", "readingTime": "8 min",
        "tools": auth0_tools, "related": auth0_related, "draft": False,
        "faq": [
            {"q": "Wat is de beste tool?", "a": "Dat hangt af van je situatie. Clerk is voor de meeste developers een prima startpunt."},
            {"q": "Zijn er gratis alternatieven?", "a": "Ja, meerdere tools hebben gratis tiers. Perfect om te beginnen."},
            {"q": "Hoe kies ik de juiste tool?", "a": "Begin met je use case en budget. Filter de tabel op score en prijs."},
        ]
    }
    auth0_fm = yaml.dump(auth0_article, allow_unicode=True, default_flow_style=False, sort_keys=False, width=120)
    auth0_out = os.path.join(ARTICLES_DIR, "auth0-vs-clerk-vs-supabase-auth-vs-firebase-auth-2026.md")
    with open(auth0_out, "w", encoding="utf-8") as f:
        f.write(f"---\n{auth0_fm}---\n{body2}")
    print(f"Auth0 written: {auth0_out} ({len(open(auth0_out).read().split())} words)")
else:
    print(f"Auth0 FAILED: HTTP {resp2.status_code}")

print("\nDone!")
