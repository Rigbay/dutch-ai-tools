#!/usr/bin/env python3
"""
Fix YAML escaping in generated AI appliance articles.
"""

import os, re
from pathlib import Path

ARTICLES_DIR = Path("/workspace/dutch-ai-tools/src/content/articles")

def fix_file(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
    
    # Fix double-escaped apostrophe: \\' -> '
    content = content.replace("programma\\\\'s", "programma's")
    
    # Write back
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"  Fixed {filepath.name}")

def main():
    files_to_fix = [
        "beste-ai-robotstofzuigers-2026-roomba-roborock-dreame.md",
        "beste-ai-koffiemachines-2026-nespresso-keurig-jura.md",
        "beste-ai-luchtfilters-2026-dyson-philips-blueair.md",
        "beste-ai-inductiekookplaten-2026-miele-bosch-siemens.md"
    ]
    
    for fname in files_to_fix:
        filepath = ARTICLES_DIR / fname
        if filepath.exists():
            fix_file(filepath)
        else:
            print(f"  Skipping {fname} (not found)")

if __name__ == "__main__":
    main()