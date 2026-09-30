#!/usr/bin/env python3
"""Vérificateur du chiffrage prototype VÉHICULE URBAIN LÉGER.
Compare les totaux attendus aux calculs, contrôle la cohérence.
"""
import sys


PHASES = {
    "Phase 1 - Étude et faisabilité": [
        ("Analyse fonctionnelle", 15_000, 35_000),
        ("Étude de marché", 10_000, 25_000),
        ("Analyse réglementaire", 15_000, 40_000),
        ("Architecture préliminaire", 20_000, 50_000),
        ("PI antériorité et FTO", 20_000, 60_000),
    ],
    "Phase 2 - Conception détaillée": [
        ("Ingénierie mécanique", 60_000, 150_000),
        ("Ingénierie électrique et batterie", 35_000, 80_000),
        ("Ingénierie thermique", 15_000, 40_000),
        ("Conception carrosserie", 20_000, 50_000),
        ("Dossier PI", 15_000, 40_000),
    ],
    "Phase 3 - Prototypage et essais": [
        ("Prototypage physique", 80_000, 200_000),
        ("Essais de sécurité", 40_000, 100_000),
        ("Essais fonctionnels", 25_000, 60_000),
        ("Conformité et homologation", 20_000, 50_000),
        ("Pilote avec usagers", 30_000, 80_000),
    ],
    "Phase 4 - Coordination et gestion": [
        ("Gestion de projet", 25_000, 60_000),
        ("Conseil juridique", 15_000, 40_000),
        ("Comptabilité analytique", 10_000, 25_000),
        ("Communication", 10_000, 30_000),
    ],
}

ATTENDU = {
    "Phase 1 - Étude et faisabilité": (80_000, 210_000),
    "Phase 2 - Conception détaillée": (145_000, 360_000),
    "Phase 3 - Prototypage et essais": (195_000, 490_000),
    "Phase 4 - Coordination et gestion": (60_000, 155_000),
}


def main():
    print("=" * 65)
    print("  VÉRIFICATION — PROJET VÉHICULE URBAIN LÉGER")
    print("=" * 65)

    total_min = 0
    total_max = 0
    tout_ok = True

    for phase, postes in PHASES.items():
        cmin = sum(p[1] for p in postes)
        cmax = sum(p[2] for p in postes)
        total_min += cmin
        total_max += cmax

        att_min, att_max = ATTENDU[phase]
        ok = (cmin == att_min and cmax == att_max)
        if not ok:
            tout_ok = False

        statut = "OK" if ok else "ECART"
        print(f"\n[{statut}] {phase}")
        print(f"  min : {cmin:>9,} (attendu {att_min:>9,})")
        print(f"  max : {cmax:>9,} (attendu {att_max:>9,})")

    print()
    print("=" * 65)
    print(f"TOTAL : {total_min:,} – {total_max:,} CAD")
    print(f"Prototype allégé (170k) < min projet complet : {170_000 < total_min}")
    print(f"Ratio max/min : {total_max / total_min:.2f} (cible < 3.0)")
    print("=" * 65)

    return 0 if tout_ok else 1


if __name__ == "__main__":
    sys.exit(main())
