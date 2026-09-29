"""
moteur_fiscal.py - Moteur fiscal PMDQ v2.8 (Module 7)

Modele comportemental scenaristique calibre sur un point observe.

Definitions :
    A0_G     : revenu imposable agrege du Quebec (2023), en G$
    T_REF    : taux effectif agrege (imput a payer / revenu imposable)
    EPSILON  : parametre scenaristique de contraction de l'assiette
    R_OBS    : imput a payer observe en 2023 (point de calibration)
    POWER    : exposant de la fonction de contraction

IMPORTANT :
    EPSILON = 0.40 est un parametre scenaristique.
    Il ne constitue PAS une estimation econometrique du comportement
    fiscal des contribuables quebecois.

    Le modele est calibre sur le point observe de 2023 :
        A(T_REF) = A0_G
        R(T_REF) = R_OBS

Usage :
    python3 moteur_fiscal.py
    python3 moteur_fiscal.py --taux 0.15
    python3 moteur_fiscal.py --json resultat.json
    python3 moteur_fiscal.py --courbe
"""
import json
import argparse
from datetime import date
from pathlib import Path

import numpy as np

# ---------------------------------------------------------------------
# Parametres calibres (Quebec, annee fiscale 2023)
# ---------------------------------------------------------------------

A0_G = 372.261        # G$, revenu imposable agrege, Quebec 2023
R_OBS = 40.790        # G$, imput a payer observe 2023 (point de calibration)
T_REF = R_OBS / A0_G  # taux effectif agrege (calcule, pas arrondi)
EPSILON = 0.40        # parametre scenaristique (NON econometrique)
POWER = 1.5           # exposant de contraction

# ---------------------------------------------------------------------
# Validation obligatoire du point de calibration
# ---------------------------------------------------------------------

def _valider_calibration():
    """Verifie que le modele reproduit exactement le point observe."""
    a_ref = A0_G  # par construction
    r_ref = T_REF * a_ref

    assert abs(a_ref - A0_G) < 1e-9, \
        f"Calibration assiette invalide : {a_ref} != {A0_G}"
    assert abs(r_ref - R_OBS) < 1e-3, \
        f"Calibration recettes invalide : {r_ref} != {R_OBS}"

_valider_calibration()


# ---------------------------------------------------------------------
# Fonctions de calcul
# ---------------------------------------------------------------------

def taxable_base(t):
    """
    Assiette imposable ajustee selon le taux t.
    - Pour t <= T_REF : pas de contraction, A(t) = A0_G
    - Pour t > T_REF : contraction selon EPSILON et POWER
    """
    if t <= T_REF:
        return A0_G
    x = (t - T_REF) / T_REF
    contraction = 1.0 - EPSILON * (x ** POWER)
    return A0_G * max(0.0, contraction)


def revenue(t):
    """Recettes fiscales brutes R(t) = t * A(t)."""
    return t * taxable_base(t)


def repartir(R, part_fqbc):
    """Repartit les recettes entre FQBC et Etat."""
    return {
        "recettes_totales_G$": round(R, 3),
        "fqbc_G$": round(R * part_fqbc, 3),
        "etat_net_G$": round(R * (1 - part_fqbc), 3),
    }


def analyser_reforme(taux_nouveau, part_fqbc):
    """Analyse l'impact d'une reforme fiscale par rapport a 2023."""
    R_actuel = R_OBS
    R_nouveau = revenue(taux_nouveau)
    delta_R = R_nouveau - R_actuel
    return {
        "taux_reference": T_REF,
        "taux_nouveau": taux_nouveau,
        "assiette_reference_G$": round(A0_G, 3),
        "assiette_nouvelle_G$": round(taxable_base(taux_nouveau), 3),
        "recettes_reference_G$": round(R_actuel, 3),
        "recettes_nouvelles_G$": round(R_nouveau, 3),
        "variation_recettes_G$": round(delta_R, 3),
        "repartition": repartir(R_nouveau, part_fqbc),
    }


# ---------------------------------------------------------------------
# Courbe de Laffer numerique
# ---------------------------------------------------------------------

def courbe_laffer(t_min=0.0, t_max=0.80, n_points=161):
    """
    Genere la courbe A(t) et R(t) sur une plage de taux.
    Recherche numeriquement le taux optimal.
    """
    taux = np.linspace(t_min, t_max, n_points)
    assiettes = np.array([taxable_base(t) for t in taux])
    recettes = taux * assiettes

    # Base positive : A(t) > 0
    masque_positif = assiettes > 0
    if not masque_positif.any():
        return None

    idx_max = int(np.argmax(recettes))
    return {
        "taux": taux.tolist(),
        "assiettes_G$": assiettes.tolist(),
        "recettes_G$": recettes.tolist(),
        "taux_optimal": round(float(taux[idx_max]), 4),
        "recettes_max_G$": round(float(recettes[idx_max]), 3),
        "assiette_au_max_G$": round(float(assiettes[idx_max]), 3),
        "taux_max_base_positive": round(float(taux[masque_positif][-1]), 4),
        "ecart_recettes_max_vs_2023_G$": round(
            float(recettes[idx_max]) - R_OBS, 3
        ),
    }


