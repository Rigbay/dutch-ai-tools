#!/usr/bin/env python3
"""Retry remaining 3 articles — July 9, 2026."""
import os, time, requests, json, sys
from datetime import date

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "qwen3.5:9b"
ARTICLES_DIR = "/workspace/kieskeuken/dutch-ai-tools/src/content/articles"

def pick_related(new_slug, n=3):
    slugs = sorted([f.replace(".md", "") for f in os.listdir(ARTICLES_DIR) if f.endswith(".md")])
    return [s for s in slugs if s != new_slug][:n]

def call_ollama(prompt):
    payload = {"model": MODEL, "prompt": prompt, "stream": False, "options": {"temperature": 0.7, "num_predict": 4096}}
    for attempt in range(3):
        try:
            resp = requests.post(OLLAMA_URL, json=payload, timeout=300)
            if resp.status_code != 200:
                print(f"  HTTP {resp.status_code}: {resp.text[:200]}")
                time.sleep(10)
                continue
            return resp.json()["response"]
        except Exception as e:
            print(f"  Exception: {e}")
            time.sleep(10)
    return None

def parse_response(raw):
    raw = raw.strip()
    if raw.startswith("```"):
        lines = raw.split("\n")
        lines = lines[1:]
        raw = "\n".join(lines)
    
    parts = raw.split("===BODY===")
    if len(parts) < 2:
        for delim in ["---BODY---", "###BODY###", "***BODY***"]:
            parts = raw.split(delim)
            if len(parts) >= 2:
                break
    if len(parts) < 2:
        print("  No BODY delimiter found")
        return None
    
    json_part = parts[0].strip()
    body_part = parts[1].strip()
    if json_part.endswith("```"):
        json_part = json_part[:-3].strip()
    
    fixed = []
    in_str = False
    esc = False
    for ch in json_part:
        if esc:
            fixed.append(ch); esc = False; continue
        if ch == '\\':
            fixed.append(ch); esc = True; continue
        if ch == '"':
            in_str = not in_str; fixed.append(ch); continue
        if in_str and ch == '\n':
            fixed.append('\\n')
        elif in_str and ch == '\r':
            fixed.append('\\r')
        elif in_str and ch == '\t':
            fixed.append('\\t')
        else:
            fixed.append(ch)
    
    try:
        data = json.loads(''.join(fixed))
        data["body"] = body_part
        return data
    except json.JSONDecodeError as e:
        print(f"  JSON parse failed at pos {e.pos}")
        return None

def write_article(data, slug):
    today = date.today().isoformat()
    fm = "---\n"
    fm += f"title: '{data['title']}'\n"
    fm += f"slug: {slug}\n"
    fm += f"description: '{data['description']}'\n"
    fm += f"category: {data['category']}\n"
    fm += f"rating: {data['rating']}\n"
    fm += f"priceRange: {data['priceRange']}\n"
    fm += "pros:\n"
    for p in data.get('pros', []):
        fm += f"- {p}\n"
    fm += "cons:\n"
    for c in data.get('cons', []):
        fm += f"- {c}\n"
    fm += "affiliateLinks:\n"
    for link in data.get('affiliateLinks', []):
        fm += f"  - {link}\n"
    fm += f"date: {today}\n"
    fm += f"modelYear: 2026\n"
    fm += f"featuredTool: {data.get('featuredTool', data['tools'][0]['name'])}\n"
    fm += f"readingTime: {data.get('readingTime', '8 min')}\n"
    fm += "tools:\n"
    for t in data['tools']:
        fm += f"- name: {t['name']}\n"
        fm += f"  verdict: {t['verdict']}\n"
        fm += f"  priceRange: {t['priceRange']}\n"
        fm += f"  bestFor: {t['bestFor']}\n"
        fm += f"  rating: {t['rating']}\n"
        fm += f"  affiliateLink: {t['affiliateLink']}\n"
    
    related = pick_related(slug, 3)
    fm += "related:\n"
    for r in related:
        fm += f"  - {r}\n"
    fm += "draft: false\n"
    fm += "faq:\n"
    for faq in data.get('faq', []):
        fm += f"- q: \"{faq['q']}\"\n"
        fm += f"  a: '{faq['a']}'\n"
    fm += "---\n\n"
    
    full = fm + data['body']
    path = os.path.join(ARTICLES_DIR, f"{slug}.md")
    with open(path, 'w') as f:
        f.write(full)
    print(f"  Written: {path} ({len(full)} chars)")
    return True

