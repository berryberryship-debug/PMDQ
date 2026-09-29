#!/usr/bin/env python3
"""
Reclassifie les marqueurs [P] abusifs en [M] ou [C] selon le contexte.
"""
import re
from pathlib import Path

SOURCES_MESUREES = [
    "ISQ", "StatCan", "Statistique Canada", "Revenu Québec",
    "Finances Québec", "Banque du Canada", "RAMQ", "MSSS",
    "donneesquebec", "Données Québec",
]

# Regex pour capturer le marqueur [P] ajouté par erreur
MARQUEUR_RE = re.compile(r'(\d+(?:[.,]\d+)?\s*M\$)\s*<span class="statut">\[P\]</span>')

def contexte_mesure(texte, position, fenetre=200):
    """Regarde si une source officielle est mentionnée dans les N caractères suivants."""
    extrait = texte[position:position + fenetre]
    for source in SOURCES_MESUREES:
        if source.lower() in extrait.lower():
            return True
    return False

def traiter(chemin):
    if not chemin.exists():
        print(f"  ✗ {chemin.name} introuvable")
        return
    contenu = chemin.read_text(encoding="utf-8")
    original = contenu
    n_reclasses = 0

    def remplacer(m):
        nonlocal n_reclasses
        montant = m.group(1)
        position = m.end()
        if contexte_mesure(contenu, position):
            n_reclasses += 1
            return f'{montant} <span class="statut">[M]</span>'
        return m.group(0)

    nouveau = MARQUEUR_RE.sub(remplacer, contenu)

    if nouveau != original:
        chemin.write_text(nouveau, encoding="utf-8")
        print(f"  ✓ {chemin.name} : {n_reclasses} marqueur(s) reclassé(s) [P]→[M]")
    else:
        print(f"  · {chemin.name} : aucun changement")

for page in ["classe-moyenne.html", "comparaison-partis.html",
             "annexe-ilots-chaleur.html", "obsolescence-programmee.html",
             "plantation-arbres.html"]:
    traiter(Path(page))
