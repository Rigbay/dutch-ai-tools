#!/usr/bin/env python3
"""Fix FAQ field names from question/answer to q/a in the 5 new articles."""
import yaml, os

ARTICLES_DIR = "/workspace/dutch-ai-tools/src/content/articles"
SLUGS = [
    "beste-ai-financiele-boekhouding-tools-2026",
    "beste-ai-reizen-vakantieplanning-tools-2026",
    "beste-ai-fitness-sport-gezondheid-tools-2026",
    "beste-ai-fotografie-beeldbewerking-tools-2026",
    "beste-ai-onderwijs-bijles-elearning-tools-2026",
]

FAQ_CONTENT = {
    "beste-ai-financiele-boekhouding-tools-2026": [
        {"q": "Wat is de beste AI boekhouding voor zzp'ers?", "a": "Moneybird is de populairste keuze voor Nederlandse zzp'ers vanwege de gebruiksvriendelijke interface, automatische btw-aangifte en uitstekende bankkoppeling. Exact Online en e-Boekhouden.nl zijn goede alternatieven."},
        {"q": "Kan AI mijn belastingaangifte volledig automatiseren?", "a": "AI kan factuurherkenning, btw-berekening en administratie grotendeels automatiseren. Voor de jaarlijkse inkomstenbelastingaangifte blijft een accountant aanbevolen."},
        {"q": "Zijn AI boekhoudtools veilig voor Nederlandse bankkoppelingen?", "a": "Ja — Exact Online, Moneybird en SnelStart gebruiken PSD2-veilige bankkoppelingen en voldoen aan de AVG. Je bankgegevens worden versleuteld opgeslagen."},
    ],
    "beste-ai-reizen-vakantieplanning-tools-2026": [
        {"q": "Wat is de beste AI reisplanner voor 2026?", "a": "Google Travel met Gemini AI biedt de meest complete ervaring. TripIt is beter voor zakenreizigers, Hopper voor prijsbewuste vakantiegangers."},
        {"q": "Kan AI echt betere prijzen vinden voor vluchten?", "a": "Ja — Hopper voorspelt prijstrends en adviseert het beste boekmoment. AI kan tot 30% besparen door timing te optimaliseren."},
        {"q": "Werken deze tools ook voor treinreizen in Europa?", "a": "Google Travel en Roadtrippers ondersteunen trein- en autoreizen. Voor Europese treinreizen zijn NS International en Trainline goede aanvullingen."},
    ],
    "beste-ai-fitness-sport-gezondheid-tools-2026": [
        {"q": "Wat is de beste AI fitnessapp voor thuis?", "a": "Freeletics past elke workout aan op basis van je feedback en herstel. Geen sportschool nodig — alleen je lichaamsgewicht."},
        {"q": "Hoe betrouwbaar zijn AI-slaaptrackers?", "a": "Ze zijn betrouwbaar voor trendanalyse maar niet medisch nauwkeurig. Sleep Cycle detecteert slaapfasen en wekt je in je lichtste fase."},
        {"q": "Kunnen deze tools mijn personal trainer vervangen?", "a": "Grotendeels wel voor algemene doelen — Freeletics, Fitbod en Aaptiv bieden gepersonaliseerde schema's. Ze missen alleen fysieke correctie."},
    ],
    "beste-ai-fotografie-beeldbewerking-tools-2026": [
        {"q": "Wat is de beste AI fotobewerking voor beginners?", "a": "Canva Foto AI en Luminar Neo zijn het toegankelijkst — AI voert achtergrondverwijdering en luchtvervanging automatisch uit."},
        {"q": "Werkt AI fotobewerking ook op oude foto's?", "a": "Ja — Remini en Topaz Photo AI herstellen oude, korrelige foto's met gezichtsherstel, ruisverwijdering en AI-upscaling."},
        {"q": "Heb ik Adobe Creative Cloud nodig voor AI fotobewerking?", "a": "Nee — Luminar Neo, Topaz Photo AI en Canva bieden uitstekende AI-fotobewerking zonder Adobe-abonnement."},
    ],
    "beste-ai-onderwijs-bijles-elearning-tools-2026": [
        {"q": "Wat is de beste AI bijlesdocent voor scholieren?", "a": "Khan Academy (Khanmigo) is de beste keuze — een AI-tutor die door vragen te stellen laat ontdekken. Gratis en dekt alle schoolvakken."},
        {"q": "Kan AI helpen bij het leren van talen?", "a": "Ja — Duolingo met AI-tutor biedt adaptieve oefeningen, spraakherkenning en AI-roleplay in meer dan 40 talen."},
        {"q": "Zijn deze tools geschikt voor het Nederlandse onderwijssysteem?", "a": "Ja — Khan Academy, Quizlet en Grammarly werken met Nederlands lesmateriaal. Duolingo biedt Nederlands als doeltaal."},
    ],
}

for slug in SLUGS:
    fpath = os.path.join(ARTICLES_DIR, f"{slug}.md")
    content = open(fpath).read()
    parts = content.split("---", 2)
    fm = yaml.safe_load(parts[1])
    fm["faq"] = FAQ_CONTENT[slug]

    # Ensure description <180 chars
    desc = fm.get("description", "")
    if len(desc) > 180:
        truncated = desc[:177]
        last_space = truncated.rfind(" ")
        if last_space > 100:
            truncated = truncated[:last_space]
        fm["description"] = truncated + "."

    frontmatter_yaml = yaml.dump(fm, allow_unicode=True, default_flow_style=False, sort_keys=False)
    body = content.split("---", 2)[2]
    if body.startswith("\n"):
        body = body[1:]

    with open(fpath, "w") as f:
        f.write("---\n")
        f.write(frontmatter_yaml)
        f.write("---\n\n")
        f.write(body)

    print(f"✅ {slug}: description={len(fm['description'])} chars, faq with q/a keys")

print("\nDone.")
