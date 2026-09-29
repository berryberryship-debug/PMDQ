#!/usr/bin/env python3
"""Corrige mobilite-urbaine.html : horizon + intro des sections vides."""
from pathlib import Path
import re

f = Path("mobilite-urbaine.html")
c = f.read_text(encoding="utf-8")
original = c

# 1. Corriger l'horizon (toutes les variantes de tiret)
for tiret in ["-", "–", "—"]:
    c = c.replace(f"Horizon 2030{tiret}2035", "Horizon 2030–2034")

# 2. Intro section 2
motif_2 = re.compile(r'(<h2>[^<]*Programme indicatif[^<]*</h2>)', re.IGNORECASE)
if motif_2.search(c) and "Le projet se déploie sur cinq ans" not in c:
    c = motif_2.sub(
        r'\1\n<p>Le projet se déploie sur cinq ans, avec des jalons annuels '
        r'vérifiables. Chaque année conditionne la suivante : un jalon non '
        r'atteint suspend la progression.</p>',
        c, count=1
    )
    print("✓ Intro ajoutée à la section 2")

# 3. Intro section 5
motif_5 = re.compile(r'(<h2>[^<]*Clause politique[^<]*</h2>)', re.IGNORECASE)
if motif_5.search(c) and "Cette clause fixe l'orientation politique" not in c:
    c = motif_5.sub(
        r"\1\n<p>Cette clause fixe l'orientation politique du projet. "
        r"Elle est assumée et débattable. Elle n'engage aucune décision "
        r"avant validation par les étapes prévues.</p>",
        c, count=1
    )
    print("✓ Intro ajoutée à la section 5")

if c != original:
    f.write_text(c, encoding="utf-8")
    print("✓ Fichier sauvegardé")
else:
    print("· Aucun changement (déjà à jour ou motifs introuvables)")

# Vérification finale
contenu = f.read_text(encoding="utf-8")
print()
print("Horizons trouvés :", re.findall(r"Horizon \d{4}[–\-—]\d{4}", contenu))
print("Intro section 2 :", "✓" if "Le projet se déploie" in contenu else "✗")
print("Intro section 5 :", "✓" if "Cette clause fixe" in contenu else "✗")
