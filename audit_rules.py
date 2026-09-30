from audit_schemas import MessageExtraction

SOURCES_VALIDES = (
    "ISQ", "StatCan", "Statistique Canada",
    "Revenu Québec", "Finances Québec", "Banque du Canada",
    "Budget", "MELS", "MSSS", "INSPQ", "DGEQ", "ASFC",
    "http://", "https://", ".pdf", ".xlsx", ".csv", ".json",
)

def _source_est_valide(ref: str) -> bool:
    if not ref:
        return False
    return any(s.lower() in ref.lower() for s in SOURCES_VALIDES)

def enforce_traceability(extraction: MessageExtraction) -> MessageExtraction:
    for claim in extraction.traceability_audit:
        if claim.claim_type in ["empirical_fact", "economic_projection"]:
            if not claim.is_sourced:
                claim.compliance_status = "BLOCAGE : Affirmation non sourcée."
            elif not claim.source_reference:
                claim.compliance_status = "RÉVISION : Référence manquante."
            elif not _source_est_valide(claim.source_reference):
                claim.compliance_status = "BLOCAGE : Source interne non opposable."
            else:
                claim.compliance_status = "CONFORME : Donnée traçable."
        else:
            claim.compliance_status = "INFO : Jugement normatif."
    return extraction

def evaluate_electoral_risk(extraction: MessageExtraction) -> dict:
    risk = {"requires_imprimatur": False, "warnings": [], "status": "OK"}

    if extraction.has_call_to_action:
        risk["requires_imprimatur"] = True
        risk["warnings"].append("Appel à l'action : autorisation officielle requise.")
        risk["status"] = "A_REVISER"

    if extraction.mentions_third_party_spending:
        risk["warnings"].append("Risque de dépense de tiers : surveillance requise.")
        risk["status"] = "BLOQUE"

    if any(
        c.compliance_status and c.compliance_status.startswith("BLOCAGE")
        for c in extraction.traceability_audit
    ):
        risk["status"] = "BLOQUE"

    return risk
