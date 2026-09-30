#!/usr/bin/env python3
"""Vérifie la cohérence des liens internes entre les pages HTML."""
import re
from pathlib import Path
from collections import defaultdict

RACINE = Path(".")
LINK_RE = re.compile(r'href=["\']([^"\']+\.html)["\']', re.IGNORECASE)

# 1. Recenser toutes les pages
pages = {f.name for f in RACINE.glob("*.html") if not f.name.endswith(".bak")}
print(f"Pages HTML : {len(pages)}\n")

# 2. Analyser les liens sortants
liens = defaultdict(set)       # source -> {cibles}
entrants = defaultdict(set)    # cible  -> {sources}
liens_morts = []

for f in sorted(RACINE.glob("*.html")):
    if f.name.endswith(".bak"):
        continue
    c = f.read_text(encoding="utf-8", errors="replace")
    for cible in LINK_RE.findall(c):
        cible = cible.split("#")[0]  # ignorer les ancres
        if not cible or cible.startswith("http"):
            continue
        liens[f.name].add(cible)
        if cible in pages:
            entrants[cible].add(f.name)
        else:
            liens_morts.append((f.name, cible))

# 3. Statistiques
print("=" * 78)
print("  ANALYSE DES LIENS INTERNES")
print("=" * 78)

print("\n[1] Liens morts (cibles inexistantes)")
if not liens_morts:
    print("  Aucun.")
else:
    par_cible = defaultdict(set)
    for src, cible in liens_morts:
        par_cible[cible].add(src)
    for cible in sorted(par_cible, key=lambda c: -len(par_cible[c])):
        sources = sorted(par_cible[cible])
        print(f"  {cible}  ←  {len(sources)} source(s)")
        for s in sources[:3]:
            print(f"      depuis {s}")
        if len(sources) > 3:
            print(f"      ... et {len(sources)-3} autre(s)")

print("\n[2] Pages orphelines (aucun lien entrant)")
orhelines = sorted(p for p in pages if p not in entrants and p != "index.html")
if not orhelines:
    print("  Aucune.")
else:
    for p in orhelines[:15]:
        print(f"  {p}")
    if len(orhelines) > 15:
        print(f"  ... et {len(orhelines)-15} autre(s)")

print("\n[3] Pages les plus liées (top 10)")
top = sorted(entrants.items(), key=lambda x: -len(x[1]))[:10]
for page, sources in top:
    print(f"  {page:<40s} : {len(sources)} lien(s) entrant(s)")

print("\n[4] Pages sans lien sortant (cul-de-sac)")
culls = [p for p in pages if not liens.get(p)]
if not culls:
    print("  Aucune.")
else:
    for p in culls[:10]:
        print(f"  {p}")

print("\n[5] Cohérence de la navigation principale")
# Détecter les pages qui partagent le même bloc <nav>
navs = {}
for f in sorted(RACINE.glob("*.html")):
    if f.name.endswith(".bak"):
        continue
    c = f.read_text(encoding="utf-8", errors="replace")
    m = re.search(r"<nav[^>]*>(.*?)</nav>", c, re.DOTALL | re.IGNORECASE)
    if m:
        nav = re.sub(r"\s+", " ", m.group(1)).strip()
        navs.setdefault(nav[:200], []).append(f.name)

print(f"  {len(navs)} variante(s) de nav détectée(s)")
for nav, fichiers in sorted(navs.items(), key=lambda x: -len(x[1])):
    print(f"    {len(fichiers):>3} page(s) : {nav[:80]}...")

print()
print("=" * 78)
