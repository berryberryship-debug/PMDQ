#!/usr/bin/env python3
"""Audit global : constantes dupliquees, non documentees, incoherences."""
import ast
from pathlib import Path
from collections import defaultdict

TRIVIAUX = {0, 1, 2, 3, 4, 5, 10, 100, 1000, 10_000, 100_000, 1_000_000}
SEUIL_SUSPECT = 1.0  # ignorer les tres petits nombres

def extraire(fichier):
    try:
        src = fichier.read_text(encoding="utf-8")
        arbre = ast.parse(src)
    except (SyntaxError, OSError):
        return []
    lignes = src.splitlines()
    trouves = []
    for noeud in ast.walk(arbre):
        if isinstance(noeud, ast.Constant) and isinstance(noeud.value, (int, float)):
            v = noeud.value
            if v in TRIVIAUX or abs(v) < SEUIL_SUSPECT:
                continue
            ligne = lignes[noeud.lineno - 1].strip()
            # Ignorer les commentaires
            if ligne.startswith("#"):
                continue
            trouves.append((v, noeud.lineno, ligne[:80]))
    return trouves

# Collecte
par_fichier = {}
par_valeur = defaultdict(list)

for f in sorted(Path(".").glob("moteur_*.py")):
    vals = extraire(f)
    par_fichier[f.name] = vals
    for v, ligne, ctx in vals:
        par_valeur[round(v, 4)].append((f.name, ligne, ctx))

# Rapport
print("=" * 78)
print("  AUDIT GLOBAL DES MOTEURS")
print("=" * 78)

print("\n[1] Nombre de constantes metier par moteur")
for nom, vals in par_fichier.items():
    print(f"  {nom:<28s} : {len(vals):>3} constantes")

print("\n[2] Valeurs partagees entre plusieurs moteurs (risque de divergence)")
dups = {v: refs for v, refs in par_valeur.items() if len(set(r[0] for r in refs)) > 1}
if not dups:
    print("  Aucune valeur partagee entre moteurs.")
else:
    for v, refs in sorted(dups.items(), key=lambda x: -len(x[1]))[:15]:
        fichiers = sorted(set(r[0] for r in refs))
        print(f"  {v:>12} : present dans {len(fichiers)} moteurs -> {', '.join(fichiers)}")

print("\n[3] Constantes repetees dans un meme moteur (candidat a extraire en haut)")
for nom, vals in par_fichier.items():
    compte = defaultdict(int)
    for v, ligne, ctx in vals:
        compte[round(v, 4)] += 1
    repetes = {v: n for v, n in compte.items() if n >= 3}
    if repetes:
        print(f"  {nom} : {repetes}")

print()
print("=" * 78)
