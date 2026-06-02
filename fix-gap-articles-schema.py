#!/usr/bin/env python3
"""Fix description length (<180 chars) and add faq field to the 5 new articles."""
import yaml, os, glob, re

ARTICLES_DIR = "/workspace/dutch-ai-tools/src/content/articles"

FAQS = {
    "beste-ai-financiele-boekhouding-tools-2026": [
        {"question": "Wat is de beste AI boekhouding voor zzp'ers?", "answer": "Moneybird is de populairste keuze voor Nederlandse zzp'ers vanwege de gebruiksvriendelijke interface, automatische btw-aangifte en uitstekende bankkoppeling. Exact Online en e-Boekhouden.nl zijn goede alternatieven, afhankelijk van je budget en groeiwensen."},
        {"question": "Kan AI mijn belastingaangifte volledig automatiseren?", "answer": "AI kan het proces grotendeels automatiseren — van factuurherkenning tot btw-berekening — maar een accountant blijft aanbevolen voor de jaarlijkse inkomstenbelastingaangifte. De meeste tools ondersteunen automatische btw-aangifte."},
        {"question": "Zijn AI boekhoudtools veilig voor Nederlandse bankkoppelingen?", "answer": "Ja, de grote spelers zoals Exact Online, Moneybird en SnelStart gebruiken PSD2-veilige bankkoppelingen en voldoen aan de Nederlandse privacywetgeving (AVG). Je bankgegevens worden versleuteld opgeslagen."},
    ],
    "beste-ai-reizen-vakantieplanning-tools-2026": [
        {"question": "Wat is de beste AI reisplanner voor 2026?", "answer": "Google Travel met Gemini AI biedt de meest complete ervaring met gepersonaliseerde aanbevelingen en automatische reisroutes. TripIt is de beste keuze voor zakenreizigers die al hun reserveringen op één plek willen."},
        {"question": "Kan AI echt betere prijzen vinden voor vluchten?", "answer": "Ja — Hopper voorspelt prijstrends en adviseert het beste moment om te boeken. Kayak vergelijkt honderden aanbieders tegelijk. AI kan tot 30% besparen op vluchten door timing te optimaliseren."},
        {"question": "Werken deze tools ook voor treinreizen in Europa?", "answer": "De meeste tools richten zich op vliegreizen, maar Google Travel en Roadtrippers ondersteunen ook trein- en autoreizen. Voor Europese treinreizen zijn NS International, Eurostar en Trainline goede aanvullingen."},
    ],
    "beste-ai-fitness-sport-gezondheid-tools-2026": [
        {"question": "Wat is de beste AI fitnessapp voor thuis?", "answer": "Freeletics is de beste keuze voor thuisworkouts zonder apparatuur — de AI past elke training aan op basis van je feedback, prestaties en herstel. Geen sportschool nodig."},
        {"question": "Hoe betrouwbaar zijn AI-slaaptrackers?", "answer": "AI-slaaptrackers zoals Sleep Cycle zijn betrouwbaar voor trendanalyse, maar niet medisch nauwkeurig. Ze kunnen slaapfasen detecteren via geluid of beweging en helpen je in de lichtste slaapfase wakker te worden."},
        {"question": "Kunnen deze tools mijn personal trainer vervangen?", "answer": "AI-tools zoals Freeletics, Fitbod en Aaptiv kunnen een personal trainer grotendeels vervangen voor algemene fitnessdoelen. Ze bieden gepersonaliseerde schema's en aanpassingen — maar missen fysieke correctie van houding."},
    ],
    "beste-ai-fotografie-beeldbewerking-tools-2026": [
        {"question": "Wat is de beste AI fotobewerking voor beginners?", "answer": "Canva Foto AI en Luminar Neo zijn het meest toegankelijk voor beginners — met AI die ingewikkelde bewerkingen zoals achtergrondverwijdering en luchtvervanging automatisch uitvoert."},
        {"question": "Werkt AI fotobewerking ook op oude foto's?", "answer": "Ja — Remini en Topaz Photo AI zijn gespecialiseerd in het herstellen van oude, korrelige of onscherpe foto's. Ze gebruiken AI om gezichten te herstellen, ruis te verwijderen en resolutie te verhogen."},
        {"question": "Heb ik Adobe Creative Cloud nodig voor AI fotobewerking?", "answer": "Nee — Luminar Neo, Topaz Photo AI en Canva bieden uitstekende AI-fotobewerking zonder abonnement op Adobe. Alleen voor professionele fotografie met geavanceerde maskers en selecties blijft Photoshop de standaard."},
    ],
    "beste-ai-onderwijs-bijles-elearning-tools-2026": [
        {"question": "Wat is de beste AI bijlesdocent voor middelbare scholieren?", "answer": "Khan Academy (Khanmigo) is de beste keuze — het is een AI-tutor die leerlingen niet zomaar antwoorden geeft maar door vragen te stellen zelf tot inzicht laat komen. Het is gratis en dekt alle schoolvakken."},
        {"question": "Kan AI helpen bij het leren van talen?", "answer": "Ja — Duolingo met AI-tutor is de populairste keuze voor talen leren. Het biedt adaptieve oefeningen, spraakherkenning en AI-roleplay gesprekken in meer dan 40 talen."},
        {"question": "Zijn deze tools geschikt voor het Nederlandse onderwijssysteem?", "answer": "Ja — Khan Academy, Quizlet en Grammarly werken met Nederlands lesmateriaal en ondersteunen de onderwijsniveaus WO, HBO en MBO. Duolingo biedt Nederlands als doeltaal en onderwijstaal."},
    ],
}

for slug, faqs in FAQS.items():
    fpath = os.path.join(ARTICLES_DIR, f"{slug}.md")
    if not os.path.exists(fpath):
        print(f"⚠️  {slug}: file not found")
        continue

    content = open(fpath).read()
    parts = content.split("---", 2)
    if len(parts) < 3:
        print(f"⚠️  {slug}: bad frontmatter")
        continue

    fm = yaml.safe_load(parts[1])

    # Fix description — must be <= 180 chars
    desc = fm.get("description", "")
    if len(desc) > 180:
        # Truncate to last complete word before 177
        truncated = desc[:177]
        last_space = truncated.rfind(" ")
        if last_space > 100:
            truncated = truncated[:last_space]
        fm["description"] = truncated + "."
        print(f"  {slug}: description {len(desc)} -> {len(fm['description'])} chars")

    # Add faq field
    fm["faq"] = faqs
    print(f"  {slug}: added {len(faqs)} FAQ entries")

    # Rebuild
    import yaml
    frontmatter_yaml = yaml.dump(fm, allow_unicode=True, default_flow_style=False, sort_keys=False)

    body = content.split("---", 2)[2]
    # Remove the leading newline after frontmatter if present
    if body.startswith("\n"):
        body = body[1:]

    with open(fpath, "w") as f:
        f.write("---\n")
        f.write(frontmatter_yaml)
        f.write("---\n\n")
        f.write(body)

    print(f"  ✅ {slug} fixed")

print("\nAll articles updated.")
