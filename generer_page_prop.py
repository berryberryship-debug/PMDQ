"""Régénère propositions.html à partir de sources/registre_propositions.json."""
import json
from pathlib import Path

data = json.loads(Path("sources/registre_propositions.json").read_text(encoding="utf-8"))

couleurs = {"[C]": "#27ae60", "[K]": "#f39c12", "[É]": "#2980b9",
            "[T]": "#8e44ad", "[P]": "#e74c3c"}

lignes = ""
for p in data["propositions"]:
    c = couleurs.get(p["statut"], "#555")
    lignes += (
        f'<tr>'
        f'<td><code>{p["id"]}</code></td>'
        f'<td>{p["titre"]}</td>'
        f'<td>Eng. {p["engagement"]}</td>'
        f'<td><span style="color:{c};font-weight:bold;">{p["statut"]}</span></td>'
        f'<td>{p["cout_m"]} M$</td>'
        f'<td>{p["base_legale"]}</td>'
        f'<td><code>{p["moteur"]}</code></td>'
        f'</tr>\n'
    )

nav = '''<a href="index.html">Accueil</a> <a href="changelog.html">Changelog</a> <a href="livres.html">Livres</a> <a href="lois.html">Lois</a> <a href="ideologie.html">Idéologie</a> <a href="programme-2030.html">Programme 2030</a> <a href="tout.html">Tout</a> <a href="moteurs.html">Moteurs</a> <a href="livre-blanc.html">Livre blanc</a> <a href="methodologie.html">Méthodologie</a> <a href="propriete-intellectuelle.html">PI</a>'''

html = f'''<!DOCTYPE html>
<html lang="fr">
<head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Registre des propositions — PMDQ v2.7.24</title><link rel="stylesheet" href="style.css"></head>
<body>
<div class="logo-banner"><div class="logo-banner__inner"><div class="logo-banner__lys">⚜</div><div class="logo-banner__text"><div class="logo-banner__name">PMDQ</div><div class="logo-banner__sub">Parti de la Mouvance Démocratique du Québec</div></div></div></div>
<header class="site-header"><div class="site-header__inner"><div class="brand">PMDQ v2.7.24<span>Registre des propositions</span></div><nav class="nav">{nav}</nav></div></header>
<main>
<section style="max-width:1100px;margin:2rem auto;padding:1rem 1.5rem;line-height:1.7;">
<h1 style="color:#1a3555;border-bottom:3px solid #2980b9;padding-bottom:0.5rem;">Registre des propositions</h1>
<p>Chaque engagement du <a href="programme-2030.html">Programme 2030</a> est associé à une ou plusieurs propositions législatives ou réglementaires. Ce registre est la <strong>source de vérité</strong> du pont entre la vision politique et les textes de loi.</p>
<p><strong>Statuts :</strong>
<span style="color:#27ae60;">[C] Certain</span> ·
<span style="color:#f39c12;">[K] Conditionnel</span> ·
<span style="color:#2980b9;">[É] À l'étude</span> ·
<span style="color:#8e44ad;">[T] Technique</span> ·
<span style="color:#e74c3c;">[P] Politique</span></p>
<p><strong>{data["total"]} propositions</strong> au registre — version {data["version"]} — {data["date"]}</p>
<div style="overflow-x:auto;">
<table style="width:100%;border-collapse:collapse;font-size:0.9em;">
<thead><tr style="background:#1a3555;color:white;">
<th style="padding:0.6rem;text-align:left;">ID</th>
<th style="padding:0.6rem;text-align:left;">Titre</th>
<th style="padding:0.6rem;text-align:left;">Eng.</th>
<th style="padding:0.6rem;text-align:left;">Statut</th>
<th style="padding:0.6rem;text-align:left;">Coût</th>
<th style="padding:0.6rem;text-align:left;">Base légale</th>
<th style="padding:0.6rem;text-align:left;">Moteur</th>
</tr></thead>
<tbody>
{lignes}</tbody>
</table></div>
<p style="margin-top:2rem;"><em>Généré depuis <code>sources/registre_propositions.json</code> par <code>generer_page_prop.py</code>.</em></p>
<p style="margin-top:1rem;"><a href="index.html">← Retour à l'accueil</a></p>
</section></main>
<footer class="footer"><p><strong>PMDQ — Version 2.7.24 + Livre X</strong></p><p>Documentairement clos. Arithmétiquement propre. Techniquement arbitré. Non adopté.</p></footer>
</body></html>'''

Path("propositions.html").write_text(html, encoding="utf-8")
print(f"✓ propositions.html régénéré ({data['total']} propositions)")