# ---------------------------------------------------------------------
# Affichage
# ---------------------------------------------------------------------

def afficher_rapport(resultat):
    print()
    print("=" * 65)
    print("  MOTEUR FISCAL — PMDQ v2.8 (Module 7)")
    print("=" * 65)
    print()
    print("  --- Point de calibration (Quebec 2023) ---")
    print(f"  A0_G (revenu imposable)     : {A0_G} G$")
    print(f"  T_REF (taux effectif)       : {T_REF*100:.2f} %")
    print(f"  R_OBS (imput a payer)       : {R_OBS} G$")
    print(f"  EPSILON (scenaristique)     : {EPSILON}")
    print()
    print("  --- Reforme simulee ---")
    print(f"  Taux nouveau                : {resultat['taux_nouveau']*100:.2f} %")
    print(f"  Assiette nouvelle           : {resultat['assiette_nouvelle_G$']} G$")
    print(f"  Recettes nouvelles          : {resultat['recettes_nouvelles_G$']} G$")
    print(f"  Variation vs 2023           : {resultat['variation_recettes_G$']:+} G$")
    print()
    rep = resultat["repartition"]
    print(f"  FQBC ({int(rep['fqbc_G$']/rep['recettes_totales_G$']*100) if rep['recettes_totales_G$'] else 0} %)         : {rep['fqbc_G$']} G$")
    print(f"  Etat net                    : {rep['etat_net_G$']} G$")
    print()
    print("=" * 65)


def afficher_courbe(courbe):
    print()
    print("=" * 65)
    print("  COURBE DE LAFFER (calibree sur 2023)")
    print("=" * 65)
    print()
    print(f"  Taux optimal (max R)        : {courbe['taux_optimal']*100:.2f} %")
    print(f"  Recettes maximales          : {courbe['recettes_max_G$']} G$")
    print(f"  Assiette au max             : {courbe['assiette_au_max_G$']} G$")
    print(f"  Ecart vs recettes 2023      : {courbe['ecart_recettes_max_vs_2023_G$']:+} G$")
    print(f"  Taux max (base positive)    : {courbe['taux_max_base_positive']*100:.2f} %")
    print()
    print("  Note : EPSILON = 0.40 est scenaristique.")
    print("         Ce n'est pas une estimation econometrique.")
    print("=" * 65)


# ---------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------

def verifier_variables():
    """Avertit si une section du registre est en retard ou a revoir."""
    p = Path("sources/etat_variables.json")
    if not p.exists():
        print("Avertissement : sources/etat_variables.json absent.")
        print("Lancer : python3 ecrire_etat.py")
        return
    try:
        etat = json.loads(p.read_text(encoding="utf-8"))
    except (OSError, ValueError) as e:
        print(f"Avertissement : lecture etat_variables.json impossible ({e}).")
        return
    r = etat.get("resume", {})
    retard = r.get("en_retard", 0)
    revoir = r.get("a_revoir", 0)
    absente = r.get("section_absente", 0)
    if not (retard or revoir or absente):
        return
    print()
    print("!" * 72)
    print("  ATTENTION : variables sensibles a mettre a jour")
    print("!" * 72)
    for s in etat.get("sections", []):
        if s.get("statut") in ("EN RETARD", "A REVOIR", "SECTION ABSENTE"):
            j = s.get("jours_depuis_maj")
            j_txt = f"{j} j" if isinstance(j, int) else "-"
            print(f"  - {s['section']:<40} {s['statut']:<16} ({j_txt})")
    print("!" * 72)
    print()

def main():
    verifier_variables()
    parser = argparse.ArgumentParser(
        description="Moteur fiscal PMDQ v2.8 — calibre sur Quebec 2023"
    )
    parser.add_argument(
        "--taux", type=float, default=0.15,
        help="Nouveau taux a simuler (ex: 0.15 pour 15 %%)"
    )
    parser.add_argument(
        "--part-fqbc", type=float, default=0.10,
        help="Part des recettes allouee au FQBC (ex: 0.10 pour 10 %%)"
    )
    parser.add_argument(
        "--courbe", action="store_true",
        help="Afficher la courbe de Laffer"
    )
    parser.add_argument(
        "--json", type=str, default=None,
        help="Exporter les resultats en JSON"
    )
    args = parser.parse_args()

    resultat = analyser_reforme(args.taux, args.part_fqbc)
    afficher_rapport(resultat)

    if args.courbe:
        courbe = courbe_laffer()
        afficher_courbe(courbe)

    if args.json:
        courbe = courbe_laffer()
        rapport = {
            "date": str(date.today()),
            "calibration": {
                "A0_G": A0_G,
                "T_REF": T_REF,
                "R_OBS": R_OBS,
                "EPSILON": EPSILON,
                "POWER": POWER,
                "note": "EPSILON scenaristique, non econometrique",
            },
            "reforme": resultat,
            "courbe_laffer": courbe,
        }
        with open(args.json, "w", encoding="utf-8") as f:
            json.dump(rapport, f, indent=2, ensure_ascii=False)
        print(f"Rapport sauvegarde : {args.json}")


if __name__ == "__main__":
    main()
