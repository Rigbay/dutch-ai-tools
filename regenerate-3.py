#!/usr/bin/env python3
"""Regenerate 3 corrupted articles with tighter formatting constraints."""
import os, time, requests, sys

API_KEY = os.popen("grep '^GEMINI_API_KEY=' ~/.hermes/.env | sed 's/GEMINI_API_KEY=//'").read().strip()
OUT_DIR = "/tmp/dutch-ai-tools/src/content/articles"

TOPICS = [
    {
        "slug": "beste-ai-tools-financieel-adviseurs-2026",
        "title": "Beste AI Tools voor Financieel Adviseurs 2026: top 6 vergeleken",
        "category": "business",
        "tools": "Bloomberg GPT, AlphaSense, Kavout, Kensho, Ayasdi, Vise AI",
        "focus": "Nederlandse financiële sector — vermogensbeheer, portefeuilleanalyse, risicobeheer, klantadvies. Focus op AFM/DNB compliance.",
    },
    {
        "slug": "beste-ai-tools-evenementen-2026",
        "title": "Beste AI Tools voor Evenementen & Event Management 2026: top 6 vergeleken",
        "category": "business",
        "tools": "Cvent AI, Bizzabo, Eventbrite AI, Swapcard, Grip, Splash",
        "focus": "Nederlandse evenementenbranche — RAI, Jaarbeurs, festivals, corporate events. Matching, agendavoorspelling, analytics.",
    },
    {
        "slug": "beste-ai-tools-onderwijs-instellingen-2026",
        "title": "Beste AI Tools voor Onderwijsinstellingen 2026: top 7 vergeleken",
        "category": "productiviteit",
        "tools": "Turnitin AI, Kahoot! AI, Century Tech, Sana Labs, Knewton Alta, Coursera AI, Magister AI",
        "focus": "Nederlands onderwijs — basisscholen tot universiteiten. Adaptief leren, plagiaatdetectie, AVG compliance, leerlingvolgsystemen.",
    },
]

PROMPT_TEMPLATE = """Je bent een Nederlandse AI-tools reviewer. Schrijf een compact, informatief artikel van 700-900 woorden.

ONDERWERP: {title}
TOOLS: {tools}
FOCUS: {focus}

BELANGRIJK — deze regels overtreden is mislukt:
- MAX 900 woorden totaal. Stop zodra je 900 woorden hebt.
- Gebruik ALLEEN platte tekst. GEEN tabellen. GEEN markdown tabellen. Schrijf de vergelijking als gewone zinnen.
- Korte paragrafen van 2-3 zinnen max.
- Begin met ## Introductie
- Dan paragrafen per tool met ### [toolnaam] als kop
- Dan ## Snel advies
- Dan ## Conclusie  
- Dan ## FAQ met exact 3 korte vragen en antwoorden
- Nederlands, geen Engels

Schrijf nu:"""

def call_gemini(prompt):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-lite:generateContent?key={API_KEY}"
    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {"temperature": 0.7, "maxOutputTokens": 2048}
    }
    for attempt in range(3):
        try:
            resp = requests.post(url, json=payload, timeout=120)
            if resp.status_code == 200:
                data = resp.json()
                text = data["candidates"][0]["content"]["parts"][0]["text"]
                return text
            print(f"  API {resp.status_code}, retry {attempt+1}/3")
            time.sleep(5)
        except Exception as e:
            print(f"  Error: {e}")
            time.sleep(3)
    return None

def main():
    for i, topic in enumerate(TOPICS):
        out_path = os.path.join(OUT_DIR, f"{topic['slug']}.md")
        print(f"[{i+1}/3] {topic['slug']}")
        
        prompt = PROMPT_TEMPLATE.format(**topic)
        body = call_gemini(prompt)
        
        if body is None:
            print(f"  FAILED")
            continue
        
        # Read existing frontmatter
        with open(out_path, "r") as f:
            content = f.read()
        
        # Split at the first markdown heading (---\n...\n---\n then body)
        parts = content.split("---\n", 2)
        if len(parts) >= 3:
            # Reassemble: frontmatter + new body
            new_content = "---\n" + parts[1] + "---\n\n" + body.strip()
        else:
            print(f"  Could not parse existing frontmatter, skipping")
            continue
        
        with open(out_path, "w") as f:
            f.write(new_content)
        
        print(f"  Written {len(new_content)} chars")
        time.sleep(3)
    
    print("Done!")

if __name__ == "__main__":
    sys.exit(main())
