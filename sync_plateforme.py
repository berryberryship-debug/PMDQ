#!/usr/bin/env python3
"""
sync_plateforme.py — Synchronisation dépôt → plateforme publique
PMDQ v2.7.22

Génère un fichier sources/plateforme.json qui décrit l'état public
de la plateforme. Utilisé par le générateur HTML pour la page d'accueil.

Ce que le script fait :
  1. Lit la version courante (git describe)
  2. Scanne les fichiers .md publics (whitelist)
  3. Détecte le dossier le plus récent publié
  4. Écrit sources/plateforme.json

Usage :
    python3 sync_plateforme.py
    python3 sync_plateforme.py --verbeux
"""
import json
import re
import subprocess
import argparse
from datetime import datetime, date
from pathlib import Path

RACINE = Path(".")
SORTIE = Path("sources/plateforme.json")

# ─── Whitelist : uniquement ces dossiers/fichiers sont publics ───
PUBLICS = {
    "livres": [
        "sources/03_LIVRE-I.md",
        "sources/04_LIVRE-II.md",
        "sources/05_LIVRE-III-A.md",
        "sources/06_LIVRE-III-B.md",
        "sources/07_LIVRE-IV.md",
        "sources/08_LIVRE-V.md",
        "sources/09_LIVRE-VI.md",
        "sources/10_LIVRE-VII.md",
        "sources/11_LIVRE-VIII.md",
        "sources/23_LIVRE-IX.md",
    ],
    "annexes": [
        "sources/12_ANNEXE-A.md",
        "sources/13_ANNEXE-B.md",
        "sources/14_ANNEXE-C.md",
        "sources/15_ANNEXE-D.md",
        "sources/16_ANNEXE-E.md",
        "sources/17_ANNEXE-F.md",
        "sources/18_ANNEXE-G.md",
    ],
    "livre_blanc": "livre_blanc.md",
    "methodologie": "SOCLE.md",
    "changelog": "CHANGELOG.md",
}

# Dossiers entièrement exclus (jamais exposés)
EXCLUS = {
    ".git", ".v", "sources/contributions", "sources/lettres-interet",
    "sources/etats-financiers", "__pycache__",
}


def version_git():
    """Retourne la version courante depuis git describe."""
    try:
        out = subprocess.check_output(
            ["git", "describe", "--tags", "--abbrev=0"],
            stderr=subprocess.DEVNULL, text=True
        ).strip()
        # Normaliser : "socle-v2.7.22" -> "v2.7.22"
        m = re.search(r"v(\d+\.\d+\.\d+)", out)
        return f"v{m.group(1)}" if m else out
    except (subprocess.CalledProcessError, FileNotFoundError):
        return "v2.7.0"


def derniere_modif(fichiers):
    """Retourne la date de modification la plus récente parmi les fichiers."""
    dates = []
    for f in fichiers:
        p = RACINE / f
        if p.exists():
            dates.append(datetime.fromtimestamp(p.stat().st_mtime))
    return max(dates) if dates else datetime.now()


# Noms de fichiers utilises comme "dossiers vedettes" (trop generiques)
NOMS_IGNORES = {"readme", "index", "contact", "notes", "todo", "draft"}


def _est_dossier_valide(f):
    """Un fichier est un dossier valide s'il n'est pas un fichier utilitaire."""
    stem = f.stem.lower()
    if stem in NOMS_IGNORES:
        return False
    if stem.startswith("_"):
        return False
    return True


def scanner_dossiers():
    """Detecte le dossier le plus recent parmi les dossiers publics."""
    dossiers_pub = []
    # Dossiers prioritaires (contenu editorial)
    for d in ["CDLI", "campagnes", "dossiers", "investissement"]:
        p = RACINE / d
        if not p.exists():
            continue
        for f in p.rglob("*.md"):
            if any(ex in f.parts for ex in EXCLUS):
                continue
            if ".v2." in f.name or ".bak" in f.name:
                continue
            if not _est_dossier_valide(f):
                continue
            dossiers_pub.append({
                "fichier": str(f.relative_to(RACINE)),
                "titre": f.stem.replace("-", " ").replace("_", " ").strip(),
                "date": datetime.fromtimestamp(f.stat().st_mtime).isoformat(),
            })
    dossiers_pub.sort(key=lambda x: x["date"], reverse=True)
    return dossiers_pub


def compter_fichiers_publics():
    """Compte les fichiers dans la whitelist."""
    n = 0
    for categorie, fichiers in PUBLICS.items():
        if isinstance(fichiers, list):
            for f in fichiers:
                if (RACINE / f).exists():
                    n += 1
        elif isinstance(fichiers, str):
            if (RACINE / fichiers).exists():
                n += 1
    return n


def construire_config():
    """Construit la configuration publique."""
    dossiers = scanner_dossiers()
    return {
        "version": version_git(),
        "genere_le": date.today().isoformat(),
        "derniere_maj_depot": derniere_modif([
            "livre_blanc.md", "SOCLE.md"
        ]).isoformat(),
        "navigation": {
            "Le projet": ["Accueil", "Livre blanc", "Méthodologie"],
            "Les documents": ["Livres", "Lois", "Dossiers"],
            "Les moteurs": ["Moteurs", "PI"],
            "Suivi": ["Changelog"],
        },
        "dossier_vedette": dossiers[0] if dossiers else None,
        "dossiers_recents": dossiers[:5],
        "nb_fichiers_publics": compter_fichiers_publics(),
        "whitelist": PUBLICS,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--verbeux", action="store_true")
    args = parser.parse_args()

    config = construire_config()

    SORTIE.parent.mkdir(parents=True, exist_ok=True)
    SORTIE.write_text(
        json.dumps(config, indent=2, ensure_ascii=False),
        encoding="utf-8"
    )

    print()
    print("=" * 68)
    print("  SYNCHRONISATION PLATEFORME ← DÉPÔT")
    print("=" * 68)
    print(f"  Version détectée      : {config['version']}")
    print(f"  Fichiers publics      : {config['nb_fichiers_publics']}")
    print(f"  Dossiers détectés     : {len(config['dossiers_recents'])}")
    if config["dossier_vedette"]:
        d = config["dossier_vedette"]
        print(f"  Dossier vedette       : {d['titre']}")
        print(f"                          ({d['date'][:10]})")
    print(f"  Fichier généré        : {SORTIE}")
    print("=" * 68)
    print()

    if args.verbeux:
        print("Configuration complète :")
        print(json.dumps(config, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
