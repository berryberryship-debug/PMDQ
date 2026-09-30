"""
Tests unitaires du moteur de règles. Aucun appel LLM.
Exécution : pytest test_main.py -v
"""
from schemas import (
    MessageExtraction,
    CialdiniTacticAudit,
    FactualClaimTraceability,
)
from rules import (
    enforce_traceability,
    evaluate_electoral_risk,
    evaluate_gold_card_legal_risks,
)


def _fixture_vide():
    return MessageExtraction(
        target_audience="Test",
        cialdini_audit=[],
        traceability_audit=[],
        has_call_to_action=False,
        mentions_third_party_spending=False,
    )


def _fixture_normale():
    return MessageExtraction(
        target_audience="Électeurs",
        cialdini_audit=[
            CialdiniTacticAudit(
                principle="Unity",
                presence="explicit",
                application="Appel à la solidarité",
                evidence=["nos familles"],
            )
        ],
        traceability_audit=[
            FactualClaimTraceability(
                statement="35 000 patients",
                claim_type="empirical_fact",
                is_sourced=True,
                source_reference="Conseil de la Santé 2024",
            ),
            FactualClaimTraceability(
                statement="120 millions $",
                claim_type="economic_projection",
                is_sourced=False,
            ),
        ],
        has_call_to_action=True,
        mentions_third_party_spending=False,
    )


def test_traceability_bloque_non_source():
    e = enforce_traceability(_fixture_normale())
    statuts = [c.compliance_status for c in e.traceability_audit]
    assert any("BLOCAGE" in s for s in statuts)
    assert any("CONFORME" in s for s in statuts)


def test_traceability_ignore_normatif():
    e = MessageExtraction(
        target_audience="X",
        cialdini_audit=[],
        traceability_audit=[
            FactualClaimTraceability(
                statement="Il faut plus de justice",
                claim_type="normative_statement",
                is_sourced=False,
            )
        ],
        has_call_to_action=False,
        mentions_third_party_spending=False,
    )
    e = enforce_traceability(e)
    assert "INFO" in e.traceability_audit[0].compliance_status


def test_risque_electoral_imprimatur():
    r = evaluate_electoral_risk(_fixture_normale())
    assert r["requires_imprimatur"] is True
    assert len(r["warnings"]) >= 1


def test_gold_card_penalise_acces_prioritaire():
    g = evaluate_gold_card_legal_risks(_fixture_normale())
    assert g["compliance_score"] < 100
    assert g["verdict"] in ("RISQUE MODÉRÉ", "RISQUE ÉLEVÉ")


def test_chiffrage_coherent():
    g = evaluate_gold_card_legal_risks(_fixture_normale())
    fin = g["financial_feasibility"]
    # Vérification arithmétique
    assert fin["revenus_annuels_millions"] == 186.0
    assert fin["couts_directs_millions"] == 90.0
    assert fin["marge_brute_millions"] == 96.0


def test_score_plancher_zero():
    g = evaluate_gold_card_legal_risks(_fixture_normale())
    assert g["compliance_score"] >= 0
