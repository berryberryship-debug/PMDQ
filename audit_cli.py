#!/usr/bin/env python3
"""CLI d'audit de publication PMDQ."""
import argparse
import json
from pathlib import Path

from moteur_audit_publication import extract_message
from audit_rules import enforce_traceability, evaluate_electoral_risk
from audit_registry import append_record


def afficher_rapport(extraction, risques):
    print("=== RAPPORT D'AUDIT DE PUBLICATION ===\n")

    print("[CIALDINI]")
    tactics_actifs = [t for t in extraction.cialdini_audit if t.presence != "absent"]
    if not tactics_actifs:
        print("  Aucune tactique détectée.")
    for t in tactics_actifs:
        print(f"  - {t.principle} ({t.presence}) : {t.application}")

    print("\n[TRACABILITE]")
    if not extraction.traceability_audit:
        print("  Aucune affirmation détectée.")
    for c in extraction.traceability_audit:
        statut = c.compliance_status or "NON EVALUE"
        print(f"  - [{statut}] {c.claim_type}")
        print(f"    « {c.statement} »")

    print(f"\n[APPEL A L'ACTION] {extraction.has_call_to_action}")
    print(f"[DEPENSE DE TIERS] {extraction.mentions_third_party_spending}")

    print(f"\n[STATUT GLOBAL] {risques['status']}")
    for w in risques["warnings"]:
        print(f"  - {w}")


def main():
    parser = argparse.ArgumentParser(
        description="Audit de publication PMDQ — détection tactiques + traçabilité"
    )
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument("--fichier", type=Path, help="Fichier à auditer (.md, .txt, .html)")
    source.add_argument("--texte", type=str, help="Texte direct")
    parser.add_argument("--output", choices=["text", "json"], default="text")
    parser.add_argument("--no-registry", action="store_true",
                        help="Ne pas archiver dans audit_registry.jsonl")
    args = parser.parse_args()

    if args.fichier:
        if not args.fichier.exists():
            print(f"Erreur : fichier introuvable : {args.fichier}")
            return 1
        text = args.fichier.read_text(encoding="utf-8")
    else:
        text = args.texte

    extraction = extract_message(text)
    extraction = enforce_traceability(extraction)
    risques = evaluate_electoral_risk(extraction)

    if args.output == "json":
        print(json.dumps({
            "extraction": json.loads(extraction.model_dump_json()),
            "risques": risques,
        }, indent=2, ensure_ascii=False))
    else:
        afficher_rapport(extraction, risques)

    if not args.no_registry:
        append_record(text, extraction.model_dump_json())

    return 0 if risques["status"] == "OK" else 1


if __name__ == "__main__":
    raise SystemExit(main())
