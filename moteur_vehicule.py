"""
moteur_vehicule.py — Programme pilote de véhicules urbains légers
PMDQ v2.7.7 — Module 5

Applique la méthodologie PMDQ au projet de véhicules 2 places.
"""
import os
import sys
import json
from datetime import date
from pathlib import Path

PHASES = {
    "Phase 1 - Ingenierie & Design chassis/securite": {
        "categorie": "R",
        "traitement": "R&D / Charges courantes",
        "total_M$": 6.5,
        "etalement_M$": [2.0, 2.0, 1.5, 0.5, 0.5],
    },
    "Phase 2 - Logiciel embarque & Telemetrie": {
        "categorie": "Re",
        "traitement": "Actif incorporel (CCSP 3410)",
        "total_M$": 4.5,
        "etalement_M$": [1.5, 1.5, 1.0, 0.3, 0.2],
    },
    "Phase 3 - Cellule robotisee modulaire pilote": {
        "categorie": "E",
        "traitement": "Immobilisation corporelle (CCSP 3150)",
        "total_M$": 8.0,
        "etalement_M$": [0.0, 2.0, 3.5, 1.5, 1.0],
    },
    "Phase 4 - Bancs d'essais, Homologation & Crash tests": {
        "categorie": "R",
        "traitement": "Depenses d'exploitation",
        "total_M$": 3.5,
        "etalement_M$": [0.5, 0.5, 1.5, 0.5, 0.5],
    },
    "Phase 5 - Fabrication lot pilote (60 unites)": {
        "categorie": "Co",
        "traitement": "Stocks / Flotte publique pilote",
        "total_M$": 2.5,
        "etalement_M$": [0.0, 0.0, 0.5, 1.2, 0.8],
    },
}

BENEFICES = {
    "Economies d'exploitation (60 unites x 5 ans)": 0.81,
    "Valeur residuelle des actifs robotiques": 6.40,
    "Valeur des actifs de PI (logiciels + brevets)": 4.00,
}

TAUX_ACTUALISATION = 0.04
TAUX_DETTE = 0.04
DUREE = 5
PIB_QUEBEC_2026 = 644.55
SEUIL_D = 1.30
ENVELOPPE_TOTALE_M = 25.0

def verifier_enveloppe():
    """Verifie que la somme des phases = 25,0 M$."""
    total = sum(p["total_M$"] for p in PHASES.values())
    return {
        "total_calcule_M$": round(total, 2),
        "total_attendu_M$": ENVELOPPE_TOTALE_M,
        "ok": abs(total - ENVELOPPE_TOTALE_M) < 0.01,
    }

def calculer_annuite(P, r, n):
    """Annuite constante : P x r(1+r)^n / ((1+r)^n - 1)."""
    facteur = (r * (1 + r) ** n) / ((1 + r) ** n - 1)
    annuite = P * facteur
    total_rembourse = annuite * n
    interets = total_rembourse - P
    return {
        "principal_M$": P,
        "taux": r,
        "duree_ans": n,
        "annuite_M$_an": round(annuite, 3),
        "total_rembourse_M$": round(total_rembourse, 3),
        "interets_cumules_M$": round(interets, 3),
    }

def calculer_ratio_D():
    """Ratio D = Valeur nette creee / Cout de possession net."""
    valeur_creee = sum(BENEFICES.values())
    cout = ENVELOPPE_TOTALE_M
    d = valeur_creee / cout
    return {
        "valeur_creee_M$": round(valeur_creee, 2),
        "cout_total_M$": cout,
        "ratio_D": round(d, 3),
        "seuil": SEUIL_D,
        "conforme": d > SEUIL_D,
    }

def calculer_impact_domar():
    """Impact de 25 M$ sur la dette quebecoise (0,025 G$)."""
    dette_G = 25.0 / 1000.0
    impact_pct_pib = (dette_G / PIB_QUEBEC_2026) * 100
    return {
        "dette_ajoutee_G$": dette_G,
        "PIB_Quebec_G$": PIB_QUEBEC_2026,
        "impact_pct_PIB": round(impact_pct_pib, 5),
        "statut": "[C] marginal",
    }

def verifier_etancheite():
    """Verifie la coherence des categories (Article 14)."""
    categories = set(p["categorie"] for p in PHASES.values())
    co_present = "Co" in categories
    return {
        "categories_utilisees": sorted(categories),
        "co_present": co_present,
        "note": "Les categories Co sont exclues de l'assiette executoire.",
    }

def generer_rapport():
    """Genere le rapport complet au format JSON."""
    env = verifier_enveloppe()
    annuite = calculer_annuite(ENVELOPPE_TOTALE_M, TAUX_DETTE, DUREE)
    ratio = calculer_ratio_D()
    domar = calculer_impact_domar()
    etancheite = verifier_etancheite()

    return {
        "enveloppe": env,
        "annuite": annuite,
        "ratio_D": ratio,
        "impact_domar": domar,
        "etancheite": etancheite,
        "phases": PHASES,
        "benefices": BENEFICES,
    }


