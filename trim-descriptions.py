#!/usr/bin/env python3
"""Trim descriptions to 180 chars max for batch 15."""
import os, yaml

ARTICLES_DIR = "/workspace/dutch-ai-tools/src/content/articles"

FIXES = {
    "beste-ai-podcast-productie-tools-2026": "AI tools voor podcastproductie en audiobewerking in 2026. Vergelijk Descript, Riverside, Cleanvoice, Auphonic, Podcastle, Alitu en Adobe Podcast voor opname en bewerking.",
    "beste-ai-research-academische-tools-2026": "AI tools voor wetenschappelijk onderzoek en academisch schrijven in 2026. Vergelijk Elicit, Scite, Connected Papers, Research Rabbit, Semantic Scholar, Paperpile en Scholarcy.",
}

for slug, new_desc in FIXES.items():
    path = os.path.join(ARTICLES_DIR, f"{slug}.md")
    with open(path) as f:
        content = f.read()
    parts = content.split("---", 2)
    fm = yaml.safe_load(parts[1])
    fm["description"] = new_desc
    new_fm = yaml.dump(fm, allow_unicode=True, default_flow_style=False, sort_keys=False)
    with open(path, "w") as f:
        f.write("---\n")
        f.write(new_fm)
        f.write("---\n")
        f.write(parts[2])
    print(f"{slug}: {len(new_desc)} chars")

print("Done")