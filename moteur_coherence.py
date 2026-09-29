#!/usr/bin/env python3
"""
moteur_coherence.py — Verification de coherence inter-moteurs
PMDQ v2.7.7

Croise les sorties JSON des autres moteurs et signale les incoherences.

Usage :
    python3 moteur_coherence.py
    python3 moteur_coherence.py --json coherence.json
"""

import argparse
import json
import os
import sys
from datetime import date
from pathlib import Path


SOURCES = Path("sources")

FICHIERS = {
    "domar": SOURCES / "domar_topologie.json",
    "etancheite": SOURCES / "etancheite_budgetaire.json",
    "provisionnement": SOURCES / "provisionnement_topologie.json",
    "rendement": SOURCES / "rendement_topologie.json",
    "vehicule": SOURCES / "vehicule_topologie.json",
}


def charger(nom):
    p = FICHIERS.get(nom)
    if p is None:
        return None, f"Fichier inconnu : {nom}"
    if not p.exists():
        return None, f"Absent : {p}"
    try:
        return json.loads(p.read_text(encoding="utf-8")), None
    except (OSError, ValueError) as e:
        return None, f"Illisible : {e}"


def verifier_presence():
    resultats = []
    for nom, p in FICHIERS.items():
        if p.exists():
            taille = p.stat().st_size
            resultats.append({
                "regle": f"Presence {nom}",
                "statut": "OK" if taille > 0 else "VIDE",
                "detail": f"{taille} octets",
            })
        else:
            resultats.append({
                "regle": f"Presence {nom}",
                "statut": "ABSENT",
                "detail": str(p),
            })
    return resultats


def verifier_constantes():
    resultats = []

    # PIB 2026 : chercher dans les moteurs qui le declarent
    pib_trouves = {}
    for nom in ("domar", "etancheite", "provisionnement"):
        data, _ = charger(nom)
        if data is None or not isinstance(data, dict):
            continue
        for cle in ("pib_2026", "PIB_2026", "pib"):
            if cle in data:
                pib_trouves[nom] = data[cle]
                break

    if not pib_trouves:
        resultats.append({
            "regle": "PIB 2026",
            "statut": "NON VERIFIABLE",
            "detail": "Aucune valeur trouvee",
        })
    elif len(set(str(v) for v in pib_trouves.values())) == 1:
        val = list(pib_trouves.values())[0]
        resultats.append({
            "regle": "PIB 2026",
            "statut": "COHERENT",
            "detail": f"{val} dans {len(pib_trouves)} moteur(s)",
        })
    else:
        resultats.append({
            "regle": "PIB 2026",
            "statut": "INCOHERENT",
            "detail": str(pib_trouves),
        })

    # Dette initiale
    data, _ = charger("domar")
    if data and isinstance(data, dict):
        dette = None
        for cle in ("d_initiale", "dette_initiale", "d0", "d"):
            if cle in data:
                dette = data[cle]
                break
        resultats.append({
            "regle": "Dette initiale (domar)",
            "statut": "TROUVE" if dette is not None else "ABSENTE",
            "detail": str(dette) if dette is not None else "Cle introuvable",
        })
    else:
        resultats.append({
            "regle": "Dette initiale (domar)",
            "statut": "NON VERIFIABLE",
            "detail": "domar illisible",
        })

    return resultats


def verifier_cles_attendues():
    """Verifie que chaque JSON contient les cles attendues."""
    attendues = {
        "domar": ["scenarios"],
        "etancheite": [],
        "provisionnement": [],
        "rendement": [],
        "vehicule": [],
    }
    resultats = []
    for nom, cles in attendues.items():
        if not cles:
            continue
        data, err = charger(nom)
        if data is None:
            resultats.append({
                "regle": f"Cles {nom}",
                "statut": "NON VERIFIABLE",
                "detail": err,
            })
            continue
        manquantes = [c for c in cles if not isinstance(data, dict) or c not in data]
        if manquantes:
            resultats.append({
                "regle": f"Cles {nom}",
                "statut": "INCOMPLET",
                "detail": f"manque : {manquantes}",
            })
        else:
            resultats.append({
                "regle": f"Cles {nom}",
                "statut": "OK",
                "detail": f"{len(cles)} cle(s) attendue(s) presente(s)",
            })
    return resultats


def analyser():
    resultats = []
    resultats.extend(verifier_presence())
    resultats.extend(verifier_constantes())
    resultats.extend(verifier_cles_attendues())

    resume = {
        "total": len(resultats),
        "ok": sum(1 for r in resultats if r["statut"] in ("OK", "COHERENT", "TROUVE")),
        "alerte": sum(1 for r in resultats if r["statut"] in ("ABSENT", "VIDE", "INCOHERENT", "INCOMPLET")),
        "info": sum(1 for r in resultats if r["statut"] in ("NON VERIFIABLE", "ABSENTE")),
    }

    return {
        "date_analyse": str(date.today()),
        "regles": resultats,
        "resume": resume,
    }


def afficher(rapport):
    print()
    print("=" * 78)
    print("  MOTEUR COHERENCE INTER-MOTEURS — PMDQ v2.7.7")
    print("=" * 78)
    print(f"  Date : {rapport['date_analyse']}")
    print()
    print(f"  {'Regle':<35} {'Statut':<18} {'Detail'}")
    print("  " + "-" * 74)
    for r in rapport["regles"]:
        detail = r.get("detail", "")
        if len(detail) > 35:
            detail = detail[:32] + "..."
        print(f"  {r['regle']:<35} {r['statut']:<18} {detail}")
    print()
    res = rapport["resume"]
    print(f"  Bilan : {res['total']} regles, {res['ok']} OK, {res['alerte']} alerte(s)")
    print("=" * 78)
    print()


def main():
    parser = argparse.ArgumentParser(
        description="Verification de coherence inter-moteurs"
    )
    parser.add_argument("--json", type=str, default=None)
    args = parser.parse_args()

    rapport = analyser()
    afficher(rapport)

    if args.json:
        with open(args.json, "w", encoding="utf-8") as f:
            json.dump(rapport, f, indent=2, ensure_ascii=False)
        print(f"Rapport sauvegarde : {args.json}")

    if os.environ.get("PMDQ_BLOQUANT"):
        if rapport["resume"]["alerte"] > 0:
            sys.exit(2)


if __name__ == "__main__":
    main()
