#!/usr/bin/env python3
"""Ajoute le bandeau + nav standard a section_corrigee.html."""
import re
from pathlib import Path

FICHIER = Path("section_corrigee.html")
contenu = FICHIER.read_text(encoding="utf-8")

Path("section_corrigee.html.bak_nav").write_text(contenu, encoding="utf-8")
print("[OK] Sauvegarde : section_corrigee.html.bak_nav")

BANDEAU = (
    '<div class="logo-banner"><div class="logo-banner__inner">'
    '<div class="logo-banner__lys">⚜</div>'
    '<div class="logo-banner__text"><div class="logo-banner__name">PMDQ</div>'
    '<div class="logo-banner__sub">Parti de la Mouvance Démocratique du Québec'
    '</div></div></div></div>\n'
)

HEADER = (
    '<header class="site-header"><div class="site-header__inner">'
    '<div class="brand">PMDQ v2.7.23 + Livre X<span>Gouvernance de campagne'
    '</span></div><nav class="nav">'
    '<a href="index.html">Accueil</a>'
    '<a href="changelog.html">Changelog</a>'
    '<a href="livres.html">Livres</a>'
    '<a href="campagne-financement.html">Campagne</a>'
    '</nav></div></header>\n<main>\n'
)

if "site-header__inner" in contenu:
    print("[SKIP] Nav deja presente")
else:
    contenu = re.sub(
        r"(<body[^>]*>)",
        r"\1\n" + BANDEAU + HEADER,
        contenu, count=1, flags=re.I
    )
    if "</main>" not in contenu:
        contenu = re.sub(r"(</body>)", "</main>\n\\1", contenu, count=1, flags=re.I)
    FICHIER.write_text(contenu, encoding="utf-8")
    print("[OK] Nav + main ajoutes")
