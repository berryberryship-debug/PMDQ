#!/usr/bin/env python3
"""moteur_nomenclature.py — Analyse catalogue composants vehicule"""

import argparse
import importlib.util
import os
import sys
from pathlib import Path

CATALOGUE_DEFAUT = "investissement/vehicule_biplace/nomenclature_C.py"


def charger_catalogue(chemin):
    spec = importlib.util.spec_from_file_location("catalogue", chemin)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def analyser(catalogue):
    composants = catalogue.COMPOSANTS
    volume = getattr(catalogue, "VOLUME_CIBLE", 10)
    marge = getattr(catalogue, "MARGE_UNITAIRE_PCT", 25)

    total = 0
    part_qc_valeur = 0
    par_sous_systeme = {}

    for c in composants:
        sous_total = c["quantite"] * c["prix_unitaire"]
        total += sous_total
        part_qc_valeur += sous_total * c["part_qc_pct"] / 100
        ss = c["sous_systeme"]
        if ss not in par_sous_systeme:
            par_sous_systeme[ss] = {"total": 0, "part_qc": 0, "nb": 0}
        par_sous_systeme[ss]["total"] += sous_total
        par_sous_systeme[ss]["part_qc"] += sous_total * c["part_qc_pct"] / 100
        par_sous_systeme[ss]["nb"] += 1

    part_qc_pct = (part_qc_valeur / total * 100) if total else 0

    cout_serie = 0
    for c in composants:
        sous_total = c["quantite"] * c["prix_unitaire"]
        if c["sous_systeme"] == "Assemblage":
            cout_serie += sous_total * 0.70
        else:
            cout_serie += sous_total * 0.85

    prix_vente = cout_serie * (1 + marge / 100)

    return {
        "categorie": catalogue.CATEGORIE,
        "version": catalogue.VERSION,
        "nb_composants": len(composants),
        "cout_prototype": round(total, 2),
        "part_qc_valeur": round(part_qc_valeur, 2),
        "part_qc_pct": round(part_qc_pct, 1),
        "par_sous_systeme": par_sous_systeme,
        "volume_cible": volume,
        "cout_serie_unitaire": round(cout_serie, 2),
        "marge_pct": marge,
        "prix_vente_unitaire": round(prix_vente, 2),
        "revenu_serie": round(prix_vente * volume, 2),
        "cout_serie_total": round(cout_serie * volume, 2),
    }


def afficher(r):
    print()
    print("=" * 78)
    print(f"  NOMENCLATURE — {r['categorie']} (v{r['version']})")
    print("=" * 78)
    print(f"  Composants             : {r['nb_composants']}")
    print(f"  Cout prototype         : {r['cout_prototype']:>12,.2f} $")
    print(f"  Part quebecoise        : {r['part_qc_valeur']:>12,.2f} $ ({r['part_qc_pct']} %)")
    print()
    print(f"  Volume cible serie     : {r['volume_cible']}")
    print(f"  Cout unitaire serie    : {r['cout_serie_unitaire']:>12,.2f} $")
    print(f"  Marge                  : {r['marge_pct']} %")
    print(f"  Prix de vente unitaire : {r['prix_vente_unitaire']:>12,.2f} $")
    print(f"  Revenu serie           : {r['revenu_serie']:>12,.2f} $")
    print(f"  Cout serie total       : {r['cout_serie_total']:>12,.2f} $")
    print()
    print("  Ventilation par sous-systeme :")
    print(f"    {'Sous-systeme':<20} {'Cout ($)':>12} {'Part QC ($)':>12} {'Nb':>4}")
    print("    " + "-" * 52)
    for ss, data in sorted(r["par_sous_systeme"].items(), key=lambda x: -x[1]["total"]):
        print(f"    {ss:<20} {data['total']:>12,.2f} {data['part_qc']:>12,.2f} {data['nb']:>4}")
    print()
    print("=" * 78)
    print()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--catalogue", type=str, default=CATALOGUE_DEFAUT)
    args = parser.parse_args()

    chemin = Path(args.catalogue)
    if not chemin.exists():
        print(f"Catalogue introuvable : {chemin}")
        sys.exit(1)

    catalogue = charger_catalogue(chemin)
    resultat = analyser(catalogue)
    afficher(resultat)

    if os.environ.get("PMDQ_BLOQUANT") and resultat["part_qc_pct"] < 30:
        print(f"ATTENTION : part quebecoise faible ({resultat['part_qc_pct']} %).")
        sys.exit(2)


if __name__ == "__main__":
    main()
