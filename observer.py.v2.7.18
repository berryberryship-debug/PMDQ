#!/usr/bin/env python3
"""
observer.py — Ajouter une observation manuelle au socle
PMDQ v2.7.18

Usage :
    python3 observer.py --liste
    python3 observer.py --cle prix_essence_quebec --valeur 1.95 --ville Sherbrooke
    python3 observer.py --cle prix_essence_quebec --valeur 1.95 --date 2026-10-15
"""

import argparse
import json
import sys
from datetime import date
from pathlib import Path


FICHIER = Path("sources/observations_manuelles.json")

CLES_CONNUES = {
    "prix_essence_quebec": {
        "unite": "$/L",
        "champ_localisation": "ville",
        "label_localisation": "Ville",
    },
    "indice_tsx": {
        "unite": "points",
        "champ_localisation": None,
    },
}


def charger():
    if not FICHIER.exists():
        return {
            "schema_version": "1.0",
            "description": "Observations manuelles",
            "observations": {},
        }
    return json.loads(FICHIER.read_text(encoding="utf-8"))


def sauver(data):
    FICHIER.parent.mkdir(parents=True, exist_ok=True)
    FICHIER.write_text(
        json.dumps(data, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )


def liste():
    data = charger()
    obs = data.get("observations", {})
    if not obs:
        print("Aucune observation enregistree.")
        return
    for cle, items in obs.items():
        info = CLES_CONNUES.get(cle, {})
        unite = info.get("unite", "")
        print(f"\n{cle} ({unite}) :")
        if not items:
            print("  (vide)")
            continue
        for item in sorted(items, key=lambda x: x.get("date", "")):
            local = ""
            champ = info.get("champ_localisation")
            if champ and item.get(champ):
                local = f" [{item[champ]}]"
            print(f"  {item.get('date', '?')}  {item.get('valeur', '?')}{local}")


def ajouter(args):
    if args.cle not in CLES_CONNUES:
        print(f"Cle inconnue : {args.cle}")
        print(f"Cles valides : {', '.join(CLES_CONNUES)}")
        sys.exit(1)

    data = charger()
    if "observations" not in data:
        data["observations"] = {}
    if args.cle not in data["observations"]:
        data["observations"][args.cle] = []

    info = CLES_CONNUES[args.cle]
    entree = {
        "date": args.date or str(date.today()),
        "valeur": args.valeur,
        "unite": info["unite"],
        "source": "observation directe",
    }
    if info.get("champ_localisation") and args.ville:
        entree[info["champ_localisation"]] = args.ville

    data["observations"][args.cle].append(entree)
    sauver(data)
    print(f"Ajoute : {args.cle} = {args.valeur} {info['unite']} ({entree['date']})")


def main():
    parser = argparse.ArgumentParser(description="Observations manuelles")
    parser.add_argument("--liste", action="store_true")
    parser.add_argument("--cle", type=str)
    parser.add_argument("--valeur", type=float)
    parser.add_argument("--date", type=str, default=None)
    parser.add_argument("--ville", type=str, default=None)
    args = parser.parse_args()

    if args.liste:
        liste()
    elif args.cle and args.valeur is not None:
        ajouter(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
