"""
Export JSON du rapport d'audit.
Usage :
    python export_json.py               # texte par defaut
    python export_json.py --out r.json  # sauvegarde
    echo "..." | python export_json.py  # stdin
"""
import argparse
import json
import sys
from datetime import datetime, timezone

from engines import ExtractionEngine
from rules import (
    enforce_traceability,
    evaluate_electoral_risk,
    evaluate_gold_card_legal_risks,
)


TEXTE_DEFAUT = """
Une nouvelle politique secrete accorderait une Gold Card prioritaire
aux riches Americains pour acceder a nos blocs operatoires au Quebec et
en Ontario en moins de 48 heures. Selon un rapport recent du Conseil de
la Sante publie en 2024, plus de 35 000 patients d'ici voient leurs
chirurgies repoussees a cause de ce programme prive de 120 millions $.
Nos familles meritent un acces universel et equitable, pas un systeme a
deux vitesses.
Mobilisez-vous et signez notre petition officielle avant le vote du
15 novembre.
"""


def audit_vers_dict(texte: str) -> dict:
    engine = ExtractionEngine()
    raw = engine.extract(texte)
    validated = enforce_traceability(raw)
    electoral = evaluate_electoral_risk(validated)
    gold = evaluate_gold_card_legal_risks(validated)

    return {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "version_moteur": "pmdq-audit-1.0",
        "texte_source": texte.strip(),
        "public_cible": validated.target_audience,
        "traceabilite": [
            {
                "enonce": c.statement,
                "type": c.claim_type,
                "source": c.is_sourced,
                "reference": c.source_reference,
                "statut": c.compliance_status,
            }
            for c in validated.traceability_audit
        ],
        "cialdini": [
            {
                "principe": t.principle,
                "presence": t.presence,
                "application": t.application,
                "extraits": t.evidence,
            }
            for t in validated.cialdini_audit
            if t.presence != "absent"
        ],
        "risque_electoral": electoral,
        "bareme_gold_card": {
            "score_conformite": gold["compliance_score"],
            "verdict": gold["verdict"],
            "federal": gold["federal_barriers"],
            "quebec": gold["provincial_barriers_qc"],
            "ontario": gold["provincial_barriers_on"],
            "electoral": gold["electoral_risks"],
        },
        "chiffrage": gold["financial_feasibility"],
    }


def main():
    parser = argparse.ArgumentParser(description="Export JSON du rapport d'audit.")
    parser.add_argument("--out", help="Fichier de sortie JSON (defaut stdout).")
    parser.add_argument("--compact", action="store_true",
                        help="Sortie compacte (pas d'indentation).")
    args = parser.parse_args()

    if not sys.stdin.isatty():
        texte = sys.stdin.read()
    else:
        texte = TEXTE_DEFAUT

    rapport = audit_vers_dict(texte)
    indent = None if args.compact else 2
    sortie = json.dumps(rapport, ensure_ascii=False, indent=indent)

    if args.out:
        with open(args.out, "w", encoding="utf-8") as f:
            f.write(sortie)
        print(f"Rapport ecrit dans {args.out}")
    else:
        print(sortie)


if __name__ == "__main__":
    main()