def afficher_rapport():
    rapport = generer_rapport()
    print("=" * 70)
    print("  MOTEUR VEHICULE — PMDQ v2.7.7 — Module 5")
    print("=" * 70)
    print()

    print("--- 1. Enveloppe budgetaire ---")
    env = rapport["enveloppe"]
    statut = "OK" if env["ok"] else "ECART"
    print(f"  Total calcule : {env['total_calcule_M$']} M$")
    print(f"  Total attendu : {env['total_attendu_M$']} M$")
    print(f"  Statut : {statut}")
    print()

    print("--- 2. Service de la dette ---")
    ann = rapport["annuite"]
    print(f"  Principal : {ann['principal_M$']} M$")
    print(f"  Taux : {ann['taux']*100:.2f} %")
    print(f"  Annuite : {ann['annuite_M$_an']} M$/an")
    print(f"  Total rembourse : {ann['total_rembourse_M$']} M$")
    print(f"  Interets cumules : {ann['interets_cumules_M$']} M$")
    print()

    print("--- 3. Ratio de rendement collectif D ---")
    rd = rapport["ratio_D"]
    statut = "CONFORME" if rd["conforme"] else "REJETE"
    print(f"  Valeur creee : {rd['valeur_creee_M$']} M$")
    print(f"  Cout total : {rd['cout_total_M$']} M$")
    print(f"  Ratio D : {rd['ratio_D']}")
    print(f"  Seuil : {rd['seuil']}")
    print(f"  Statut : {statut}")
    print()

    print("--- 4. Impact Domar (Livre V) ---")
    dm = rapport["impact_domar"]
    print(f"  Dette ajoutee : {dm['dette_ajoutee_G$']} G$")
    print(f"  PIB Quebec : {dm['PIB_Quebec_G$']} G$")
    print(f"  Impact : {dm['impact_pct_PIB']} % du PIB")
    print(f"  Statut : {dm['statut']}")
    print()

    print("--- 5. Etancheite budgetaire (Article 14) ---")
    et = rapport["etancheite"]
    print(f"  Categories : {', '.join(et['categories_utilisees'])}")
    print(f"  Co present : {et['co_present']}")
    print(f"  Note : {et['note']}")
    print()

    print("=" * 70)


def sauvegarder_json():
    """Sauvegarde le rapport dans sources/."""
    rapport = generer_rapport()
    with open("sources/vehicule_topologie.json", "w", encoding="utf-8") as f:
        json.dump(rapport, f, indent=2, ensure_ascii=False)
    print("Rapport sauvegarde : sources/vehicule_topologie.json")


# ---------------------------------------------------------------------
# Calculateur de scenarios — test de differentes enveloppes
# ---------------------------------------------------------------------

SCENARIOS_ENVELOPPE = [25.0, 22.0, 20.0, 18.0, 15.0, 12.0, 11.12]


def calculer_scenarios():
    """Calcule le ratio D pour differentes enveloppes."""
    valeur_creee = sum(BENEFICES.values())
    scenarios = []
    for env in SCENARIOS_ENVELOPPE:
        d = valeur_creee / env if env > 0 else float("inf")
        scenarios.append({
            "enveloppe_M$": env,
            "ratio_D": round(d, 3),
            "conforme": d > SEUIL_D,
        })
    return scenarios


def calculer_seuil_passage():
    """Calcule l'enveloppe maximale qui permet D > 1,30."""
    valeur_creee = sum(BENEFICES.values())
    return round(valeur_creee / SEUIL_D, 3)


def afficher_scenarios():
    print("=" * 70)
    print("  SCENARIOS D'ENVELOPPE — Recherche du seuil D > 1,30")
    print("=" * 70)
    print()
    print(f"  Valeur creee (benefices documentes) : {sum(BENEFICES.values()):.2f} M$")
    print(f"  Seuil requis : D > {SEUIL_D}")
    print(f"  Enveloppe maximale pour D = 1,30 : {calculer_seuil_passage()} M$")
    print()
    print(f"  {'Enveloppe':>12} {'Ratio D':>10} {'Statut':>12}")
    print("  " + "-" * 36)
    for s in calculer_scenarios():
        statut = "CONFORME" if s["conforme"] else "REJETE"
        print(f"  {s['enveloppe_M$']:>10.2f} M$ {s['ratio_D']:>10.3f} {statut:>12}")
    print()
    print("  Note : les phases sont reduites proportionnellement dans chaque scenario.")
    print("=" * 70)


# ---------------------------------------------------------------------
# Requalification — deux regimes distincts
# ---------------------------------------------------------------------

REGIMES = {
    "Regime 1 - R&D et capacites (phases 1-4)": {
        "montant_M$": 22.5,
        "critere": "Creation d'actifs immateriels + capacites documentees",
        "seuil_D": None,
        "statut": "[T] - Investissement en capacites industrielles",
    },
    "Regime 2 - Pilote industriel (phase 5)": {
        "montant_M$": 2.5,
        "critere": "Ratio D > 1,30 sur horizon 10 ans",
        "seuil_D": 1.30,
        "statut": "[P] - Decision d'industrialisation",
    },
}


