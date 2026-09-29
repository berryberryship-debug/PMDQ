#!/usr/bin/env python3
"""Extrait les constantes numériques codees en dur dans un moteur."""
import ast
import sys
from pathlib import Path

# Nombres triviaux a ignorer
TRIVIAUX = {0, 1, 2, 3, 4, 5, 10, 100, 1000, 10_000, 100_000, 1_000_000}

def extraire(fichier):
    src = Path(fichier).read_text(encoding="utf-8")
    arbre = ast.parse(src)
    lignes = src.splitlines()
    trouves = []
    
    for noeud in ast.walk(arbre):
        # Constantes numeriques isolees
        if isinstance(noeud, ast.Constant) and isinstance(noeud.value, (int, float)):
            v = noeud.value
            if v in TRIVIAUX:
                continue
            if abs(v) < 0.1:  # trop petit, probablement un seuil
                continue
            ligne = lignes[noeud.lineno - 1].strip()
            trouves.append({
                "ligne": noeud.lineno,
                "valeur": v,
                "contexte": ligne[:100],
            })
    
    # Deduplication
    vus = set()
    uniques = []
    for t in trouves:
        cle = (t["valeur"], t["ligne"])
        if cle not in vus:
            vus.add(cle)
            uniques.append(t)
    return uniques

if __name__ == "__main__":
    fichier = sys.argv[1] if len(sys.argv) > 1 else "moteur_vehicule.py"
    print(f"=== Constantes metier dans {fichier} ===\n")
    const = extraire(fichier)
    for c in const:
        print(f"  L{c['ligne']:>4}  {c['valeur']:>10}  {c['contexte']}")
    print(f"\nTotal : {len(const)} constantes")
