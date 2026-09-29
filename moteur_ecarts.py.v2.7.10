#!/usr/bin/env python3
"""
moteur_ecarts.py — Detection d'ecarts registre / cache officiel
PMDQ v2.7.10

Compare les valeurs declarees dans le registre humain aux valeurs
officielles du cache economique, pour les variables explicitement
listees dans ECARTS_SUIVIS.

Usage :
    python3 moteur_ecarts.py
    python3 moteur_ecarts.py --json ecarts.json
"""

import argparse
import json
import os
import re
import sys
import unicodedata
from datetime import date
from pathlib import Path


REGISTRE = Path("sources/variables-sensibles.md")
CACHE = Path("sources/cache_economique.json")

# Correspondances : nom normalise du registre -> (cle cache, seuil absolu)
# Le seuil est dans l'unite de la variable comparee.
ECARTS_SUIVIS = {
    "inflation": ("taux_inflation_annuel", 0.5),
    "taux de change cad/usd": ("taux_change_usd_cad", 0.05),
    "taux d'interet effectif (r)": ("taux_directeur", 0.5),
    "taux d'interet effectif": ("taux_directeur", 0.5),
}


def normaliser(t):
    if not t:
        return ""
    t = unicodedata.normalize("NFKD", t)
    t = "".join(c for c in t if not unicodedata.combining(c))
    return " ".join(t.lower().split())


def extraire_nombre(s):
    """Extrait le premier nombre d'une chaine. Retourne None si aucun."""
    if not s:
        return None
    s = s.replace(",", ".")
    m = re.search(r"[-+]?\d+(?:\.\d+)?", s)
    return float(m.group(0)) if m else None


def parser_tableaux(contenu):
    """Extrait les lignes de tableaux du registre (nom, valeur)."""
    lignes = []
    for ligne in contenu.split("\n"):
        ligne = ligne.strip()
        if not ligne.startswith("|"):
            continue
        cells = [c.strip() for c in ligne.strip("|").split("|")]
        if len(cells) < 2:
            continue
        if cells[0].lower() == "variable":
            continue
        if all(set(c) <= set("-: ") for c in cells):
            continue
        lignes.append((cells[0], cells[1]))
    return lignes


def analyser():
    if not REGISTRE.exists():
        return {"erreur": f"Registre introuvable : {REGISTRE}"}
    if not CACHE.exists():
        return {"erreur": f"Cache introuvable : {CACHE} (lancer collecteur.py)"}

    cache = json.loads(CACHE.read_text(encoding="utf-8"))
    contenu = REGISTRE.read_text(encoding="utf-8")
    lignes = parser_tableaux(contenu)

    resultats = []
    vus = set()

    for nom, val_declaree in lignes:
        cle_norm = normaliser(nom)
        if cle_norm in vus:
            continue
        if cle_norm not in ECARTS_SUIVIS:
            continue
        vus.add(cle_norm)

        cle_cache, seuil = ECARTS_SUIVIS[cle_norm]
        info_cache = cache.get(cle_cache, {})
        val_officielle = info_cache.get("valeur")

        if val_officielle is None:
            resultats.append({
                "variable": nom,
                "declare": val_declaree,
                "officiel": None,
                "ecart": None,
                "seuil": seuil,
                "statut": "PAS DE CACHE",
                "date_officielle": None,
            })
            continue

        num = extraire_nombre(val_declaree)
        if num is None:
            resultats.append({
                "variable": nom,
                "declare": val_declaree,
                "officiel": val_officielle,
                "ecart": None,
                "seuil": seuil,
                "statut": "NON NUMERIQUE",
                "date_officielle": info_cache.get("date_observation"),
            })
            continue

        diff = abs(num - val_officielle)
        statut = "ECART" if diff > seuil else "OK"
        resultats.append({
            "variable": nom,
            "declare": num,
            "officiel": val_officielle,
            "ecart": round(diff, 3),
            "seuil": seuil,
            "statut": statut,
            "date_officielle": info_cache.get("date_observation"),
        })

    resume = {
        "total": len(resultats),
        "ok": sum(1 for r in resultats if r["statut"] == "OK"),
        "ecart": sum(1 for r in resultats if r["statut"] == "ECART"),
        "non_verifiable": sum(1 for r in resultats if r["statut"] in ("NON NUMERIQUE", "PAS DE CACHE")),
    }

    return {
        "date_analyse": str(date.today()),
        "ecarts": resultats,
        "resume": resume,
    }


def afficher(rapport):
    print()
    print("=" * 78)
    print("  MOTEUR ECARTS REGISTRE / CACHE OFFICIEL — PMDQ v2.7.10")
    print("=" * 78)
    print(f"  Date : {rapport['date_analyse']}")
    print()

    if not rapport["ecarts"]:
        print("  Aucune correspondance definie dans ECARTS_SUIVIS.")
        print("=" * 78)
        print()
        return

    print(f"  {'Variable':<35} {'Declare':>10} {'Officiel':>10} {'Ecart':>8} {'Statut':<15}")
    print("  " + "-" * 74)
    for r in rapport["ecarts"]:
        decl = r.get("declare", "-")
        off = r.get("officiel")
        ec = r.get("ecart")
        decl_s = f"{decl}" if isinstance(decl, (int, float)) else str(decl)[:10]
        off_s = f"{off}" if off is not None else "-"
        ec_s = f"{ec}" if ec is not None else "-"
        print(f"  {r['variable']:<35} {decl_s:>10} {off_s:>10} {ec_s:>8} {r['statut']:<15}")

    print()
    res = rapport["resume"]
    print(f"  Bilan : {res['total']} comparees, {res['ok']} OK, {res['ecart']} ecart(s), {res['non_verifiable']} non verifiable(s)")
    print("=" * 78)
    print()


def main():
    parser = argparse.ArgumentParser(description="Detection d'ecarts registre / cache")
    parser.add_argument("--json", type=str, default=None)
    args = parser.parse_args()

    rapport = analyser()
    if "erreur" in rapport:
        print(rapport["erreur"])
        sys.exit(1)

    afficher(rapport)

    if args.json:
        with open(args.json, "w", encoding="utf-8") as f:
            json.dump(rapport, f, indent=2, ensure_ascii=False)
        print(f"Rapport sauvegarde : {args.json}")

    if os.environ.get("PMDQ_BLOQUANT"):
        if rapport["resume"]["ecart"] > 0:
            sys.exit(2)


if __name__ == "__main__":
    main()
