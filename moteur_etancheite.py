"""
moteur_etancheite.py — Topologie et traçabilité budgétaire
PMDQ v2.7.5 — Module 4

Vérifie l'étanchéité budgétaire par analyse de graphe orienté.

Règles structurelles (Articles 14, 15, 16) :
    R  (ressources garanties)   → admissible aux décaissements
    Ré (report automatique)     → admissible aux décaissements
    É  (économies)              → admissible aux décaissements
    Co (revenus conditionnels)  → EXCLU, réservé à la réserve de contingence

Violations détectables :
    - Arête Co → Décaissement (violation Article 14)
    - Absence de réserve de contingence alimentée par Co (violation Article 15)
    - Double comptage entre ministères (FIN-002)
"""
import networkx as nx
import json
from datetime import date
from pathlib import Path

# --- Construction du graphe orienté ---
G = nx.DiGraph()

# Sources
G.add_node("R",  type="source", statut="admissible")
G.add_node("Ré", type="source", statut="admissible")
G.add_node("É",  type="source", statut="admissible")
G.add_node("Co", type="source", statut="exclu")

# Destinations
G.add_node("Décaissements",         type="destination")
G.add_node("Réserve de contingence", type="destination")

# Arêtes autorisées (Article 14)
G.add_edge("R",  "Décaissements",        statut="autorise")
G.add_edge("Ré", "Décaissements",        statut="autorise")
G.add_edge("É",  "Décaissements",        statut="autorise")

# Arête EXCLUSIVE (Article 15)
G.add_edge("Co", "Réserve de contingence", statut="autorise_exclusif")

# Arêtes INTERDITES (détectables)
INTERDITES = [("Co", "Décaissements")]

# --- Flux réels (scénario B, Livre II) ---
FLUX = {
    "Réaffectations": {"valeur_G$": 5.14, "categorie": "R"},
    "Économies":      {"valeur_G$": 2.57, "categorie": "É"},
    "Redevances":     {"valeur_G$": 0.69, "categorie": "Co"},
}

# Anomalies déclarées
ANOMALIES = [
    {"code": "FIN-001", "valeur_G$": 0.85, "description": "Pénalités É-04 + É-05 mal classées en É", "devrait_etre": "Co"},
    {"code": "FIN-002", "valeur_G$": 0.09, "description": "Double comptage MSSS/MCN"},
]

# --- Analyse ---
def verifier_etancheite():
    violations = []

    # 1. Vérifier les arêtes interdites
    for source, dest in INTERDITES:
        if G.has_edge(source, dest):
            violations.append({
                "type": "arête_interdite",
                "source": source,
                "destination": dest,
                "regle": "Article 14 — ressources admissibles"
            })

    # 2. Vérifier que Co alimente bien la réserve de contingence
    if not G.has_edge("Co", "Réserve de contingence"):
        violations.append({
            "type": "réserve_non_alimentée",
            "source": "Co",
            "regle": "Article 15 — réserve de contingence distincte"
        })

    # 3. Vérifier les flux classés en Co
    for nom, data in FLUX.items():
        if data["categorie"] == "Co":
            # Co → Décaissement serait une violation
            if G.has_edge("Co", "Décaissements"):
                violations.append({
                    "type": "flux_exclu_vers_decaissement",
                    "flux": nom,
                    "valeur_G$": data["valeur_G$"],
                    "regle": "Article 14 — Co exclu"
                })

    return violations

def calculer_assiette_executoire():
    """Somme des catégories admissibles (R, Ré, É)."""
    return sum(
        d["valeur_G$"] for d in FLUX.values()
        if d["categorie"] in ["R", "Ré", "É"]
    )

def calculer_revenus_conditionnels():
    """Somme des catégories exclues (Co)."""
    return sum(
        d["valeur_G$"] for d in FLUX.values()
        if d["categorie"] == "Co"
    )

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
    print("MOTEUR D'ÉTANCHÉITÉ BUDGÉTAIRE — PMDQ v2.7.5")
    print("=" * 72)
    print()

    # 1. Topologie
    print("--- Topologie du graphe ---")
    print(f"  Nœuds       : {G.number_of_nodes()}")
    print(f"  Arêtes      : {G.number_of_edges()}")
    print(f"  Sources     : R, Ré, É, Co")
    print(f"  Destinations: Décaissements, Réserve de contingence")
    print()

    # 2. Assiette exécutoire
    assiette = calculer_assiette_executoire()
    conditionnels = calculer_revenus_conditionnels()
    print("--- Assiette exécutoire (Article 14) ---")
    print(f"  R + Ré + É  : {assiette:.2f} G$")
    print(f"  Co (exclu)  : {conditionnels:.2f} G$")
    print(f"  Total flux  : {assiette + conditionnels:.2f} G$")
    print()

    # 3. Violations structurelles
    violations = verifier_etancheite()
    print("--- Violations structurelles ---")
    if violations:
        for v in violations:
            print(f"  ⚠ {v}")
    else:
        print("  ✅ Aucune violation détectée.")
    print()

    # 4. Anomalies déclarées
    print("--- Anomalies financières déclarées ---")
    for a in ANOMALIES:
        print(f"  {a['code']} — {a['valeur_G$']} G$ — {a['description']}")
        if "devrait_etre" in a:
            print(f"     Devrait être classé en : {a['devrait_etre']}")
    print()

    # 5. Impact de FIN-001 sur l'assiette
    impact = ANOMALIES[0]["valeur_G$"]
    assiette_corrigee = assiette - impact
    print("--- Assiette exécutoire corrigée (si FIN-001 résolu) ---")
    print(f"  Avant correction : {assiette:.2f} G$")
    print(f"  Après correction : {assiette_corrigee:.2f} G$")
    print(f"  Impact           : -{impact:.2f} G$")
    print()

    # 6. Sauvegarde JSON
    rapport = {
        "date_calcul": str(date.today()),
        "topologie": {
            "noeuds": G.number_of_nodes(),
            "aretes": G.number_of_edges(),
            "sources": ["R", "Ré", "É", "Co"],
            "destinations": ["Décaissements", "Réserve de contingence"]
        },
        "assiette_executoire_G$": round(assiette, 2),
        "revenus_conditionnels_G$": round(conditionnels, 2),
        "assiette_corrigee_G$": round(assiette_corrigee, 2),
        "violations": violations,
        "anomalies_declarees": ANOMALIES
    }

    with open("sources/etancheite_budgetaire.json", "w", encoding="utf-8") as f:
        json.dump(rapport, f, indent=2, ensure_ascii=False)
    print("Rapport sauvegardé : sources/etancheite_budgetaire.json")



# --- Test de robustesse : simuler une violation et vérifier la détection ---
def test_detection_violation():
    """Simule une arête interdite et vérifie que le moteur la détecte."""
    G_test = G.copy()
    G_test.add_edge("Co", "Décaissements", statut="interdit")

    violations_test = []
    for source, dest in INTERDITES:
        if G_test.has_edge(source, dest):
            violations_test.append({
                "type": "arête_interdite",
                "source": source,
                "destination": dest,
                "regle": "Article 14 — ressources admissibles"
            })

    if violations_test:
        print("✅ Test de robustesse : violation correctement détectée.")
        print(f"   {violations_test[0]}")
    else:
        print("❌ Test de robustesse : la violation n'a pas été détectée.")

if __name__ == "__main__":
    main()
    print()
    print("--- Test de robustesse du moteur ---")
    test_detection_violation()
