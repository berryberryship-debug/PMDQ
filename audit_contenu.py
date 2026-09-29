#!/usr/bin/env python3
"""
audit_contenu.py — Audit du contenu .md contre le socle PMDQ
Scanne les .md, vérifie les références, les moteurs cités et les chiffres G$.
"""
import re
import json
from pathlib import Path
from collections import defaultdict

RACINE = Path(".")

# Dossiers à ignorer complètement
IGNORES = {".git", ".v", "node_modules", "__pycache__"}

# --- Collecte des fichiers ---
def fichier_ignore(p):
    return any(part in IGNORES or part.startswith(".") for part in p.parts)

fichiers_md = []
for p in RACINE.rglob("*.md"):
    if not fichier_ignore(p):
        # Exclure les fichiers .v2.7.* ou backups
        if ".v2." not in p.name and ".bak" not in p.name:
            fichiers_md.append(p)
fichiers_md.sort()

# Tous les fichiers existants (nom + chemin relatif)
tous_fichiers = set()
for p in RACINE.rglob("*"):
    if p.is_file() and not fichier_ignore(p):
        tous_fichiers.add(p.name)
        try:
            tous_fichiers.add(str(p.relative_to(RACINE)))
        except ValueError:
            pass

# Moteurs présents à la racine
moteurs = {p.name for p in RACINE.glob("moteur_*.py")}

# --- Rapport ---
rapport = {
    "references_mortes": [],
    "moteurs_cites_absents": [],
    "versions_detectees": defaultdict(list),
    "chiffres_g": [],
}

# Regex
RE_REF = re.compile(r"`?([a-zA-Z0-9_\-/]+\.(?:md|py|json|html|csv))`?")
RE_MOTEUR = re.compile(r"\b(moteur_[a-z_]+\.py)\b")
RE_VERSION = re.compile(r"\bv(\d+)\.(\d+)(?:\.(\d+))?\b")
RE_GDOLLAR = re.compile(r"(\d+(?:[.,]\d+)?)\s*G\$")

for f in fichiers_md:
    try:
        contenu = f.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        continue

    # Références à des fichiers
    for match in RE_REF.finditer(contenu):
        ref = match.group(1)
        if ref.startswith("http") or ref.startswith("/"):
            continue
        if ref not in tous_fichiers and Path(ref).name not in tous_fichiers:
            rapport["references_mortes"].append((str(f), ref))

    # Moteurs cités
    for match in RE_MOTEUR.finditer(contenu):
        m = match.group(1)
        if m not in moteurs:
            rapport["moteurs_cites_absents"].append((str(f), m))

    # Versions
    for match in RE_VERSION.finditer(contenu):
        major, minor, patch = match.group(1), match.group(2), match.group(3)
        ver = f"v{major}.{minor}" + (f".{patch}" if patch else "")
        rapport["versions_detectees"][ver].append(str(f))

    # Chiffres G$
    for match in RE_GDOLLAR.finditer(contenu):
        try:
            v = float(match.group(1).replace(",", "."))
        except ValueError:
            continue
        if v > 0.1:
            rapport["chiffres_g"].append((str(f), v))

# --- Cache économique ---
cache_path = Path("sources/cache_economique.json")
valeurs_cache = set()
cache_dispo = False
if cache_path.exists():
    try:
        cache = json.loads(cache_path.read_text(encoding="utf-8"))
        cache_dispo = True
        for k, v in cache.items():
            if isinstance(v, dict):
                for kk in ("valeur", "valeur_g$", "ratio_pib_pct"):
                    if kk in v and v[kk] is not None:
                        try:
                            valeurs_cache.add(round(float(v[kk]), 2))
                        except (ValueError, TypeError):
                            pass
            elif isinstance(v, (int, float)):
                valeurs_cache.add(round(float(v), 2))
    except (OSError, ValueError):
        pass

# --- Affichage ---
print()
print("=" * 78)
print("  AUDIT DU CONTENU — PMDQ")
print("=" * 78)
print(f"  Fichiers .md analysés : {len(fichiers_md)}")
print(f"  Moteurs présents      : {len(moteurs)}")
print(f"  Cache économique      : {'chargé (' + str(len(valeurs_cache)) + ' valeurs)' if cache_dispo else 'ABSENT'}")
print()

# Références mortes
print("--- Références à des fichiers inexistants ---")
if not rapport["references_mortes"]:
    print("  Aucune.")
else:
    par_fichier = defaultdict(set)
    for src, ref in rapport["references_mortes"]:
        par_fichier[src].add(ref)
    total = 0
    for src in sorted(par_fichier):
        refs = sorted(par_fichier[src])
        print(f"  {src} :")
        for r in refs[:8]:
            print(f"    -> {r}")
            total += 1
        if len(refs) > 8:
            print(f"    ... et {len(refs) - 8} autre(s)")
    print(f"  Total : {total} référence(s) morte(s)")
print()

# Moteurs cités mais absents
print("--- Moteurs cités mais inexistants ---")
if not rapport["moteurs_cites_absents"]:
    print("  Aucun.")
else:
    par_fichier = defaultdict(set)
    for src, m in rapport["moteurs_cites_absents"]:
        par_fichier[src].add(m)
    for src in sorted(par_fichier):
        print(f"  {src} :")
        for m in sorted(par_fichier[src]):
            print(f"    -> {m}")
print()

# Versions
print("--- Versions citées dans le contenu ---")
for ver in sorted(rapport["versions_detectees"], key=lambda x: [int(n) for n in x[1:].split(".")]):
    n = len(set(rapport["versions_detectees"][ver]))
    print(f"  {ver:10s} : {n} fichier(s)")
print()

# Chiffres G$ non présents dans le cache
print("--- Chiffres G$ non trouvés dans le cache (top 20) ---")
if not cache_dispo:
    print("  Cache absent : impossible de comparer.")
else:
    vus = set()
    suspects = []
    for src, v in rapport["chiffres_g"]:
        vr = round(v, 2)
        if vr in valeurs_cache or vr in vus:
            continue
        vus.add(vr)
        suspects.append((src, v))
    suspects.sort(key=lambda x: -x[1])
    if not suspects:
        print("  Aucun : tous les G$ du contenu sont dans le cache.")
    else:
        for src, v in suspects[:20]:
            print(f"  {v:>8.2f} G$  ({src})")
        print(f"  Total de valeurs distinctes : {len(suspects)}")
print()
print("=" * 78)
print()
