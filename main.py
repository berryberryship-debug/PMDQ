from moteur_audit_publication import extract_message
from audit_rules import enforce_traceability, evaluate_electoral_risk

try:
    from audit_registry import append_record
except ImportError:
    def append_record(text, report):
        pass

TEXTE_TEST = (
    "Tous les économistes sérieux s'accordent : il ne reste que 60 jours "
    "pour sécuriser nos PME. Notre fonds souverain est de 2,4 milliards $. "
    "Votez maintenant, rejoignez-nous."
)


def main():
    print("=== RAPPORT D'AUDIT DE PUBLICATION ===")
    print("Texte analysé :")
    print(TEXTE_TEST)
    print()

    extraction = extract_message(TEXTE_TEST)
    extraction = enforce_traceability(extraction)
    risques = evaluate_electoral_risk(extraction)

    print("[CIALDINI]")
    for t in extraction.cialdini_audit:
        if t.presence != "absent":
            print(f"  - {t.principle} ({t.presence}) : {t.application}")

    print()
    print("[TRACABILITE]")
    for c in extraction.traceability_audit:
        print(f"  - {c.claim_type} | {c.compliance_status}")
        print(f"    {c.statement}")

    print()
    print(f"[APPEL A L'ACTION] {extraction.has_call_to_action}")
    print(f"[DEPENSE DE TIERS] {extraction.mentions_third_party_spending}")

    print()
    print(f"[STATUT GLOBAL] {risques['status']}")
    for w in risques["warnings"]:
        print(f"  - {w}")

    report_json = extraction.model_dump_json(indent=2, ensure_ascii=False)

    print()
    print("[JSON COMPLET]")
    print(report_json)

    append_record(TEXTE_TEST, report_json)


if __name__ == "__main__":
    main()
