#!/usr/bin/env python3
"""corriger_pages.py -- Corrige les pages HTML avec anomalies."""
import re
from pathlib import Path
from datetime import datetime

RACINE = Path(__file__).parent

CIBLES = {
    "audit_dashboard.html": "Audit dashboard",
    "section_corrigee.html": "Section corrigee — Gouvernance de campagne",
}

TEMPLATE_PAGE = '''<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{titre}</title>
<style>
body{{background:#0d1117;color:#c9d1d9;font-family:-apple-system,sans-serif;max-width:900px;margin:0 auto;padding:2em;line-height:1.6}}
h2{{color:#3fb950;margin-top:2em}}
h3{{color:#d29922}}
ul{{padding-left:1.5em}}
li{{margin:.5em 0}}
strong{{color:#58a6ff}}
code{{background:#161b22;padding:.2em .5em;border-radius:4px}}
</style>
</head>
<body>
{contenu}
</body>
</html>
'''


def est_fragment(contenu):
    return not re.search(r"<(html|body|head)\b", contenu, re.I)


def corriger(fichier, titre):
    contenu = fichier.read_text(encoding="utf-8")
    # Sauvegarde
    bak = fichier.with_suffix(fichier.suffix + ".bak_audit")
    bak.write_text(contenu, encoding="utf-8")

    if est_fragment(contenu):
        nouveau = TEMPLATE_PAGE.format(titre=titre, contenu=contenu.strip())
        action = "enveloppe (fragment -> page complete)"
    else:
        # Page existante : on injecte les balises manquantes dans <head>
        corps = contenu
        if "charset" not in corps.lower():
            corps = re.sub(r"(<head[^>]*>)", r'\1\n<meta charset="UTF-8">', corps, count=1, flags=re.I)
        if 'name="viewport"' not in corps.lower():
            corps = re.sub(
                r"(<head[^>]*>)",
                r'\1\n<meta name="viewport" content="width=device-width,initial-scale=1">',
                corps, count=1, flags=re.I
            )
        if not re.search(r"<html[^>]*\blang=", corps, re.I):
            corps = re.sub(r"<html\b", '<html lang="fr"', corps, count=1, flags=re.I)
        nouveau = corps
        action = "balises ajoutees dans <head>"

    fichier.write_text(nouveau, encoding="utf-8")
    return action


def main():
    print("=" * 60)
    print("CORRECTION DES PAGES HTML")
    print("=" * 60)
    for nom, titre in CIBLES.items():
        f = RACINE / nom
        if not f.exists():
            print("[SKIP] " + nom + " (absent)")
            continue
        action = corriger(f, titre)
        print("[OK]   " + nom + " -- " + action)
    print("=" * 60)
    print("Sauvegardes : *.bak_audit")
    print("=" * 60)


if __name__ == "__main__":
    main()
