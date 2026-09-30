#!/usr/bin/env python3
"""Génère un tableau de bord HTML du registre d'audit."""
import html
import json
from pathlib import Path

from audit_registry import read_all

OUTPUT = Path("audit_dashboard.html")


def generer():
    records = read_all()

    lignes = []
    for i, r in enumerate(records, 1):
        report = r.get("report", {})
        statut = "OK"
        if isinstance(report, dict):
            for claim in report.get("traceability_audit", []):
                if (claim.get("compliance_status") or "").startswith("BLOCAGE"):
                    statut = "BLOQUE"
                    break
                if (claim.get("compliance_status") or "").startswith("RÉVISION"):
                    statut = "A_REVISER"

        couleur = {"OK": "#27ae60", "A_REVISER": "#f39c12", "BLOQUE": "#c0392b"}[statut]

        lignes.append(f"""
        <tr>
          <td>{i}</td>
          <td>{html.escape(r.get('audited_at', ''))}</td>
          <td><span style="color:{couleur};font-weight:bold">{statut}</span></td>
          <td><code>{html.escape(r.get('text_sha256', '')[:16])}…</code></td>
          <td>{html.escape(r.get('text_preview', ''))}</td>
        </tr>
        """)

    contenu = f"""<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="UTF-8">
<title>Tableau de bord — Audit de publication</title>
<style>
body {{ font-family: -apple-system, sans-serif; max-width: 1100px; margin: 2rem auto; padding: 1rem; }}
h1 {{ color: #1a1a1a; }}
table {{ width: 100%; border-collapse: collapse; margin: 1rem 0; }}
th, td {{ border: 1px solid #ddd; padding: 0.5rem; text-align: left; font-size: 0.9rem; }}
th {{ background: #1a3555; color: white; }}
tr:nth-child(even) {{ background: #f9f9f9; }}
code {{ background: #eee; padding: 0.1em 0.3em; border-radius: 3px; }}
</style>
</head>
<body>
<h1>Tableau de bord — Audit de publication</h1>
<p><strong>{len(records)}</strong> enregistrement(s) dans le registre.</p>
<table>
  <thead>
    <tr><th>#</th><th>Date (UTC)</th><th>Statut</th><th>SHA-256 texte</th><th>Aperçu</th></tr>
  </thead>
  <tbody>
    {''.join(lignes)}
  </tbody>
</table>
<p style="color:#666;font-size:0.85rem;">
  Ce tableau est généré depuis <code>audit_registry.jsonl</code>.
  Le SHA-256 permet de vérifier l'intégrité de chaque texte audité.
</p>
</body>
</html>"""

    OUTPUT.write_text(contenu, encoding="utf-8")
    print(f"✓ Tableau de bord généré : {OUTPUT}")
    print(f"  {len(records)} enregistrement(s)")


if __name__ == "__main__":
    generer()
