#!/usr/bin/env python3
"""Audit fin : distingue formatage et metier."""
import ast
from pathlib import Path
from collections import defaultdict

# Valeurs à ignorer (formatage, ASCII, largeurs)
IGNORER = {0, 1, 2, 3, 4, 5, 10, 20, 32, 48, 50, 60, 64, 65, 70, 72, 78, 80,
           100, 120, 128, 256, 512, 1024, 1000, 10_000, 100_000, 1_000_000}

def extraire(fichier):
    src = fichier.read_text(encoding="utf-8")
    arbre = ast.parse(src)
    lignes = src.splitlines()
    trouves = []
    for noeud in ast.walk(arbre):
        if isinstance(noeud, ast.Constant) and isinstance(noeud.value, (int, float)):
            v = noeud.value
            if v in IGNORER:
                continue
            ligne_complete = lignes[noeud.lineno - 1]
            # Ignorer si la ligne contient 'print' ou '='
            est_print = "print" in ligne_complete
            est_format = "*" in ligne_complete and "=" in ligne_complete and '"' in ligne_complete
            if est_print or est_format:
                continue
            trouves.append((v, noeud.lineno, ligne_complete.strip()[:90]))
    return trouves

print("=" * 80)
print("  CONSTANTES METIER (hors formatage)")
print("=" * 80)

for f in sorted(Path(".").glob("moteur_*.py")):
    vals = extraire(f)
    if not vals:
        continue
    print(f"\n### {f.name} ({len(vals)} constantes)")
    vus = set()
    for v, ligne, ctx in vals:
        cle = (round(v, 4), ligne)
        if cle in vus:
            continue
        vus.add(cle)
        print(f"  L{ligne:>4}  {v:>12}  {ctx}")
