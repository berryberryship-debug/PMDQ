"""
Audit en lot de plusieurs fichiers texte.

Usage :
    python audit_batch.py --dir textes/
    python audit_batch.py --dir textes/ --out resultats/
"""
import argparse
import json
from pathlib import Path

from engines import ExtractionEngine
from rules import (
    enforce_traceability,
    evaluate_electoral_risk,
    evaluate_gold_card_legal_risks,
)


def auditer_texte(texte: str) -> dict:
    engine = ExtractionEngine()
    raw = engine.extract(texte)
    validated = enforce_traceability(raw)
    electoral = evaluate_electoral_risk(validated)
    gold = evaluate_gold_card_legal_risks(validated)
    return {
        "public_cible": validated.target_audience,
        "nb_affirmations": len(validated.traceability_audit),
        "nb_non_sourcees": sum(
            1 for c in validated.traceability_audit
            if c.claim_type != "normative_statement" and not c.is_sourced
        ),
        "cialdini_actifs": [
            t.principle for t in validated.cialdini_audit
            if t.presence != "absent"
        ],
        "imprimatur_requis": electoral["requires_imprimatur"],
        "score": gold["compliance_score"],
        "verdict": gold["verdict"],
        "chiffrage_faisable": gold["financial_feasibility"]["faisabilite"],
    }


def main():
    parser = argparse.ArgumentParser(description="Audit en lot de fichiers texte.")
    parser.add_argument("--dir", required=True,
                        help="Dossier contenant les fichiers .txt a auditer.")
    parser.add_argument("--out", default=None,
                        help="Dossier de sortie pour les JSON individuels.")
    args = parser.parse_args()

    dossier = Path(args.dir)
    if not dossier.is_dir():
        print(f"ERREUR : {args.dir} n'est pas un dossier.")
        return

    fichiers = sorted(dossier.glob("*.txt"))
    if not fichiers:
        print(f"Aucun fichier .txt dans {args.dir}")
        return

    if args.out:
        Path(args.out).mkdir(parents=True, exist_ok=True)

    print("=" * 90)
    print(f"AUDIT EN LOT — {len(fichiers)} fichier(s)")
    print("=" * 90)
    print(f"{'Fichier':<30} {'Score':>6} {'Verdict':<15} "
          f"{'Non srce':>9} {'Cialdini':<20} {'Imp':<4}")
    print("-" * 90)

    resultats = []

    for f in fichiers:
        texte = f.read_text(encoding="utf-8")
        res = auditer_texte(texte)
        resultats.append({"fichier": f.name, **res})

        cialdini_str = ",".join(res["cialdini_actifs"][:2]) or "-"
        if len(res["cialdini_actifs"]) > 2:
            cialdini_str += ",+"

        print(f"{f.name:<30} {res['score']:>5}/100 "
              f"{res['verdict']:<15} {res['nb_non_sourcees']:>9} "
              f"{cialdini_str:<20} {str(res['imprimatur_requis']):<4}")

        if args.out:
            out_file = Path(args.out) / f"{f.stem}.json"
            out_file.write_text(
                json.dumps(res, ensure_ascii=False, indent=2),
                encoding="utf-8",
            )

    print("-" * 90)
    non_conformes = [r for r in resultats if r["verdict"] != "CONFORME"]
    print(f"Total : {len(resultats)} fichier(s)")
    print(f"Conformes : {len(resultats) - len(non_conformes)}")
    print(f"Non conformes : {len(non_conformes)}")
    if non_conformes:
        print("\nFichiers à revoir :")
        for r in non_conformes:
            print(f"  - {r['fichier']} ({r['verdict']})")
    print("=" * 90)


if __name__ == "__main__":
    main()
