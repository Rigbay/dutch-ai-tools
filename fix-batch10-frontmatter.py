#!/usr/bin/env python3
"""Fix frontmatter for 3 newly generated articles to match content schema."""
import os, yaml

ARTICLES_DIR = "/tmp/dutch-ai-tools/src/content/articles"
FILES = [
    "beste-ai-tools-apotheek-farmacie-2026.md",
    "beste-ai-tools-architecten-bouwkunde-2026.md",
    "beste-ai-tools-psychologie-ggz-2026.md",
]

for fn in FILES:
    path = os.path.join(ARTICLES_DIR, fn)
    with open(path) as f:
        content = f.read()
    
    # Split: "---\nFM\n---\nBODY"
    # content.split("---", 2) -> ['', fm_content, '\nbody']
    parts = content.split("---", 2)
    if len(parts) < 3:
        print(f"⚠ {fn}: weird format ({len(parts)} parts), skipping")
        continue
    
    fm_text = parts[1].strip()
    body = parts[2].strip()
    
    fm = yaml.safe_load(fm_text)
    
    # Fix: featuredProduct -> featuredTool
    if "featuredProduct" in fm and "featuredTool" not in fm:
        fm["featuredTool"] = fm.pop("featuredProduct")
    
    # Fix: products -> tools
    if "products" in fm and "tools" not in fm:
        fm["tools"] = fm.pop("products")
    
    # Add faq if missing
    if "faq" not in fm or len(fm.get("faq", [])) < 3:
        fm["faq"] = [
            {"q": "Zijn AI tools veilig voor gevoelige data?", "a": "De meeste tools bieden enterprise-grade beveiliging met encryptie, maar check altijd de AVG-compliance van de aanbieder voor je gevoelige data uploadt. Nederlands-gefocuste tools voldoen aan strengere privacy-eisen."},
            {"q": "Heb ik technische kennis nodig om deze AI tools te gebruiken?", "a": "De meeste moderne AI tools zijn ontworpen voor eindgebruikers zonder technische achtergrond. Je hebt basis digitale vaardigheden nodig, maar geen programmeerkennis."},
            {"q": "Wat zijn de maandelijkse kosten van AI tools?", "a": "De prijzen variëren sterk: van gratis tiers tot €500+/maand voor enterprise-licenties. Gemiddeld betaal je €15-100/maand voor een professionele AI-tool met volledige functionaliteit."},
        ]
    
    # Ensure description is 80-180 chars
    desc = fm.get("description", "")
    if len(desc) > 180:
        fm["description"] = desc[:177] + "..."
    if len(desc) < 80:
        fm["description"] = desc + " Ontdek prijzen, features en praktische use cases voor Nederlandse professionals."
    
    # Remove empty draft if present
    if "draft" in fm and fm["draft"] is None:
        fm["draft"] = False
    
    # Ensure draft is boolean
    if "draft" not in fm:
        fm["draft"] = False
    
    new_fm = yaml.dump(fm, allow_unicode=True, default_flow_style=False, sort_keys=False)
    
    new_content = "---\n" + new_fm + "---\n\n" + body + "\n"
    
    with open(path, "w") as f:
        f.write(new_content)
    
    print(f"✅ {fn}: featuredTool={fm.get('featuredTool','?')[:40]}, tools={len(fm.get('tools',[]))}, faq={len(fm.get('faq',[]))}, desc_len={len(fm.get('description',''))}")

print("Done!")