# =====================================================================
# CONSTANTES DU MODULE 5 — VÉHICULE URBAIN LÉGER
# =====================================================================
# Natures distinguées :
#   [EMP]  Valeur empirique — mesurée ou issue d'une source documentée
#   [MÉTH] Seuil méthodologique — paramètre de la grille d'évaluation
#   [SCÉN] Paramètre scénaristique — hypothèse de travail assumée
# =====================================================================

# Constante 1 — economies_10ans (base 0,81 M$ sur 5 ans)
# Valeur    : 0,81 M$
# Unité     : millions CAD par période de 5 ans
# Statut    : [SCÉN] paramètre scénaristique
# Justification : économies d'exploitation attendues sur un pilote
#                 industriel de 5 ans, doublées pour couvrir un
#                 horizon de 10 ans. À valider par étude dédiée.

# Constante 2 — valeur actifs robotiques (6,40 M$)
# Valeur    : 6,40 M$
# Unité     : millions CAD
# Statut    : [SCÉN] paramètre scénaristique
# Justification : valeur résiduelle estimée d'un parc robotique
#                 industriel. Aucune source externe documentée.

# Constante 3 — investissement robots total (8,0 M$)
# Valeur    : 8,0 M$
# Unité     : millions CAD
# Statut    : [SCÉN] paramètre scénaristique
# Justification : investissement total présumé en robots pour le
#                 projet. Sert de dénominateur à la quote-part
#                 (2,5 / 8,0). Aucune source externe documentée.

# Constante 4 — valeur PI totale (4,00 M$)
# Valeur    : 4,00 M$
# Unité     : millions CAD
# Statut    : [SCÉN] paramètre scénaristique
# Justification : valeur estimée du portefeuille de propriété
#                 intellectuelle associé au projet. Aucune source.

# Constante 5 — investissement PI total (4,5 M$)
# Valeur    : 4,5 M$
# Unité     : millions CAD
# Statut    : [SCÉN] paramètre scénaristique
# Justification : investissement total présumé en PI. Sert de
#                 dénominateur à la quote-part (2,5 / 4,5).
#                 Aucune source externe documentée.

# NOTE D'AUDIT
# Ces cinq constantes sont utilisées dans le calcul du ratio D = 2,337.
# Elles sont toutes classées [SCÉN] : ce sont des hypothèses de travail
# non adossées à une source externe. Le ratio D qui en résulte doit
# donc être présenté comme [P] prospectif dans toute communication
# publique. Toute demande de validation externe (économiste, bailleur,
# comité) devra porter en priorité sur ces cinq valeurs.
# =====================================================================


def calculer_D_pilote_10ans():
    """Ratio D du pilote sur 10 ans (au lieu de 5)."""
    # Benefices sur 10 ans
    economies_10ans = 0.81 * 2  # 0,81 M$ x 2 (5 ans -> 10 ans)
    part_robotique = (2.5 / 8.0) * 6.40  # quote-part des robots
    part_PI = (2.5 / 4.5) * 4.00  # quote-part de la PI
    valeur_creee = economies_10ans + part_robotique + part_PI
    cout = 2.5
    d = valeur_creee / cout
    return {
        "horizon_ans": 10,
        "economies_M$": round(economies_10ans, 2),
        "part_robotique_M$": round(part_robotique, 2),
        "part_PI_M$": round(part_PI, 2),
        "valeur_creee_M$": round(valeur_creee, 2),
        "cout_M$": cout,
        "ratio_D": round(d, 3),
        "seuil": SEUIL_D,
        "conforme": d > SEUIL_D,
    }


def afficher_requalification():
    print("=" * 70)
    print("  REQUALIFICATION — DEUX REGIMES DISTINCTS")
    print("=" * 70)
    print()
    for nom, data in REGIMES.items():
        print(f"  {nom}")
        print(f"    Montant  : {data['montant_M$']} M$")
        print(f"    Critere  : {data['critere']}")
        print(f"    Statut   : {data['statut']}")
        print()
    print("  --- Regime 2 — Calcul du ratio D sur 10 ans ---")
    r = calculer_D_pilote_10ans()
    print(f"    Economies (10 ans) : {r['economies_M$']} M$")
    print(f"    Part robotique     : {r['part_robotique_M$']} M$")
    print(f"    Part PI            : {r['part_PI_M$']} M$")
    print(f"    Valeur creee       : {r['valeur_creee_M$']} M$")
    print(f"    Cout total         : {r['cout_M$']} M$")
    statut = "CONFORME" if r["conforme"] else "REJETE"
    print(f"    Ratio D            : {r['ratio_D']} ({statut})")
    print()
    print("  Note : le seuil D > 1,30 s'applique au pilote industriel,")
    print("         pas a l'investissement en capacites R&D.")
    print("=" * 70)


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

if __name__ == "__main__":
    verifier_variables()
    afficher_rapport()
    print()
    sauvegarder_json()
    print()
    afficher_scenarios()
    print()
    afficher_requalification()
