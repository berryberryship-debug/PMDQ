#!/usr/bin/env python3
"""PMDQ — audit de robustesse du dépôt publié."""
import sys
from urllib.request import urlopen

BASE_URL = "https://berryberryship-debug.github.io/PMDQ"

PAGES_PUBLIQUES = [
    "index.html", "01_livre_I_architecture.html", "02_livre_II_finances.html",
    "03_livre_III_portefeuille_17_projets.html", "04_livre_IV_simulateur_macro.html",
    "05_livre_V_dette_domar.html", "06_livre_VI_audit_invariants.html",
    "07_livre_VII_moteur_python.html", "08_livre_VIII_exports_et_annexes.html",
    "09_livre_IX_rapport_final.html", "cdli.html", "livre_X_justice.html",
    "fiche-D1-D5.html", "fiche-D3.html", "fiche-D1.html", "fiche-D2.html", "fiche-D5.html", "registre-propositions.html", "annexe_fiscal_passif.html", "corridor-narp.html", "annexe-ocap.html", "annexe-ocap-ia.html", "coalition-scientifique-technologique.html", "annexe-agentivite-trajectoire.html", "gold-card.html", "references.html", "changelog.html", "demande-clarification-domar.html", "reforme-education-impact.html", "moteurs.html", "marge-fiscale-tvq.html", "taxe-luxe.html",  "demande-clarification-domar.html", "annexe_fiscal_passif.html", "lettre.html", "note-synthese.html", "style.css",
]

PAGES_SILENCIEUSES = [
    "annexe_livres_I_a_IV.html",
    "annexe_axiomes.html",
    "annexe_axiomes.html",
]

def check_url(path):
    try:
        r = urlopen(f"{BASE_URL}/{path}", timeout=10)
        return r.status == 200
    except Exception:
        return False

def main():
    ok, ko = [], []
    for p in PAGES_PUBLIQUES + PAGES_SILENCIEUSES:
        (ok if check_url(p) else ko).append(p)

    print(f"=== PMDQ — audit de robustesse ===")
    print(f"Total testé   : {len(PAGES_PUBLIQUES) + len(PAGES_SILENCIEUSES)}")
    print(f"Publiées OK   : {len(ok)}")
    if ko:
        print(f"EN ERREUR     : {ko}")
        sys.exit(1)
    print("Dépôt intégralement cohérent.")

if __name__ == "__main__":
    main()
