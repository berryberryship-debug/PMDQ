"""
moteur_rendement.py — Rendement collectif D et cycle de vie
PMDQ v2.7.7 — Module 3

Vérifie le seuil D > 1,30 (Article 18) et applique le taux
d'actualisation social (Article 19).

Implémentation numpy pure (pas de numpy_financial/QuantLib — ARM64 compatible).

Formules :
    VAN = -C0 + Σ (CF_t / (1 + r)^t)
    D = Valeur créée nette / Coût total
    Seuil : D > 1,30

Taxonomie (Article 14) :
    R, Ré, É → inclus dans les flux
    Co       → EXCLU (réserve de contingence seulement)
"""
import numpy as np
import os
import sys
import json
from datetime import date
from pathlib import Path

# --- Paramètres (Livre V, hypothèse centrale documentée) ---
TAUX_ACTUALISATION_SOCIAL = 0.035  # [T] 3,5 % — hypothèse centrale documentée
SEUIL_D = 1.30                     # [M] Article 18

# --- Projets à évaluer (exemples indicatifs [P]) ---
PROJETS = [
    {
        "nom": "Plantation d'arbres — 20 quartiers",
        "C0": 2.28,           # G$ investissement initial
        "flux_annuels": [0.47] * 10,  # G$/an (usufruit + clim évitée) × 10 ans
        "categorie": "É",     # admissible
    },
    {
        "nom": "MOD-ECO-CIRC-2025",
        "C0": 6.0,            # G$ CAPEX
        "flux_annuels": [5.43] * 3,  # G$/an × 3 ans (enveloppe marketing)
        "categorie": "É",
    },
    {
        "nom": "Mobilité urbaine — prototype",
        "C0": 1.275,          # G$ (borne haute : 1 275 k$ = 1,275 G$? Non, 1 275 k$ = 1,275 M$)
        "flux_annuels": [],   # Pas de revenus à ce stade — projet [P]
        "categorie": "Co",    # exclu
    },
]

def van(c0, flux, r):
    """Valeur actualisée nette."""
    actualises = [cf / ((1 + r) ** (t + 1)) for t, cf in enumerate(flux)]
    return -c0 + sum(actualises)

def ratio_d(c0, flux, r):
    """
    Ratio D = Valeur créée nette / Coût total
    Selon Article 17 : D = Valeur créée nette / Coût total
    On actualise les flux et on divise par le coût initial actualisé.
    """
    if c0 == 0:
        return float('inf')
    val_actualisee = sum(cf / ((1 + r) ** (t + 1)) for t, cf in enumerate(flux))
    return val_actualisee / c0

def evaluer_projet(projet, r, seuil):
    """Évalue un projet selon l'Article 18."""
    c0 = projet["C0"]
    flux = projet["flux_annuels"]
    categorie = projet["categorie"]

    # Exclusion stricte des Co
    if categorie == "Co":
        return {
            "nom": projet["nom"],
            "statut": "EXCLU",
            "raison": "Catégorie Co — non admissible (Article 14)",
            "van": None,
            "D": None,
            "conforme": False
        }

    if not flux:
        return {
            "nom": projet["nom"],
            "statut": "SANS_FLUX",
            "raison": "Aucun flux à évaluer",
            "van": None,
            "D": None,
            "conforme": False
        }

    van_val = van(c0, flux, r)
    d_val = ratio_d(c0, flux, r)
    conforme = d_val > seuil

    return {
        "nom": projet["nom"],
        "statut": "CONFORME" if conforme else "REJETÉ",
        "categorie": categorie,
        "C0_G$": c0,
        "van_G$": round(van_val, 3),
        "D": round(d_val, 3),
        "seuil": seuil,
        "conforme": conforme
    }

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
    print("MOTEUR DE RENDEMENT D — PMDQ v2.7.7")
    print("=" * 72)
    print(f"Taux d'actualisation social : {TAUX_ACTUALISATION_SOCIAL*100:.1f} % [T]")
    print(f"Seuil D (Article 18)        : {SEUIL_D} [M]")
    print()

    resultats = {
        "date_calcul": str(date.today()),
        "taux_actualisation_social": TAUX_ACTUALISATION_SOCIAL,
        "seuil_D": SEUIL_D,
        "projets": []
    }

    print(f"{'Projet':<45} {'Cat.':>5} {'VAN (G$)':>10} {'D':>7} {'Statut':>12}")
    print("-" * 82)

    for p in PROJETS:
        res = evaluer_projet(p, TAUX_ACTUALISATION_SOCIAL, SEUIL_D)
        cat = p.get("categorie", "—")
        van_aff = f"{res['van_G$']:.2f}" if res.get("van_G$") is not None else "—"
        d_aff = f"{res['D']:.2f}" if res.get("D") is not None else "—"
        print(f"{res['nom']:<45} {cat:>5} {van_aff:>10} {d_aff:>7} {res['statut']:>12}")
        resultats["projets"].append(res)

    print()

    # Test de sensibilité au taux d'actualisation
    print("=" * 72)
    print("TEST DE SENSIBILITÉ AU TAUX D'ACTUALISATION")
    print("=" * 72)
    taux_test = [0.02, 0.035, 0.05, 0.07]
    print(f"{'Projet':<45}", end="")
    for t in taux_test:
        print(f"{t*100:>8.1f} %", end="")
    print()
    print("-" * 82)
    for p in PROJETS:
        if p["categorie"] == "Co" or not p["flux_annuels"]:
            continue
        print(f"{p['nom']:<45}", end="")
        for t in taux_test:
            d_val = ratio_d(p["C0"], p["flux_annuels"], t)
            print(f"{d_val:>8.2f}", end="")
        print()

    print()
    print("Note : le seuil D > 1,30 doit être atteint pour tout projet admissible.")
    print("       Les catégories Co sont automatiquement exclues.")

    # Sauvegarde
    with open("sources/rendement_topologie.json", "w", encoding="utf-8") as f:
        json.dump(resultats, f, indent=2, ensure_ascii=False)
    print()
    print("Rapport sauvegardé : sources/rendement_topologie.json")

if __name__ == "__main__":
    main()
