"""
monte_carlo.py — Module Monte-Carlo pour analyse de problemes de terrain
PMDQ v2.7.5

Simule N scenarios pour repondre a un probleme :
    - Depassement de cout d'un contrat
    - Malus estime (50 % du surcoût imputable)
    - Recette fiscale esperee
    - Probabilite que la cause soit superficielle

Usage :
    python3 monte_carlo.py              # mode interactif
    python3 monte_carlo.py --demo       # mode demonstration
"""
import json
from datetime import date
from pathlib import Path

# ---------------------------------------------------------------------
# Parametres globaux
# ---------------------------------------------------------------------

N_SIMULATIONS = 10_000
SEUIL_MALUS = 0.50      # 50 % du surcoût imputable
GRAINE = 42             # reproductibilite

# Causes classifiees
CAUSES = {
    "superficielles": [
        "temperature exceptionnelle",
        "hausse du transport",
        "prix des biens",
        "ca marchait pas",
        "erreur de planification",
        "sous-estimation volontaire",
    ],
    "profondes": [
        "tremblement de terre",
        "guerre",
        "pandemie imprevisible",
        "decouverte archeologique",
        "force majeure documentee",
        "changement de loi en cours de projet",
    ],
}

import numpy as np


def classifier_cause(cause, historique_firme):
    """
    Classe une cause comme superficielle ou profonde.
    Retourne un score de superficialite entre 0 et 1.
    """
    cause_lower = cause.lower()
    for c in CAUSES["superficielles"]:
        if c in cause_lower or cause_lower in c:
            return 1.0
    for c in CAUSES["profondes"]:
        if c in cause_lower or cause_lower in c:
            return 0.0
    # Cause inconnue : depend de l'historique
    return min(1.0, historique_firme / 5.0)


def simuler_probleme(contrat_M, marge_prevue, depassement_M,
                     cause, historique_firme, n=N_SIMULATIONS, graine=GRAINE):
    """
    Simule N scenarios Monte-Carlo pour un probleme de depassement.
    Retourne les statistiques cles.
    """
    rng = np.random.default_rng(graine)

    # Score de superficialite (0 = profonde, 1 = superficielle)
    score = classifier_cause(cause, historique_firme)

    # Marge de risque prevue au contrat
    marge_M = contrat_M * marge_prevue

    # Part imputable = depassement au-dela de la marge
    part_imputable = max(0, depassement_M - marge_M)

    # Simulation : incertitude sur le score de superficialite
    # et sur la part imputable (variation +/- 20 %)
    scores_sim = np.clip(rng.normal(score, 0.15, n), 0, 1)
    parts_sim = np.clip(
        rng.normal(part_imputable, part_imputable * 0.20, n),
        0, None
    )

    # Malus = 50 % de la part imputable, pondere par le score
    malus_sim = SEUIL_MALUS * parts_sim * scores_sim

    # Statistiques
    return {
        "contrat_M$": contrat_M,
        "marge_prevue_M$": round(marge_M, 2),
        "depassement_M$": depassement_M,
        "part_imputable_M$": round(part_imputable, 2),
        "cause": cause,
        "score_superficialite": round(score, 3),
        "n_simulations": n,
        "malus_median_M$": round(float(np.median(malus_sim)), 3),
        "malus_moyen_M$": round(float(malus_sim.mean()), 3),
        "malus_ic_bas_M$": round(float(np.quantile(malus_sim, 0.025)), 3),
        "malus_ic_haut_M$": round(float(np.quantile(malus_sim, 0.975)), 3),
        "probabilite_superficielle": round(float(np.mean(scores_sim > 0.5)), 3),
        "recette_fiscale_esperee_M$": round(float(malus_sim.mean()), 3),
    }

def afficher_rapport(r):
    """Affiche le rapport Monte-Carlo de facon lisible."""
    print()
    print("=" * 65)
    print("  MONTE-CARLO — PMDQ v2.7.5")
    print("=" * 65)
    print()
    print(f"  Contrat                : {r['contrat_M$']} M$")
    print(f"  Marge prevue           : {r['marge_prevue_M$']} M$")
    print(f"  Depassement observe    : {r['depassement_M$']} M$")
    print(f"  Part imputable         : {r['part_imputable_M$']} M$")
    print(f"  Cause invoquee         : {r['cause']}")
    print()
    print(f"  Score de superficialite : {r['score_superficialite']} (0=profonde, 1=superficielle)")
    print(f"  Simulations            : {r['n_simulations']}")
    print()
    print(f"  --- Resultats ---")
    print(f"  Probabilite superficielle : {r['probabilite_superficielle']*100:.1f} %")
    print(f"  Malus median              : {r['malus_median_M$']} M$")
    print(f"  Malus moyen               : {r['malus_moyen_M$']} M$")
    print(f"  IC 95 %                   : [{r['malus_ic_bas_M$']} ; {r['malus_ic_haut_M$']}] M$")
    print(f"  Recette fiscale esperee   : {r['recette_fiscale_esperee_M$']} M$")
    print()
    print("=" * 65)


def mode_interactif():
    """Pose les questions et lance la simulation."""
    print()
    print("=== MODE INTERACTIF ===")
    print()
    try:
        contrat = float(input("Montant du contrat (M$) : "))
        marge = float(input("Marge prevue au contrat (%, ex: 10) : ")) / 100
        depassement = float(input("Depassement observe (M$) : "))
        cause = input("Cause invoquee : ")
        historique = int(input("Historique de depassements de la firme (nombre) : "))
    except ValueError:
        print("Erreur : entrez des nombres valides.")
        return

    r = simuler_probleme(contrat, marge, depassement, cause, historique)
    afficher_rapport(r)


def mode_demo():
    """Execute deux exemples pour valider le moteur."""
    print()
    print("=== MODE DEMONSTRATION ===")

    # Cas 1 : cause superficielle
    print()
    print("--- Cas 1 : cause superficielle (temperature) ---")
    r1 = simuler_probleme(
        contrat_M=100,
        marge_prevue=0.10,
        depassement_M=25,
        cause="temperature exceptionnelle",
        historique_firme=3,
    )
    afficher_rapport(r1)

    # Cas 2 : cause profonde
    print()
    print("--- Cas 2 : cause profonde (tremblement de terre) ---")
    r2 = simuler_probleme(
        contrat_M=100,
        marge_prevue=0.10,
        depassement_M=25,
        cause="tremblement de terre",
        historique_firme=0,
    )
    afficher_rapport(r2)


if __name__ == "__main__":
    import sys
    if "--demo" in sys.argv:
        mode_demo()
    else:
        mode_interactif()
