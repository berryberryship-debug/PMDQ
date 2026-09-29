#!/usr/bin/env python3
"""
Ajoute un marqueur [P] aux montants M$ qui n'en ont pas.
"""
import re
from pathlib import Path

PAGES = [
    "annexe-ilots-chaleur.html",
    "classe-moyenne.html",
    "comparaison-partis.html",
    "obsolescence-programmee.html",
    "plantation-arbres.html",
]

# Regex : N M$ sans marqueur juste apres
MONTANT_RE = re.compile(r'(\d+(?:[.,]\d+)?\s*M\$)(?!\s*\[)')

def traiter(chemin):
    if not chemin.exists():
        print(f"  ✗ {chemin.name} introuvable")
        return
    contenu = chemin.read_text(encoding="utf-8")
    # Sauvegarde
    chemin.with_suffix(".html.bak").write_text(contenu, encoding="utf-8")
    # Remplacer les montants sans marqueur
    nouveau = MONTANT_RE.sub(r'\1 <span class="statut">[P]</span>', contenu)
    if nouveau != contenu:
        chemin.write_text(nouveau, encoding="utf-8")
        n = len(MONTANT_RE.findall(contenu))
        print(f"  ✓ {chemin.name} : {n} montant(s) marque(s) [P]")
    else:
        print(f"  · {chemin.name} : rien à modifier")

for page in PAGES:
    traiter(Path(page))
