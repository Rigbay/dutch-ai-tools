#!/usr/bin/env python3
"""Set proper descriptions (80-180 chars) for all 5 new articles."""
import re

DESCRIPTIONS = {
    'beste-ai-tools-supply-chain-logistiek-2026': "Vergelijk de beste AI tools voor supply chain en logistiek in 2026. Van voorraadvoorspelling tot route-optimalisatie: gericht op de Nederlandse logistieke sector.",
    'beste-ai-tools-klantfeedback-cx-2026': "Vergelijk de beste AI tools voor klantfeedback en customer experience in 2026. Van NPS-analyse tot sentimentdetectie: welke CX AI tool past bij jouw bedrijf?",
    'beste-ai-tools-financieel-adviseurs-2026': "AI tools voor financieel adviseurs in 2026. Vergelijk tools voor portefeuilleanalyse, risicobeheer en klantadvies met focus op AFM- en DNB-compliance.",
    'beste-ai-tools-evenementen-2026': "De beste AI tools voor evenementenorganisatie in 2026. Van slimme bezoekersmatching tot ticketoptimalisatie: vergelijk 6 tools voor de Nederlandse eventbranche.",
    'beste-ai-tools-onderwijs-instellingen-2026': "Vergelijk de beste AI tools voor scholen, universiteiten en opleidingsinstituten in 2026. Van adaptief leren tot plagiaatdetectie — met focus op AVG-compliance.",
}

BASE = '/tmp/dutch-ai-tools/src/content/articles'

for slug, new_desc in DESCRIPTIONS.items():
    path = f'{BASE}/{slug}.md'
    with open(path) as f:
        content = f.read()
    
    new_content = re.sub(
        r"description: '.+?'",
        f"description: '{new_desc}'",
        content
    )
    
    with open(path, 'w') as f:
        f.write(new_content)
    
    dlen = len(new_desc)
    status = "OK" if 80 <= dlen <= 180 else f"WARN ({dlen} chars)"
    print(f'{slug}: {status}')

print('Done')
