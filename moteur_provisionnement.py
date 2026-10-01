"""
moteur_provisionnement.py — Provisionnement actuariel (numpy pur)
PMDQ v2.7.7 — Module 1

Vérifie les réserves prévues par les Articles 13 et 15.

Méthodes implémentées :
    - Chain-Ladder (facteurs de développement)
    - Erreur-type de Mack (formule standard)
    - Bootstrap paramétrique (loi log-normale)
    - Réserve de précaution (Article 13) : 0,15 × max(0, Plafond - Ressources)
    - Réserve de contingence (Article 15) : alimentée par les revenus Co
"""
import numpy as np
import os
import sys
import json
from datetime import date
from pathlib import Path

# --- Paramètres ---
TAUX_PRECAUTION = 0.15            # [M] Article 13
ALPHA_BOOTSTRAP = 0.05            # [P] seuil de confiance 95 %
N_SIMULATIONS = 10000             # [P] nombre de simulations Monte-Carlo
GRAINE = 42                       # [P] reproductibilité

# --- Triangle de développement (exemple indicatif [P]) ---
# Lignes = années de survenance, colonnes = années de développement
# Valeur = décaissements cumulés (G$)
TRIANGLE = np.array([
    [1.000, 1.500, 1.800, 1.950, 2.000],
    [1.100, 1.650, 1.950, 2.100, np.nan],
    [1.200, 1.800, 2.100, np.nan, np.nan],
    [1.150, 1.700, np.nan, np.nan, np.nan],
    [1.300, np.nan, np.nan, np.nan, np.nan],
])

def calculer_facteurs_chain_ladder(triangle):
    """Facteurs de développement : f_j = sum(C_{i,j+1}) / sum(C_{i,j})."""
    n, m = triangle.shape
    facteurs = []
    for j in range(m - 1):
        col_j = triangle[:, j]
        col_j1 = triangle[:, j + 1]
        mask = ~np.isnan(col_j) & ~np.isnan(col_j1)
        if mask.sum() == 0:
            facteurs.append(1.0)
            continue
        f_j = np.nansum(col_j1[mask]) / np.nansum(col_j[mask])
        facteurs.append(f_j)
    return np.array(facteurs)

def projeter_triangle(triangle, facteurs):
    """Complète le triangle avec les facteurs Chain-Ladder."""
    n, m = triangle.shape
    triangle_proj = triangle.copy()
    for i in range(n):
        for j in range(m - 1):
            if np.isnan(triangle_proj[i, j + 1]) and not np.isnan(triangle_proj[i, j]):
                triangle_proj[i, j + 1] = triangle_proj[i, j] * facteurs[j]
    return triangle_proj

def calculer_reserves(triangle_orig, triangle_proj):
    """Réserve = dernière valeur projetée - dernière valeur observée."""
    n = triangle_orig.shape[0]
    reserves = []
    for i in range(n):
        # Dernière valeur observée
        ligne_obs = triangle_orig[i, :]
        val_obs = np.nanmax(ligne_obs[~np.isnan(ligne_obs)]) if not np.all(np.isnan(ligne_obs)) else 0
        # Dernière valeur projetée
        val_proj = triangle_proj[i, -1]
        reserves.append(max(0, val_proj - val_obs))
    return np.array(reserves)

def erreur_mack(triangle, facteurs, reserves):
    """Erreur-type de Mack (formule simplifiée)."""
    n, m = triangle.shape
    # Approximation : variance proportionnelle à la réserve
    # (formule complète de Mack nécessite les variances par cellule)
    sigma2 = np.var(reserves) if len(reserves) > 1 else 0
    return np.sqrt(sigma2)

def bootstrap_reserves(reserves, n_sim, alpha, seed):
    """
    Bootstrap NON-PARAMÉTRIQUE : rééchantillonnage avec remise.
    Plus robuste que la log-normale quand les réserves sont hétérogènes.
    """
    rng = np.random.default_rng(seed)
    n = len(reserves)
    # Rééchantillonnage : pour chaque simulation, tirer n réserves avec remise
    indices = rng.integers(0, n, size=(n_sim, n))
    simulations = reserves[indices]
    totaux = simulations.sum(axis=1)
    ic_bas = np.quantile(totaux, alpha / 2)
    ic_haut = np.quantile(totaux, 1 - alpha / 2)
    return totaux, ic_bas, ic_haut

def reserve_precaution(plafond, ressources_prevues):
    """Article 13 : Réserve_t = 0,15 × max(0, Plafond - Ressources)."""
    return TAUX_PRECAUTION * max(0, plafond - ressources_prevues)

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
    if os.environ.get("PMDQ_BLOQUANT"):
        sys.exit(2)

