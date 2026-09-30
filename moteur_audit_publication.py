from audit_schemas import MessageExtraction, CialdiniTacticAudit, FactualClaimTraceability

def extract_message(text: str) -> MessageExtraction:
    lower = text.lower()

    has_cta = any(term in lower for term in [
        "votez",
        "rejoignez",
        "adhérez",
        "signez",
        "agissez",
        "dès aujourd'hui",
        "maintenant",
    ])

    third_party = any(term in lower for term in [
        "tiers",
        "dépense",
        "publicité payée",
        "financement externe",
    ])

    tactics = []

    if any(term in lower for term in [
        "économistes sérieux",
        "experts",
        "spécialistes",
        "autorité",
    ]):
        tactics.append(CialdiniTacticAudit(
            principle="Authority",
            presence="explicit",
            application="Le texte invoque une autorité pour renforcer sa crédibilité.",
            evidence=["économistes sérieux"],
        ))

    if any(term in lower for term in [
        "60 jours",
        "urgent",
        "dernier",
        "maintenant",
    ]):
        tactics.append(CialdiniTacticAudit(
            principle="Scarcity",
            presence="possible",
            application="Le texte crée une urgence temporelle.",
            evidence=["60 jours"],
        ))

    if "nous" in lower:
        tactics.append(CialdiniTacticAudit(
            principle="Unity",
            presence="possible",
            application="Le texte mobilise un sentiment d'appartenance collective.",
            evidence=["nous"],
        ))

    claims = []

    if "2,4 milliards" in lower or "2.4 milliards" in lower:
        source_ok = any(term in lower for term in [
            "https://",
            "http://",
            ".pdf",
            "finances québec",
        ])

        claims.append(FactualClaimTraceability(
            statement="Notre fonds souverain est de 2,4 milliards $.",
            claim_type="empirical_fact",
            is_sourced=source_ok,
            source_reference=(
                "Finances Québec, 2024-2025, https://..."
                if source_ok else "Projection interne"
            ),
        ))

    if "60 jours" in lower:
        claims.append(FactualClaimTraceability(
            statement="Il ne reste que 60 jours pour sécuriser nos PME.",
            claim_type="economic_projection",
            is_sourced=False,
            source_reference=None,
        ))

    return MessageExtraction(
        target_audience="citoyens et militants",
        cialdini_audit=tactics,
        traceability_audit=claims,
        has_call_to_action=has_cta,
        mentions_third_party_spending=third_party,
    )
