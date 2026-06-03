#!/usr/bin/env python3
"""Add 'Verder lezen' internal linking sections to 5 new articles."""
from pathlib import Path

DIR = Path("/workspace/dutch-ai-tools/src/content/articles")

FURTHER_READING = {
    "beste-ai-tools-marketing-automation-2026.md": (
        '### Verder lezen\n\n'
        'Wil je meer weten over AI tools voor jouw marketingstrategie? Bekijk ook:\n'
        '- [Beste AI Marketing Tools 2026](/beste-ai-marketing-tools-2026/) \u2014 overzicht van alle AI marketingtools\n'
        '- [AI voor SEO 2026](/ai-voor-seo-2026/) \u2014 optimaliseer je vindbaarheid met AI\n'
        '- [Beste AI Copywriting Tools 2026](/beste-ai-copywriting-tools-2026/) \u2014 AI voor contentcreatie\n\n'
    ),
    "beste-ai-tools-videomarketing-2026.md": (
        '### Verder lezen\n\n'
        'Meer AI tools voor jouw marketingstrategie:\n'
        '- [Beste AI Marketing Tools 2026](/beste-ai-marketing-tools-2026/) \u2014 alle marketingtools op een rij\n'
        '- [AI Content Distributie 2026](/beste-ai-content-distributie-marketing-2026/) \u2014 verspreid je video-content effectief\n'
        '- [AI Social Media Tools 2026](/beste-ai-tools-social-media-2026/) \u2014 social media beheer met AI\n\n'
    ),
    "beste-ai-tools-mlops-platform-engineering-2026.md": (
        '### Verder lezen\n\n'
        'Meer AI tools voor development en infrastructuur:\n'
        '- [Beste AI DevOps Tools 2026](/beste-ai-tools-devs-ops-2026/) \u2014 CI/CD en infrastructuur met AI\n'
        '- [Beste AI Programmeer Tools 2026](/beste-ai-tools-programmeren-2026/) \u2014 AI voor softwareontwikkeling\n'
        '- [AI Cloud Optimalisatie 2026](/beste-ai-tools-cloud-optimalisatie-2026/) \u2014 beheer cloudkosten met AI\n\n'
    ),
    "beste-ai-tools-prompt-engineering-2026.md": (
        '### Verder lezen\n\n'
        'Meer over AI en de nieuwste technologie\u00ebn:\n'
        '- [AI Trends 2026 Nederland](/ai-trends-2026-nederland/) \u2014 de belangrijkste AI-ontwikkelingen\n'
        '- [Beste Super AI Agents 2026](/beste-super-ai-agents-2026/) \u2014 autonome AI-agenten vergeleken\n'
        '- [AI Frontend Web Development 2026](/beste-ai-tools-frontend-web-development-2026/) \u2014 AI voor webontwikkeling\n\n'
    ),
    "beste-ai-tools-web-analytics-conversie-2026.md": (
        '### Verder lezen\n\n'
        'Meer AI tools voor marketing en optimalisatie:\n'
        '- [Beste AI Marketing Tools 2026](/beste-ai-marketing-tools-2026/) \u2014 overzicht van AI marketingtools\n'
        '- [Beste AI A/B Testing Tools 2026](/beste-ai-ab-testing-conversie-optimalisatie-2026/) \u2014 optimaliseer conversies met AI\n'
        '- [Beste AI SEO Tools 2026](/beste-ai-seo-tools-2026/) \u2014 verbeter je vindbaarheid met AI\n\n'
    ),
}

for fname, further_text in FURTHER_READING.items():
    fpath = DIR / fname
    if not fpath.exists():
        print(f"SKIP {fname}: not found")
        continue

    content = fpath.read_text(encoding="utf-8")

    # Try inserting before FAQ section
    for marker in ["### Veelgestelde vragen", "## Veelgestelde vragen"]:
        if marker in content:
            idx = content.find(marker)
            new_content = content[:idx] + further_text + content[idx:]
            fpath.write_text(new_content, encoding="utf-8")
            print(f"OK {fname}: inserted Verder lezen before FAQ ({len(further_text)} chars)")
            break
    else:
        print(f"FAIL {fname}: no FAQ marker found")

print("\nDone.")