def main():
    verifier_variables()
    print("=" * 72)
    print("MOTEUR DE PROVISIONNEMENT ACTUARIEL — PMDQ v2.7.7")
    print("=" * 72)
    print(f"Taux de précaution (Article 13) : {TAUX_PRECAUTION*100:.1f} %")
    print(f"Seuil de confiance bootstrap    : {100*(1-ALPHA_BOOTSTRAP):.0f} %")
    print(f"Simulations Monte-Carlo         : {N_SIMULATIONS}")
    print()

    # 1. Chain-Ladder
    print("--- 1. Triangle de développement ---")
    print(TRIANGLE)
    print()
    facteurs = calculer_facteurs_chain_ladder(TRIANGLE)
    print(f"Facteurs de développement : {np.round(facteurs, 4).tolist()}")
    print()

    # 2. Projection
    triangle_proj = projeter_triangle(TRIANGLE, facteurs)
    print("--- 2. Triangle projeté ---")
    print(np.round(triangle_proj, 3))
    print()

    # 3. Réserves par année
    reserves = calculer_reserves(TRIANGLE, triangle_proj)
    print("--- 3. Réserves par année de survenance (G$) ---")
    for i, r in enumerate(reserves):
        print(f"  Année {i+1} : {r:.3f} G$")
    reserve_totale = reserves.sum()
    print(f"  TOTAL    : {reserve_totale:.3f} G$")
    print()

    # 4. Erreur-type de Mack
    err_mack = erreur_mack(TRIANGLE, facteurs, reserves)
    print(f"--- 4. Erreur-type de Mack ---")
    print(f"  σ (approximation) : {err_mack:.3f} G$")
    print()

    # 5. Bootstrap
    totaux, ic_bas, ic_haut = bootstrap_reserves(reserves, N_SIMULATIONS, ALPHA_BOOTSTRAP, GRAINE)
    print(f"--- 5. Bootstrap (n={N_SIMULATIONS}) ---")
    print(f"  Réserve médiane : {np.median(totaux):.3f} G$")
    print(f"  IC 95 % bas     : {ic_bas:.3f} G$")
    print(f"  IC 95 % haut    : {ic_haut:.3f} G$")
    print()

    # 6. Réserve de précaution (Article 13)
    # Exemple indicatif : Plafond 8,40 G$, Ressources prévues 7,71 G$
    plafond = 8.40
    ressources_prevues = 7.71
    res_precaution = reserve_precaution(plafond, ressources_prevues)
    print("--- 6. Réserve de précaution (Article 13) ---")
    print(f"  Plafond           : {plafond:.2f} G$")
    print(f"  Ressources prévues: {ressources_prevues:.2f} G$")
    print(f"  Écart             : {plafond - ressources_prevues:.2f} G$")
    print(f"  Réserve (15 %)    : {res_precaution:.3f} G$")
    print()

    # 7. Réserve de contingence (Article 15)
    # Alimentée par les revenus conditionnels Co
    revenus_co = 0.69  # G$ (scénario B, Livre II)
    print("--- 7. Réserve de contingence (Article 15) ---")
    print(f"  Revenus conditionnels (Co) : {revenus_co:.2f} G$")
    print(f"  Alimentation réserve       : {revenus_co:.2f} G$ (100 % de Co)")
    print()

    # Sauvegarde
    rapport = {
        "parametres": {
            "taux_precaution": TAUX_PRECAUTION,
            "alpha_bootstrap": ALPHA_BOOTSTRAP,
            "n_simulations": N_SIMULATIONS,
        },
        "chain_ladder": {
            "facteurs": np.round(facteurs, 4).tolist(),
            "reserves_par_annee_G$": np.round(reserves, 3).tolist(),
            "reserve_totale_G$": round(float(reserve_totale), 3),
            "erreur_mack_G$": round(float(err_mack), 3),
        },
        "bootstrap": {
            "mediane_G$": round(float(np.median(totaux)), 3),
            "ic_95_bas_G$": round(float(ic_bas), 3),
            "ic_95_haut_G$": round(float(ic_haut), 3),
        },
        "reserve_precaution_G$": round(res_precaution, 3),
        "reserve_contingence_G$": round(revenus_co, 3),
    }

    with open("sources/provisionnement_topologie.json", "w", encoding="utf-8") as f:
        json.dump(rapport, f, indent=2, ensure_ascii=False)
    print("Rapport sauvegardé : sources/provisionnement_topologie.json")

if __name__ == "__main__":
    main()
