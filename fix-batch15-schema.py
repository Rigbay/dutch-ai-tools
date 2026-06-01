#!/usr/bin/env python3
"""Fix schema validation errors for batch 15 articles.
Issues: descriptions > 180 chars, missing faq fields."""
import os, yaml

ARTICLES_DIR = "/workspace/dutch-ai-tools/src/content/articles"

FIXES = {
    "beste-ai-e-commerce-dropshipping-tools-2026": {
        "description": "AI tools voor e-commerce en dropshipping in 2026. Vergelijk Spocket, DSers, Zendrop, Sell The Trend, EcomHunt, Niche Scraper en SaleHoo voor productonderzoek en orderverwerking.",
        "faq": [
            {"q": "Welke AI e-commerce tool is het beste voor beginners?", "a": "Voor beginners is Sell The Trend een goede start door de AI-product research en eenvoudige Shopify-integratie. Ook DSers biedt een gratis basisplan om AliExpress dropshipping te verkennen zonder directe investering."},
            {"q": "Heb ik meerdere tools nodig voor mijn webshop?", "a": "Niet per se. Veel dropshippers beginnen met een combinatie van DSers (orderbeheer) en EcomHunt (productonderzoek). Naarmate je schaalt, kun je Spocket toevoegen voor snellere EU-levering en SaleHoo voor groothandel sourcing."},
            {"q": "Wat kost AI-e-commerce software gemiddeld per maand?", "a": "De meeste tools bieden gratis basisplannen. Voor serieuze dropshipping reken je op EUR 30-80 per maand voor premium functies zoals AI-productanalyse, automatisering en uitgebreide leveranciersdatabases."},
        ]
    },
    "beste-ai-3d-modellering-tools-2026": {
        "description": "AI tools voor 3D-modellering, AR en VR in 2026. Vergelijk Blender, Spline, Meshy, Luma AI, Kaedim, Masterpiece Studio en NVIDIA Omniverse voor 3D-ontwerp en virtual reality.",
        "faq": [
            {"q": "Kan ik met AI 3D-modellen maken zonder ervaring?", "a": "Ja, tools als Meshy en Luma AI genereren 3D-modellen vanuit tekstbeschrijvingen of foto's. Je hebt geen 3D-software-ervaring nodig om basis modellen te maken, al blijft Blender de standaard voor professioneel werk."},
            {"q": "Welke AI 3D tool is het beste voor game-ontwikkeling?", "a": "Voor game-ontwikkeling zijn Kaedim (2D-naar-3D voor game assets) en Blender met AI-plugins het populairst. NVIDIA Omniverse is de keuze voor real-time simulatie en digital twins."},
            {"q": "Zijn AI 3D-tools duur voor hobbyisten?", "a": "Nee, Blender is volledig gratis en Spline heeft een gratis laag. Luma AI en Meshy bieden ook gratis opties. Alleen professionele tools zoals Kaedim en Omniverse vragen hogere tarieven."},
        ]
    },
    "beste-ai-interieur-ontwerp-tools-2026": {
        "description": "AI tools voor interieurontwerp en woninginrichting in 2026. Vergelijk Planner 5D, Interior AI, HomeByMe, RoomGPT, DecorMatters en Hutch voor virtuele inrichting en stijladvies.",
        "faq": [
            {"q": "Werken AI interieur tools ook met Nederlandse maten en meubels?", "a": "Ja, Planner 5D en HomeByMe ondersteunen Nederlandse maatvoering. De tools werken met algemene meubelafmetingen, maar voor exacte IKEA of Jysk producten moet je soms handmatig de afmetingen controleren."},
            {"q": "Kan ik mijn eigen kamer fotograferen en direct een nieuwe inrichting zien?", "a": "Interior AI en RoomGPT doen precies dat: upload een foto van je eigen kamer en de AI toont direct hoe deze eruitziet in verschillende woonstijlen. DecorMatters voegt AR toe via je smartphonecamera."},
            {"q": "Welke interieur AI tool is het beste voor verhuizing?", "a": "Planner 5D is ideaal voor verhuizing: teken de plattegrond van je nieuwe woning, plaats virtuele meubels en bekijk alles in 3D voordat je iets koopt."},
        ]
    },
    "beste-ai-podcast-productie-tools-2026": {
        "description": "AI tools voor podcastproductie en audiobewerking in 2026. Vergelijk Descript, Riverside, Cleanvoice, Auphonic, Podcastle, Alitu en Adobe Podcast voor opname, bewerking en distributie.",
        "faq": [
            {"q": "Welke AI podcast tool is het beste voor beginners?", "a": "Adobe Podcast is gratis en ideaal om te starten met AI-ruisonderdrukking. Riverside biedt een gratis plan voor remote opnames met lokale kwaliteit. Podcastle combineert opname en editing in één platform."},
            {"q": "Kan AI mijn podcast volledig automatisch editen?", "a": "Alitu en Cleanvoice doen dit: upload je ruwe opname, en zij verwijderen stiltes, um's en mondgeluiden, normaliseren het volume en voegen intro/outro toe. Descript laat je daarna nog tekst-gebaseerd fine-tunen."},
            {"q": "Is Descript het geld waard voor Nederlandse podcasters?", "a": "Descript ondersteunt Nederlandse transcriptie en is zeer krachtig voor tekst-gebaseerde editing. Voor alleen audio-cleanup is Cleanvoice of Alitu voordeliger. Descript is het best waard als je ook video-podcast maakt."},
        ]
    },
    "beste-ai-research-academische-tools-2026": {
        "description": "AI tools voor wetenschappelijk onderzoek, literatuurstudie en academisch schrijven in 2026. Vergelijk Elicit, Scite, Connected Papers, Research Rabbit, Semantic Scholar, Paperpile en Scholarcy.",
        "faq": [
            {"q": "Zijn AI research tools accuraat genoeg voor academisch werk?", "a": "Ja, mits je de output controleert. Elicit en Semantic Scholar gebruiken peer-reviewed bronnen en geven directe links naar papers. Gebruik AI als assistent, niet als vervanging van eigen literatuuronderzoek."},
            {"q": "Welke tool is het beste voor een literatuurstudie?", "a": "Elicit is onverslaanbaar voor literatuuronderzoek: stel een vraag en krijg een tabel met bevindingen uit tientallen papers. Research Rabbit helpt bij het ontdekken van gerelateerd werk en auteurs."},
            {"q": "Kunnen deze tools helpen bij citatiebeheer?", "a": "Paperpile is gespecialiseerd in referentiebeheer met Google Docs integratie. Scite laat zien hoe papers worden geciteerd (ondersteunend, weerleggend of neutraal), wat waardevol is voor citatie-analyse."},
        ]
    }
}

def fix_article(slug):
    path = os.path.join(ARTICLES_DIR, f"{slug}.md")
    with open(path) as f:
        content = f.read()
    
    # Split frontmatter and body
    if not content.startswith("---"):
        print(f"  {slug}: no frontmatter")
        return False
    
    parts = content.split("---", 2)
    if len(parts) < 3:
        print(f"  {slug}: malformed frontmatter")
        return False
    
    fm_raw = parts[1]
    body = parts[2]
    
    fm = yaml.safe_load(fm_raw)
    fixes = FIXES[slug]
    
    # Fix description
    fm["description"] = fixes["description"]
    
    # Add faq
    fm["faq"] = fixes["faq"]
    
    # Rebuild frontmatter
    new_fm = yaml.dump(fm, allow_unicode=True, default_flow_style=False, sort_keys=False)
    
    with open(path, "w") as f:
        f.write("---\n")
        f.write(new_fm)
        f.write("---\n")
        f.write(body)
    
    print(f"  {slug}: fixed (desc: {len(fixes['description'])} chars, faq: {len(fixes['faq'])} items)")
    return True

print("Fixing schema issues...")
for slug in FIXES:
    fix_article(slug)
print("Done!")