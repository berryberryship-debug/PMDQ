"""
Orchestrateur d'audit.

Flux : texte → extraction LLM → règles déterministes → rapport.
"""
from engines import ExtractionEngine
from rules import (
    enforce_traceability,
    evaluate_electoral_risk,
    evaluate_gold_card_legal_risks,
)


def afficher_rapport(validated, legal, gold):
    sep = "=" * 52

    print(f"\n{sep}")
    print("        RAPPORT D'AUDIT COMPLET")
    print(sep)

    print(f"\n[ PUBLIC CIBLE ]\n{validated.target_audience}")

    print("\n[ TRAÇABILITÉ FACTUELLE ]")
    for c in validated.traceability_audit:
        print(f"\n- Énoncé : \"{c.statement}\"")
        print(f"  Type    : {c.claim_type}")
        print(f"  Sourcé  : {c.is_sourced} (Réf : {c.source_reference})")
        print(f"  Statut  : {c.compliance_status}")

    print("\n[ LEVIERS DE MOBILISATION (CIALDINI) ]")
    for t in validated.cialdini_audit:
        if t.presence != "absent":
            print(f"- {t.principle} [{t.presence.upper()}] : {t.application}")
            if t.evidence:
                print(f"  Extrait : \"{' ; '.join(t.evidence)}\"")

    print("\n[ CONFORMITÉ LÉGALE (DGEQ / ÉLECTIONS) ]")
    print(f"- Requiert Imprimatur : {legal['requires_imprimatur']}")
    if legal["warnings"]:
        for w in legal["warnings"]:
            print(f"  ! {w}")
    else:
        print("  Aucune alerte légale identifiée.")

    print(f"\n{sep}")
    print("        BARRIÈRES LÉGALES GOLD CARD")
    print(sep)
    print(f"- Score de conformité : {gold['compliance_score']}/100")
    print(f"- Verdict : {gold['verdict']}")

    for bloc, libellé in [
        ("federal_barriers", "FÉDÉRAL"),
        ("provincial_barriers_qc", "QUÉBEC"),
        ("provincial_barriers_on", "ONTARIO"),
        ("electoral_risks", "ÉLECTORAL"),
    ]:
        if gold[bloc]:
            print(f"\n  ⚠️  {libellé} :")
            for item in gold[bloc]:
                print(f"    • {item}")

    print(f"\n{sep}")
    print("        CHIFFRAGE DU MODÈLE ÉCONOMIQUE")
    print(sep)
    fin = gold["financial_feasibility"]
    hyp = fin["hypothese"]

    print("\n  HYPOTHÈSES :")
    print(f"    • Prix Gold Card : {hyp['prix_gold_card']:,} $/an")
    print(f"    • Franchise par chirurgie : "
          f"{hyp['franchise_par_chirurgie']:,} $")
    print(f"    • Coût moyen d'une chirurgie : "
          f"{hyp['cout_moyen_chirurgie']:,} $")
    print(f"    • Volume de chirurgies / patient : "
          f"{hyp['volume_chirurgies_par_patient']} / an")
    print(f"    • Patients ciblés (année 3) : {hyp['patients_cible_an3']:,}")

    print("\n  PROJECTIONS (ANNÉE 3) :")
    print(f"    • Revenus annuels : {fin['revenus_annuels_millions']} M$")
    print(f"    • Coûts directs : {fin['couts_directs_millions']} M$")
    print(f"    • Marge brute : {fin['marge_brute_millions']} M$")
    print(f"    • Marge brute / patient : "
          f"{fin['marge_brute_par_patient']:,} $")
    print(f"    • Faisabilité : {fin['faisabilite']}")

    print(f"\n{sep}")
    print("        SYNTHÈSE STRATÉGIQUE")
    print(sep)

    verdict = gold["verdict"]
    faisable = fin["faisabilite"]

    if verdict == "RISQUE ÉLEVÉ" and faisable == "OUI":
        print("\n  ⚠️  VIABLE ÉCONOMIQUEMENT / LÉGALITÉ DOUTEUSE")
        print("  → Recommandation : abandonner ou reformuler en profondeur")
    elif verdict == "RISQUE ÉLEVÉ" and faisable == "NON":
        print("\n  ❌  NON-VIABLE (économique + légal)")
        print("  → Recommandation : abandonner immédiatement")
    elif verdict == "RISQUE MODÉRÉ" and faisable == "OUI":
        print("\n  ⚠️  VIABLE MAIS RISQUES LÉGAUX SIGNIFICATIFS")
        print("  → Recommandation : consulter un avocat avant de poursuivre")
    else:
        print("\n  ✅  PROMETTEUR (sous réserve de validation juridique)")
        print("  → Recommandation : poursuivre avec audit approfondi")

    print(sep)


def main():
    sample_text = """
    Une nouvelle politique secrète accorderait une « Gold Card » prioritaire
    aux riches Américains pour accéder à nos blocs opératoires au Québec et
    en Ontario en moins de 48 heures. Selon un rapport récent du Conseil de
    la Santé publié en 2024, plus de 35 000 patients d'ici voient leurs
    chirurgies repoussées à cause de ce programme privé de 120 millions $.
    Nos familles méritent un accès universel et équitable, pas un système à
    deux vitesses.
    Mobilisez-vous et signez notre pétition officielle avant le vote du
    15 novembre.
    """

    print("1. Extraction sémantique (LLM)...")
    engine = ExtractionEngine()
    raw = engine.extract(sample_text)

    print("2. Application des règles déterministes (Python)...")
    validated = enforce_traceability(raw)
    legal = evaluate_electoral_risk(validated)
    gold = evaluate_gold_card_legal_risks(validated)

    afficher_rapport(validated, legal, gold)


if __name__ == "__main__":
    main()
