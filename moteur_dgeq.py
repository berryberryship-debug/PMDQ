"""
moteur_dgeq.py - Moteur de conformite DGEQ (Module 8)
PMDQ v2.7.5

Valide les contributions politiques selon la Loi sur les elections
et les referendums du Quebec (DGEQ).

Regles principales :
    - Plafond : 100 $ par an par electeur
    - +100 $ supplementaire l'annee d'une election
    - Contributions > 50 $ : cheque ou carte (pas comptant)
    - Contributions > 100 $ : transmission obligatoire au DGEQ
    - Aucune personne morale ne peut contribuer

Usage :
    python3 moteur_dgeq.py --demo
    python3 moteur_dgeq.py --fichier contributions.csv
    python3 moteur_dgeq.py --interactif
"""
import json
import csv
from datetime import date
from pathlib import Path

# ---------------------------------------------------------------------
# Regles DGEQ (parametres officiels)
# ---------------------------------------------------------------------

PLAFOND_ANNUEL = 100.00       # $ par electeur par an
PLAFOND_ELECTION = 200.00     # $ par electeur l'annee d'une election
SEUIL_CHEQUE = 50.00          # $ au-dela duquel le comptant est interdit
SEUIL_DGEQ = 100.00           # $ au-dela duquel la transmission est obligatoire

MODES_PAIEMENT = ["cheque", "carte", "comptant", "transfert"]


# ---------------------------------------------------------------------
# Fonctions de validation
# ---------------------------------------------------------------------

def valider_contribution(contribution, annee_electorale=False):
    """
    Valide une contribution individuelle.

    contribution : dict avec
        - donateur (str)
        - montant (float)
        - mode (str) : cheque, carte, comptant, transfert
        - est_personne_morale (bool)
        - cumul_annuel (float) : total deja verse cette annee
    """
    erreurs = []
    avertissements = []

    nom = contribution.get("donateur", "inconnu")
    montant = float(contribution.get("montant", 0))
    mode = contribution.get("mode", "").lower()
    est_pm = contribution.get("est_personne_morale", False)
    cumul = float(contribution.get("cumul_annuel", 0))

    # Regle 1 : aucune personne morale
    if est_pm:
        erreurs.append("Personne morale interdite (DGEQ)")

    # Regle 2 : mode de paiement
    if mode not in MODES_PAIEMENT:
        erreurs.append(f"Mode de paiement inconnu : {mode}")
    if montant > SEUIL_CHEQUE and mode == "comptant":
        erreurs.append(
            f"Comptant interdit au-dela de {SEUIL_CHEQUE:.0f} $ (DGEQ)"
        )

    # Regle 3 : plafond annuel
    plafond = PLAFOND_ELECTION if annee_electorale else PLAFOND_ANNUEL
    total_apres = cumul + montant
    if total_apres > plafond:
        depassement = total_apres - plafond
        erreurs.append(
            f"Plafond annuel depasse : {total_apres:.2f} $ > {plafond:.2f} $ "
            f"(depassement de {depassement:.2f} $)"
        )

    # Regle 4 : transmission obligatoire
    if montant > SEUIL_DGEQ:
        avertissements.append(
            f"Transmission obligatoire au DGEQ ({montant:.2f} $ > {SEUIL_DGEQ:.0f} $)"
        )

    return {
        "donateur": nom,
        "montant": round(montant, 2),
        "mode": mode,
        "annee_electorale": annee_electorale,
        "plafond_applicable": plafond,
        "cumul_annuel": round(cumul, 2),
        "total_apres": round(total_apres, 2),
        "valide": len(erreurs) == 0,
        "erreurs": erreurs,
        "avertissements": avertissements,
    }


# ---------------------------------------------------------------------
# Demonstration
# ---------------------------------------------------------------------

def demo():
    """Execute 4 cas de test pour valider le moteur."""
    cas = [
        {
            "donateur": "Alice Tremblay",
            "montant": 50,
            "mode": "cheque",
            "est_personne_morale": False,
            "cumul_annuel": 0,
        },
        {
            "donateur": "Bob Gagnon",
            "montant": 150,
            "mode": "comptant",
            "est_personne_morale": False,
            "cumul_annuel": 0,
        },
        {
            "donateur": "Corporation XYZ",
            "montant": 500,
            "mode": "cheque",
            "est_personne_morale": True,
            "cumul_annuel": 0,
        },
        {
            "donateur": "Claire Roy",
            "montant": 80,
            "mode": "carte",
            "est_personne_morale": False,
            "cumul_annuel": 60,
        },
    ]

    print()
    print("=" * 65)
    print("  MOTEUR DE CONFORMITE DGEQ — PMDQ v2.7.5")
    print("=" * 65)
    print()

    for c in cas:
        r = valider_contribution(c, annee_electorale=False)
        statut = "VALIDE" if r["valide"] else "REJETE"
        print(f"  {r['donateur']:20s} | {r['montant']:>7.2f} $ | {r['mode']:10s} | {statut}")
        for e in r["erreurs"]:
            print(f"      X {e}")
        for a in r["avertissements"]:
            print(f"      ! {a}")
        print()

    print("=" * 65)


# ---------------------------------------------------------------------
# Chargement depuis CSV
# ---------------------------------------------------------------------

def charger_csv(chemin):
    """Charge un fichier CSV de contributions et les valide."""
    contributions = []
    with open(chemin, "r", encoding="utf-8") as f:
        lecteur = csv.DictReader(f)
        for ligne in lecteur:
            contributions.append({
                "donateur": ligne.get("nom_donateur", ""),
                "montant": float(ligne.get("montant", 0)),
                "mode": ligne.get("mode", ""),
                "est_personne_morale": ligne.get("est_personne_morale", "non").lower() == "oui",
                "cumul_annuel": float(ligne.get("cumul_annuel", 0)),
            })
    return contributions


# ---------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------

def main():
    import argparse
    parser = argparse.ArgumentParser(
        description="Moteur de conformite DGEQ — PMDQ v2.7.5"
    )
    parser.add_argument("--demo", action="store_true", help="Lancer la demo")
    parser.add_argument("--fichier", type=str, default=None,
                        help="Fichier CSV de contributions")
    parser.add_argument("--interactif", action="store_true",
                        help="Mode interactif")
    args = parser.parse_args()

    if args.fichier:
        contributions = charger_csv(args.fichier)
        for c in contributions:
            r = valider_contribution(c)
            statut = "VALIDE" if r["valide"] else "REJETE"
            print(f"{r['donateur']:20s} | {r['montant']:>7.2f} $ | {statut}")
            for e in r["erreurs"]:
                print(f"    X {e}")
    elif args.interactif:
        print("Mode interactif (a completer)")
    else:
        demo()


if __name__ == "__main__":
    main()
