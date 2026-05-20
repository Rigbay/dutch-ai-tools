#!/usr/bin/env python3
"""Fix batch5 articles: add FAQ, rename relatedArticles→related."""
import os
from pathlib import Path

ARTICLES_DIR = Path("/workspace/agent-workspace/scripts/missions/passive-income/dutch-ai-tools-comparison/src/content/articles")

FAQ_DATA = {
    "beste-ai-vertaaltools-2026": [
        {"q": "Is DeepL beter dan Google Translate voor Nederlands?", "a": "Ja, DeepL levert consistent nauwkeurigere en natuurlijkere Nederlandse vertalingen dan Google Translate, vooral voor zakelijke en formele teksten. Google Translate is beter voor snelle, informele vertalingen in veel talen tegelijk."},
        {"q": "Kan ik AI-vertaling gebruiken voor juridische documenten?", "a": "AI-vertaling is een goed startpunt, maar voor juridische documenten is menselijke controle essentieel. DeepL en ChatGPT kunnen de basisvertaling leveren, maar juridische nuances en landspecifieke terminologie vereisen een professionele vertaler."},
        {"q": "Welke AI-vertaaltool is het beste voor ZZP'ers?", "a": "DeepL is de beste keuze voor Nederlandse ZZP'ers. Het gratis plan dekt de meeste behoeften, en het Pro-abonnement (EUR 10-25/mnd) biedt onbeperkt vertalen, glossaria en teamfuncties voor als je groeit."},
    ],
    "beste-ai-presentatie-tools-2026": [
        {"q": "Kan Gamma Nederlandse presentaties maken?", "a": "Ja, Gamma ondersteunt Nederlands. Je kunt Nederlandstalige prompts geven en Gamma genereert de presentatie in het Nederlands. De AI past automatisch de taal van de slides aan op basis van je input."},
        {"q": "Zijn AI-presentatietools gratis te gebruiken?", "a": "De meeste AI-presentatietools hebben een gratis tier. Gamma, Tome en Canva AI bieden gratis plannen met beperkte credits. Beautiful.ai en Decktopus hebben betaalde plannen vanaf EUR 10-12/mnd."},
        {"q": "Kan ik AI-presentaties exporteren naar PowerPoint?", "a": "Ja, de meeste tools ondersteunen PowerPoint-export. Gamma, Beautiful.ai, Decktopus en Canva AI laten je presentaties downloaden als .pptx-bestand. Tome exporteert naar PDF. Check de exportopties per tool — dit verschilt per abonnement."},
    ],
    "beste-ai-sales-tools-2026": [
        {"q": "Zijn AI-sales tools geschikt voor ZZP'ers?", "a": "Ja, Apollo.io en Instantly hebben gratis plannen die prima werken voor ZZP'ers. Je kunt beginnen met een gratis account, je eerste leads vinden en een paar honderd outreach-mails per maand versturen zonder kosten."},
        {"q": "Is cold email via AI toegestaan in Nederland?", "a": "Ja, mits je voldoet aan de AVG/GDPR. Je moet een legitiem belang kunnen aantonen, ontvangers een opt-out bieden, en alleen zakelijke e-mailadressen benaderen. Instantly en Lemlist hebben ingebouwde compliance-features voor Europese regelgeving."},
        {"q": "Welke AI-sales tool is het beste voor het MKB?", "a": "Apollo.io is de beste allround keuze voor het Nederlandse MKB. Het combineert lead-database, AI-scoring en outreach in één platform, heeft een gratis tier, en de Europese contactdatabase is uitgebreid. Voor pure e-mailpersonalisatie is Lemlist sterker."},
    ],
}

def fix_article(slug):
    path = ARTICLES_DIR / f"{slug}.md"
    with open(path) as f:
        content = f.read()

    # Split frontmatter from body
    parts = content.split("---", 2)
    if len(parts) < 3:
        print(f"  ❌ {slug}: invalid format")
        return False
    fm = parts[1]
    body = parts[2]

    # Replace relatedArticles with related
    fm = fm.replace("relatedArticles:", "related:")

    # Check if faq already exists
    if "faq:" not in fm:
        # Build FAQ block
        faq_entries = FAQ_DATA.get(slug, [])
        faq_lines = ["faq:"]
        for entry in faq_entries:
            faq_lines.append(f"  - q: \"{entry['q']}\"")
            faq_lines.append(f"    a: \"{entry['a']}\"")
        fm += "\n" + "\n".join(faq_lines)

    # Reconstruct
    new_content = f"---{fm}---{body}"
    with open(path, "w") as f:
        f.write(new_content)

    return True


def main():
    slugs = [
        "beste-ai-vertaaltools-2026",
        "beste-ai-presentatie-tools-2026",
        "beste-ai-sales-tools-2026",
    ]
    for slug in slugs:
        ok = fix_article(slug)
        print(f"  {'✅' if ok else '❌'} {slug}")


if __name__ == "__main__":
    main()
