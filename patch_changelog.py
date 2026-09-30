#!/usr/bin/env python3
"""patch_changelog.py -- Corrige et enrichit changelog.html."""
import re
from pathlib import Path

FICHIER = Path("changelog.html")


def sauvegarder(contenu):
    Path("changelog.html.bak_20260930").write_text(contenu, encoding="utf-8")
    print("[OK] Sauvegarde : changelog.html.bak_20260930")


BLOC_MAINTENANCE = '''<div class="alert info">
<p><strong>Maintenance du 30 septembre 2026 — v2.7.23-clean</strong></p>
<ul>
<li><strong>Empreinte JSON</strong> — Creation de <code>data/empreinte_pmdq.json</code> avec les valeurs figees v2.7.23 (ratio D moyen 1,4048 ; decaisse 7,127 G$ ; 6 RUPT documentees).</li>
<li><strong>Audit visuel</strong> — Nouvel outil <code>audit_visuel.py</code> (detecte viewport manquant, charset, liens casses, IDs dupliques).</li>
<li><strong>5 corrections HTML</strong> — <code>audit_dashboard.html</code> (+ viewport) ; <code>section_corrigee.html</code> (+ viewport, charset, title, lang).</li>
<li><strong>Script tout-en-un</strong> — <code>verifier.sh</code> (audit visuel + empreinte + archive).</li>
<li><strong>Archivage</strong> — 18 fichiers redondants dans <code>_archive_20260930/</code> (aucune suppression).</li>
<li><strong>Git</strong> — Commits <code>e1b646e</code> et <code>40349fd</code>, tags <code>v2.7.23-audit-visuel</code> et <code>v2.7.23-clean</code>.</li>
</ul>
</div>'''


def patcher(contenu):
    # 1. Title
    contenu = contenu.replace("Changelog — PMDQ v2.7.22", "Changelog — PMDQ v2.7.23")
    # 2. Brand
    contenu = contenu.replace('class="brand">PMDQ v2.7.22', 'class="brand">PMDQ v2.7.23')
    # 3. Alerte
    contenu = contenu.replace(
        '2.7.5 + Livre X</span> — 26 septembre 2026',
        '2.7.23 + Livre X</span> — 30 septembre 2026'
    )
    # 4. Insertion apres lede
    marqueur = '<p class="lede">Historique des versions et des corrections du Dossier Maître PMDQ</p>'
    if marqueur in contenu and "Maintenance du 30 septembre 2026" not in contenu:
        contenu = contenu.replace(marqueur, marqueur + "\n" + BLOC_MAINTENANCE, 1)
    return contenu


def main():
    contenu = FICHIER.read_text(encoding="utf-8")
    sauvegarder(contenu)
    nouveau = patcher(contenu)
    FICHIER.write_text(nouveau, encoding="utf-8")
    print("[OK] changelog.html mis a jour")
    print("     - Title v2.7.22 -> v2.7.23")
    print("     - Brand v2.7.22 -> v2.7.23")
    print("     - Alerte 2.7.5 -> 2.7.23")
    print("     - Bloc maintenance 30 sept ajoute")


if __name__ == "__main__":
    main()
