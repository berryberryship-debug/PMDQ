"""
moteur_domar.py — Solveur SFC / Domar
PMDQ v2.7.5 — Module 2 (version corrigée, cohérente avec le Livre V)

Modélise la dynamique d'endettement :
    s* = [(i - g) / (1 + g)] × d

où :
    s* = solde primaire stabilisant (% du PIB)
    i  = taux d'intérêt effectif
    g  = taux de croissance NOMINALE
    d  = ratio dette brute / PIB

Références :
    - 05_livre_V_dette_domar.html : scénarios 2,11 / 5,02 / 9,91 G$
    - Finances Québec : g réel 2026 = 1,1 % [M]
"""
import numpy as np
from scipy.integrate import solve_ivp
import json
from pathlib import Path
from datetime import date

# --- Paramètres validés ---
D_INITIALE = 0.423       # [C] ratio dette brute / PIB
PIB_2026 = 644.55        # [C] G$, dérivé
DETTE_BRUTE = 272.644    # [M] G$, 31 mars 2026

# --- Scénarios du Livre V ---
SCENARIOS = {
    "Favorable":   {"i": 0.0400, "g": 0.0320},
    "Central":     {"i": 0.0460, "g": 0.0271},
    "Défavorable": {"i": 0.0550, "g": 0.0180},
}

def calculer_effort_primaire(i, g, d):
    """Solde primaire stabilisant : s* = [(i - g) / (1 + g)] × d"""
    return ((i - g) / (1 + g)) * d

def simuler_horizon(i, g, d0, effort_G, pib0, annees=25):
    """
    Simule la trajectoire DISCRÈTE annuelle :
        d_t = [(1 + i) / (1 + g)] × d_{t-1} − s_t
    où s_t = effort_G / PIB_t, et PIB_t = PIB_0 × (1 + g)^t.
    L'effort est constant en G$, mais la fraction du PIB décroît.
    """
    d = [d0]
    for t in range(1, annees + 1):
        pib_t = pib0 * ((1 + g) ** t)
        s_t = effort_G / pib_t
        d_next = ((1 + i) / (1 + g)) * d[-1] - s_t
        d.append(d_next)
    return d

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
    print("=" * 72)
    print("MOTEUR DOMAR — PMDQ v2.7.5 (cohérent avec le Livre V)")
    print("=" * 72)
    print(f"d (dette brute / PIB) : {D_INITIALE*100:.1f} % [C]")
    print(f"PIB implicite 2026    : {PIB_2026:.2f} G$ [C]")
    print()

    resultats = {
        "date_calcul": str(date.today()),
        "parametres": {
            "d": {"valeur": D_INITIALE, "statut": "[C]"},
            "PIB_2026": {"valeur": PIB_2026, "statut": "[C]"},
            "note": "g = croissance NOMINALE (pas réelle). g réel 2026 = 1,1 % [M]."
        },
        "scenarios": []
    }

    print(f"{'Scénario':<15} {'i':>8} {'g':>8} {'i-g':>8} {'s* (% PIB)':>12} {'s* (G$)':>12}")
    print("-" * 72)

    for nom, params in SCENARIOS.items():
        i, g = params["i"], params["g"]
        s_star = calculer_effort_primaire(i, g, D_INITIALE)
        effort_g = s_star * PIB_2026

        print(f"{nom:<15} {i*100:>7.2f} % {g*100:>7.2f} % {(i-g)*100:>7.2f} % {s_star*100:>10.3f} % {effort_g:>10.2f} G$")

        resultats["scenarios"].append({
            "nom": nom,
            "i": i, "g": g,
            "i_minus_g": round((i - g) * 100, 2),
            "s_star_pct": round(s_star * 100, 3),
            "effort_G$": round(effort_g, 2),
        })

    # --- Test de trajectoire sur 25 ans avec effort central fixe ---
    print()
    print("=" * 72)
    print("TRAJECTOIRES SUR 25 ANS — effort fixe = 5,02 G$/an")
    print("=" * 72)
    s_central = calculer_effort_primaire(SCENARIOS["Central"]["i"], SCENARIOS["Central"]["g"], D_INITIALE)

    for nom, params in SCENARIOS.items():
        effort_central_G = s_central * PIB_2026
        sol = simuler_horizon(params["i"], params["g"], D_INITIALE, effort_central_G, PIB_2026, annees=25)
        d_final = sol[-1] * 100
        tendance = "baisse" if d_final < D_INITIALE*100 else ("stable" if abs(d_final - D_INITIALE*100) < 0.5 else "explose")
        print(f"  {nom:<15} → d(25 ans) = {d_final:>6.1f} %  ({tendance})")
        resultats["scenarios"][list(SCENARIOS.keys()).index(nom)]["d_final_25ans"] = round(d_final, 1)

    # --- Sauvegarde ---
    with open("sources/domar_topologie.json", "w", encoding="utf-8") as f:
        json.dump(resultats, f, indent=2, ensure_ascii=False)
    print()
    print("Résultats sauvegardés : sources/domar_topologie.json")

if __name__ == "__main__":
    main()