ARTICLES = [
    {
        "slug": "taal-apps-vergelijken-2026-duolingo-babbel-busuu-memrise",
        "prompt": """Schrijf een Nederlands vergelijkingsartikel over de 6 beste taal leer apps in 2026: Duolingo, Babbel, Busuu, Memrise, Mondly, Preply.

OUTPUT: JSON metadata block, dan ===BODY===, dan markdown body.

JSON metadata:
{
  "title": "Beste Taal Apps 2026: Duolingo vs Babbel vs Busuu vs Memrise — Welke Leert Je Echt een Taal?",
  "description": "Vergelijking van de 6 beste taal leer apps in 2026. Eerlijke scores, prijzen en verdicts voor Duolingo, Babbel, Busuu, Memrise, Mondly en Preply.",
  "category": "persoonlijk",
  "rating": 4.5,
  "priceRange": "EUR 0-40/uur",
  "pros": ["Eerlijke 2026 vergelijking van de populairste taal leer apps", "Duidelijke prijsranges, scores en verdicts per app", "Nederlandstalig en praktijkgericht advies met FAQ"],
  "cons": ["Prijzen kunnen wijzigen", "Niet elke app is dagelijks getest", "Leerresultaten verschillen per persoon"],
  "affiliateLinks": ["https://www.duolingo.com/?ref=aitoolsnl"],
  "featuredTool": "Babbel",
  "readingTime": "9 min",
  "tools": [
    {"name": "Duolingo", "verdict": "Beste gratis optie — gamification maakt leren verslavend, maar brengt je niet verder dan A2/B1", "priceRange": "EUR 0-14/mnd", "bestFor": "Beginners die een taal willen proeven", "rating": 4.3, "affiliateLink": "https://www.duolingo.com/?ref=aitoolsnl"},
    {"name": "Babbel", "verdict": "Beste voor conversatie — gestructureerde lessen met realistische dialogen", "priceRange": "EUR 0-14/mnd", "bestFor": "Reizigers en expats die snel willen kunnen praten", "rating": 4.5, "affiliateLink": "https://www.babbel.com/?ref=aitoolsnl"},
    {"name": "Busuu", "verdict": "Unieke community-feedback — native speakers corrigeren je oefeningen", "priceRange": "EUR 0-12/mnd", "bestFor": "Leerders die echte feedback willen", "rating": 4.4, "affiliateLink": "https://www.busuu.com/?ref=aitoolsnl"},
    {"name": "Memrise", "verdict": "Beste voor vocabulaire — korte video's van locals maken woorden memorabel", "priceRange": "EUR 0-9/mnd", "bestFor": "Visuele leerders die snel woordenschat willen opbouwen", "rating": 4.1, "affiliateLink": "https://www.memrise.com/?ref=aitoolsnl"},
    {"name": "Mondly", "verdict": "Meest innovatief — AR en VR maken leren interactief, maar diepgang beperkt", "priceRange": "EUR 0-10/mnd", "bestFor": "Tech-liefhebbers die AR/VR willen ervaren", "rating": 3.9, "affiliateLink": "https://www.mondly.com/?ref=aitoolsnl"},
    {"name": "Preply", "verdict": "Beste voor serieuze leerders — 1-op-1 tutoring, duur maar meest effectief", "priceRange": "EUR 10-40/uur", "bestFor": "Gemotiveerde leerders die vloeiend willen worden", "rating": 4.6, "affiliateLink": "https://preply.com/?ref=aitoolsnl"}
  ],
  "faq": [
    {"q": "Welke app is het beste om Nederlands te leren?", "a": "Babbel en Busuu hebben gestructureerde NT2-programma's. Preply biedt 1-op-1 lessen met Nederlandse docenten."},
    {"q": "Kan ik echt een taal leren met alleen een app?", "a": "Apps brengen je tot A2/B1 niveau. Voor vloeiendheid heb je aanvullende methoden nodig zoals tutoring of onderdompeling."},
    {"q": "Welke app is het beste voor kinderen?", "a": "Duolingo is het meest kindvriendelijk door de gamified aanpak. Mondly Kids is ook een goede optie."}
  ]
}

===BODY===
Schrijf een volledig artikel in het Nederlands (1500+ woorden) met introductie, per tool een sectie met Wat het is/Voor wie/Pluspunten(5)/Minpunten(4-5), vergelijkingstabel, aanbevelingen per type leerders, en conclusie. Gebruik Nederlandse voorbeelden en prijzen in EUR."""
    },
    {
        "slug": "bbq-vergelijken-2026-gas-houtskool-elektrisch-pellet",
        "prompt": """Schrijf een Nederlands vergelijkingsartikel over de 6 beste BBQ types in 2026: Houtskool, Gas, Elektrisch, Pellet, Kamado, Tafel BBQ.

OUTPUT: JSON metadata block, dan ===BODY===, dan markdown body.

JSON metadata:
{
  "title": "Beste BBQ 2026: Gas vs Houtskool vs Elektrisch vs Pellet — Welke Past Bij Jouw Tuin of Balkon?",
  "description": "Vergelijking van de 6 beste BBQ types in 2026. Eerlijke scores, prijzen en verdicts voor houtskool, gas, elektrisch, pellet, kamado en tafel BBQ's.",
  "category": "huis-tuin",
  "rating": 4.6,
  "priceRange": "EUR 30-2000",
  "pros": ["Eerlijke 2026 vergelijking van alle BBQ types", "Duidelijke prijsranges, scores en verdicts", "Nederlandstalig en praktijkgericht advies"],
  "cons": ["Prijzen kunnen wijzigen", "Niet elk model is dagelijks getest", "Smaakvoorkeuren zijn subjectief"],
  "affiliateLinks": ["https://www.amazon.nl/dp/B07RZY2HZ5?tag=kieskeukennl-21"],
  "featuredTool": "Gas BBQ",
  "readingTime": "9 min",
  "tools": [
    {"name": "Houtskool BBQ", "verdict": "Beste voor pure grillsmaak — onverslaanbaar in smaak maar traag in opstarten", "priceRange": "EUR 100-400", "bestFor": "Barbecue-puristen die smaak boven gemak stellen", "rating": 4.5, "affiliateLink": "https://www.amazon.nl/dp/B07RZY2HZ5?tag=kieskeukennl-21"},
    {"name": "Gas BBQ", "verdict": "Beste allrounder — snel op temperatuur, schoon, precieze controle", "priceRange": "EUR 300-1000", "bestFor": "Gezinnen die vaak en snel willen barbecueën", "rating": 4.7, "affiliateLink": "https://www.amazon.nl/dp/B07RZY2HZ5?tag=kieskeukennl-21"},
    {"name": "Elektrische BBQ", "verdict": "Beste voor balkons — rookvrij, compact, maar mist authentieke BBQ-smaak", "priceRange": "EUR 100-300", "bestFor": "Appartementbewoners die niet mogen stoken", "rating": 3.8, "affiliateLink": "https://www.amazon.nl/dp/B07RZY2HZ5?tag=kieskeukennl-21"},
    {"name": "Pellet BBQ", "verdict": "Beste voor slow cooking — automatische temperatuurregeling, unieke rooksmaak", "priceRange": "EUR 500-1500", "bestFor": "BBQ-liefhebbers die low & slow willen gaan", "rating": 4.4, "affiliateLink": "https://www.amazon.nl/dp/B07RZY2HZ5?tag=kieskeukennl-21"},
    {"name": "Kamado BBQ", "verdict": "Meest veelzijdig — grillen, roken, bakken, pizza's. Houdt temperatuur perfect vast", "priceRange": "EUR 500-2000", "bestFor": "Enthousiaste koks die het hele jaar door barbecueën", "rating": 4.6, "affiliateLink": "https://www.amazon.nl/dp/B07RZY2HZ5?tag=kieskeukennl-21"},
    {"name": "Tafel BBQ", "verdict": "Beste voor picknicks — compact, snel, goedkoop, maar beperkte capaciteit", "priceRange": "EUR 30-100", "bestFor": "Studenten, kampeerders en kleine balkons", "rating": 3.7, "affiliateLink": "https://www.amazon.nl/dp/B07RZY2HZ5?tag=kieskeukennl-21"}
  ],
  "faq": [
    {"q": "Mag ik een houtskool BBQ op mijn balkon?", "a": "Check je huurcontract en VvE-reglement. Veel complexen verbieden houtskool- en gas-BBQ's. Een elektrische BBQ is dan de beste optie."},
    {"q": "Wat is het beste BBQ merk in Nederland?", "a": "Weber is het populairst vanwege bouwkwaliteit en garantie. The Bastard is toonaangevend in kamado's."},
    {"q": "Hoeveel moet ik uitgeven aan een goede BBQ?", "a": "Houtskool vanaf EUR 150, gas vanaf EUR 350, pellet/kamado vanaf EUR 500 maar gaat 10+ jaar mee."}
  ]
}

===BODY===
Schrijf een volledig artikel in het Nederlands (1500+ woorden) met introductie, per type een sectie met Wat het is/Voor wie/Pluspunten(5)/Minpunten(4-5), vergelijkingstabel, aanbevelingen per situatie, en conclusie. Gebruik Nederlandse voorbeelden en prijzen in EUR."""
    },
    {
        "slug": "airco-ventilator-vergelijken-2026-split-unit-mobiel-plafond",
        "prompt": """Schrijf een Nederlands vergelijkingsartikel over de 6 beste koeloplossingen voor Nederlandse huizen in 2026: Split-unit airco, Mobiele airco, Plafondventilator, Torenventilator, Vloerventilator, Ventilator met verneveling.

OUTPUT: JSON metadata block, dan ===BODY===, dan markdown body.

JSON metadata:
{
  "title": "Airco vs Ventilator 2026: Split-Unit, Mobiel of Plafond — Wat Koelt Jouw Huis Het Beste?",
  "description": "Vergelijking van de 6 beste koeloplossingen voor Nederlandse huizen in 2026. Eerlijke scores, prijzen en verdicts voor split-unit airco's, mobiele airco's en ventilatoren.",
  "category": "huis-tuin",
  "rating": 4.5,
  "priceRange": "EUR 20-2500",
  "pros": ["Eerlijke 2026 vergelijking van alle koeloplossingen", "Duidelijke prijsranges, scores en verdicts", "Nederlandstalig en praktijkgericht advies"],
  "cons": ["Prijzen kunnen wijzigen", "Niet elk model is dagelijks getest", "Installatiekosten variëren per woning"],
  "affiliateLinks": ["https://www.amazon.nl/dp/B07RZY2HZ5?tag=kieskeukennl-21"],
  "featuredTool": "Split-unit airco",
  "readingTime": "9 min",
  "tools": [
    {"name": "Split-unit airco", "verdict": "Beste koelprestatie — echte airconditioning, snel en efficiënt, maar hoge aanschafkosten", "priceRange": "EUR 800-2500", "bestFor": "Huisbezitters die structureel willen koelen", "rating": 4.8, "affiliateLink": "https://www.amazon.nl/dp/B07RZY2HZ5?tag=kieskeukennl-21"},
    {"name": "Mobiele airco", "verdict": "Beste compromis — geen installatie, verplaatsbaar, maar minder efficiënt en luider", "priceRange": "EUR 200-600", "bestFor": "Huurders die flexibel willen koelen", "rating": 4.0, "affiliateLink": "https://www.amazon.nl/dp/B07RZY2HZ5?tag=kieskeukennl-21"},
    {"name": "Plafondventilator", "verdict": "Beste voor constante luchtcirculatie — stil, energiezuinig, gelijkmatige verkoeling", "priceRange": "EUR 50-300", "bestFor": "Slaapkamers en woonkamers", "rating": 4.3, "affiliateLink": "https://www.amazon.nl/dp/B07RZY2HZ5?tag=kieskeukennl-21"},
    {"name": "Torenventilator", "verdict": "Beste design — compact, oscillerend, past in elk interieur", "priceRange": "EUR 30-150", "bestFor": "Kantoren en designbewuste gebruikers", "rating": 3.9, "affiliateLink": "https://www.amazon.nl/dp/B07RZY2HZ5?tag=kieskeukennl-21"},
    {"name": "Vloerventilator", "verdict": "Beste budget — krachtige luchtstroom voor weinig geld, maar luidruchtig", "priceRange": "EUR 20-80", "bestFor": "Studenten en mensen met een klein budget", "rating": 3.6, "affiliateLink": "https://www.amazon.nl/dp/B07RZY2HZ5?tag=kieskeukennl-21"},
    {"name": "Ventilator met verneveling", "verdict": "Beste voor droge hitte — watermist versterkt koeleffect, alleen effectief bij lage luchtvochtigheid", "priceRange": "EUR 50-200", "bestFor": "Buiten gebruik op terrassen en balkons", "rating": 3.7, "affiliateLink": "https://www.amazon.nl/dp/B07RZY2HZ5?tag=kieskeukennl-21"}
  ],
  "faq": [
    {"q": "Wat is het verschil in stroomverbruik?", "a": "Split-unit airco: 0,5-1,5 kW/uur (EUR 0,15-0,45/uur). Ventilator: 0,03-0,07 kW (EUR 0,01-0,02/uur). Het verschil is aanzienlijk."},
    {"q": "Heb ik een vergunning nodig voor een split-unit?", "a": "Meestal niet, maar check bij monumentale panden of zichtbare buitenunits. Huurders hebben toestemming nodig."},
    {"q": "Kan een airco ook verwarmen?", "a": "Ja, moderne split-units zijn warmtepompen die 3-4x efficiënter verwarmen dan elektrische kachels."}
  ]
}

===BODY===
Schrijf een volledig artikel in het Nederlands (1500+ woorden) met introductie, per type een sectie met Wat het is/Voor wie/Pluspunten(5)/Minpunten(4-5), vergelijkingstabel, aanbevelingen per situatie, en conclusie. Gebruik Nederlandse voorbeelden en prijzen in EUR."""
    }
]

def main():
    success = 0
    for i, art in enumerate(ARTICLES):
        print(f"\n[{i+1}/3] Generating: {art['slug']}")
        path = os.path.join(ARTICLES_DIR, f"{art['slug']}.md")
        if os.path.exists(path):
            print(f"  SKIP: already exists")
            continue
        
        raw = call_ollama(art['prompt'])
        if not raw:
            print(f"  FAILED: no response")
            continue
        
        data = parse_response(raw)
        if not data:
            print(f"  FAILED: parse error")
            debug_path = f"/tmp/gen-debug-{art['slug']}.txt"
            with open(debug_path, 'w') as f:
                f.write(raw)
            continue
        
        if write_article(data, art['slug']):
            success += 1
        time.sleep(3)
    
    print(f"\n=== DONE: {success}/3 ===")
    return success

if __name__ == "__main__":
    main()
