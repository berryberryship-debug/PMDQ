"""Ajoute une ligne "Derniere mise a jour" sous chaque titre de section."""
import re, shutil
from datetime import date
from pathlib import Path

REGISTRE = Path("sources/variables-sensibles.md")
SAUVEGARDE = Path("sources/variables-sensibles.md.bak")

if not REGISTRE.exists():
    print(f"Erreur : {REGISTRE} introuvable")
    raise SystemExit(1)

shutil.copy2(REGISTRE, SAUVEGARDE)
print(f"Sauvegarde creee : {SAUVEGARDE}")

contenu = REGISTRE.read_text(encoding="utf-8")
aujourd_hui = date.today().isoformat()

motif = re.compile(r"^(## \d+\..+)$", re.MULTILINE)

def remplacer(match):
    return match.group(1) + f"\n\n**Dernière mise à jour** : {aujourd_hui}"

nouveau = motif.sub(remplacer, contenu)
nouveau = re.sub(
    r"(\*\*Dernière mise à jour\*\* : \d{4}-\d{2}-\d{2}\n){2,}",
    r"\1",
    nouveau,
)

REGISTRE.write_text(nouveau, encoding="utf-8")
print(f"Dates ajoutees dans : {REGISTRE}")
print(f"Date utilisee       : {aujourd_hui}")
