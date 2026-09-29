#!/usr/bin/env python3
"""
ecrire_etat.py
Produit sources/etat_variables.json a partir de l'analyse du registre,
avec un bloc resume pour les consommateurs rapides.
"""

import json
from pathlib import Path

import moteur_variables as mv

SORTIE = Path("sources/etat_variables.json")
SCHEMA_VERSION = "1.0"


def resume(sections):
    d = {
        "total": len(sections),
        "a_jour": 0,
        "en_retard": 0,
        "a_revoir": 0,
        "section_absente": 0,
    }
    for s in sections:
        st = s.get("statut", "")
        if st == "A JOUR":
            d["a_jour"] += 1
        elif st == "EN RETARD":
            d["en_retard"] += 1
        elif st == "A REVOIR":
            d["a_revoir"] += 1
        elif st == "SECTION ABSENTE":
            d["section_absente"] += 1
    return d


def main():
    rapport = mv.analyser_registre()

    if "erreur" in rapport:
        raise SystemExit(rapport["erreur"])

    rapport["schema_version"] = SCHEMA_VERSION
    rapport["registre"] = str(mv.REGISTRE)
    rapport["resume"] = resume(rapport["sections"])

    SORTIE.parent.mkdir(parents=True, exist_ok=True)
    SORTIE.write_text(
        json.dumps(rapport, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"Ecrit : {SORTIE}")


if __name__ == "__main__":
    main()
