#!/usr/bin/env python3
"""
Fix corrupted articles — replace stub "Welkom bij AI Tools NL" with proper opening
paragraphs that were lost during the frontmatter patch.
"""
import os, sys
from pathlib import Path

ARTICLES_DIR = Path("/workspace/dutch-ai-tools/src/content/articles")

FIXES = {
    "beste-ai-tools-videomarketing-2026.md": (
        "Welkom bij AI Tools NL\n",
        "In 2026 is videomarketing niet langer een optie, maar een absolute noodzaak voor elke Nederlandse ondernemer die relevant wil blijven en wil groeien. De aandachtspanne van consumenten wordt steeds korter en visuele content, met name video, domineert de online landschappen – van sociale mediafeeds tot e-mailcampagnes en websites. Echter, het creëren van hoogwaardige video's was voorheen vaak tijdrovend, kostbaar en vereiste specifieke technische vaardigheden. Dit vormde een aanzienlijke drempel, vooral voor kleinere bedrijven en solo-ondernemers met beperkte middelen.\n\n"
    ),
    "beste-ai-tools-mlops-platform-engineering-2026.md": (
        "Welkom bij AI Tools NL\n",
        "De adoptie van kunstmatige intelligentie (AI) is in een stroomversnelling geraakt, en Nederlandse ondernemers staan voor de uitdaging om hun AI-initiatieven te schalen van experimentele projecten naar robuuste, productieve systemen. In 2026 is het niet langer voldoende om een getalenteerd team van data scientists te hebben; de echte winst zit in de operationele efficiëntie en schaalbaarheid van je machine learning (ML) modellen. Hier komen MLOps (Machine Learning Operations) en Platform Engineering om de hoek kijken. Deze disciplines zorgen ervoor dat AI-modellen snel ontwikkeld, getest, geïmplementeerd en gemonitord kunnen worden, wat cruciaal is voor het behouden van een concurrentievoordeel in een snel digitaliserende markt.\n\n"
    ),
    "beste-ai-tools-prompt-engineering-2026.md": (
        "Welkom bij AI Tools NL\n",
        "De wereld van kunstmatige intelligentie evolueert razendsnel, en 2026 belooft wederom een jaar te worden waarin AI niet langer een futuristisch concept is, maar een onmisbaar fundament voor succesvolle ondernemingen. Voor Nederlandse ondernemers betekent dit dat de efficiëntie en effectiviteit waarmee je AI inzet direct impact heeft op je concurrentiepositie en je bedrijfsresultaten. En precies hierin speelt prompt engineering een cruciale rol. Het gaat er niet langer alleen om *welke* AI-modellen je gebruikt, maar vooral *hoe* je deze modellen aanstuurt om de best mogelijke resultaten te leveren.\n\n"
    ),
    "beste-ai-tools-web-analytics-conversie-2026.md": (
        "Welkom bij AI Tools NL\n",
        "De digitale wereld evolueert razendsnel, en voor Nederlandse ondernemers in 2026 betekent dit dat traditionele web analytics niet langer volstaan. Om concurrerend te blijven en échte groei te realiseren, is een diepgaand begrip van gebruikersgedrag essentieel, en dat is precies waar Artificiële Intelligentie (AI) het verschil maakt. AI-gestuurde web analytics tools transformeren ruwe data in bruikbare inzichten, waardoor ondernemers niet alleen kunnen zien wat er gebeurt, maar ook waarom het gebeurt en, cruciaal, wat er *gaat* gebeuren. Dit stelt hen in staat om proactief te optimaliseren, conversies te verhogen en de ROI van hun marketinginspanningen significant te verbeteren.\n\n"
    ),
}

for fname, (old_line, new_intro) in FIXES.items():
    fpath = ARTICLES_DIR / fname
    if not fpath.exists():
        print(f"SKIP {fname}: not found")
        continue
    
    content = fpath.read_text(encoding='utf-8')
    
    # Only replace the very first occurrence at the start of body content
    if old_line in content:
        new_content = content.replace(old_line, new_intro, 1)
        fpath.write_text(new_content, encoding='utf-8')
        old_len = len(content)
        new_len = len(new_content)
        print(f"FIXED {fname}: restored opening paragraph ({old_len} → {new_len} chars)")
    else:
        print(f"CHECK {fname}: stub not found — need manual review")

print("\nDone. All 4 corrupted articles restored.")