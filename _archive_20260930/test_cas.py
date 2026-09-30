"""
Jeu de tests de calibration.

Lance le moteur sur 5 textes contrastes pour verifier que les verdicts
sont coherents. Utile pour detecter les faux positifs et faux negatifs.
"""
from engines import ExtractionEngine
from rules import (
    enforce_traceability,
    evaluate_electoral_risk,
    evaluate_gold_card_legal_risks,
)


CAS = {
    "CAS_1_gold_card_evident": """
    Une Gold Card prioritaire aux riches Americains pour acceder a nos
    blocs operatoires en moins de 48 heures. Signez la petition avant
    le vote du 15 novembre.
    """,

    "CAS_2_texte_neutre": """
    Le gouvernement a publie un rapport sur les delais d'attente
    hospitaliers en 2024. Le document recommande une revision des
    processus administratifs.
    """,

    "CAS_3_chiffres_sources": """
    Selon le rapport annuel du MSSS publie en 2024, le taux de
    diplomation secondaire a atteint 82 %. Selon Statistique Canada,
    la population active a progresse de 1,3 %.
    """,

    "CAS_4_chiffres_non_sources": """
    Le programme coutera 500 millions $ sur 5 ans. Il beneficiera a
    100 000 personnes. Le retour sur investissement sera de 250 %.
    """,

    "CAS_5_appel_action_seul": """
    Signez notre petition officielle avant le vote du 15 novembre.
    Mobilisez-vous pour la sante universelle.
    """,
}


def main():
    engine = ExtractionEngine()

    print("=" * 72)
    print("CALIBRATION - 5 CAS")
    print("=" * 72)

    for nom, texte in CAS.items():
        raw = engine.extract(texte)
        validated = enforce_traceability(raw)
        electoral = evaluate_electoral_risk(validated)
        gold = evaluate_gold_card_legal_risks(validated)

        non_sources = sum(
            1 for c in validated.traceability_audit
            if c.claim_type != "normative_statement" and not c.is_sourced
        )
        cialdini_actifs = [
            t.principle for t in validated.cialdini_audit
            if t.presence != "absent"
        ]

        print(f"\n--- {nom} ---")
        print(f"  Score             : {gold['compliance_score']}/100")
        print(f"  Verdict           : {gold['verdict']}")
        print(f"  Affirmations non sourcees : {non_sources}")
        print(f"  Cialdini actifs   : {', '.join(cialdini_actifs) or 'aucun'}")
        print(f"  Imprimatur requis : {electoral['requires_imprimatur']}")

    print("\n" + "=" * 72)
    print("Fin de calibration.")
    print("=" * 72)


if __name__ == "__main__":
    main()
