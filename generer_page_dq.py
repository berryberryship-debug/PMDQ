import json
from pathlib import Path

data = json.loads(Path("sources/donnees_quebec.json").read_text(encoding="utf-8"))

sections = ""
for terme, contenu in data["mots_cles"].items():
    lignes = ""
    for j in contenu["jeux"]:
        org = j.get("organisation") or "N/A"
        lignes += f'<tr><td><a href="https://www.donneesquebec.ca/recherche/dataset/{j["id"]}" target="_blank">{j["titre"]}</a></td><td>{org}</td></tr>\n'
    sections += f'<h2 style="color:#1a3555;margin-top:2rem;">{terme.capitalize()} ({contenu["total"]} jeu(x))</h2>\n'
    sections += '<div style="overflow-x:auto;"><table style="width:100%;border-collapse:collapse;font-size:0.9em;">'
    sections += '<thead><tr style="background:#1a3555;color:white;"><th style="padding:0.5rem;text-align:left;">Titre</th><th style="padding:0.5rem;text-align:left;">Organisation</th></tr></thead><tbody>\n'
    sections += lignes + '</tbody></table></div>\n'

nav = '''<a href="index.html">Accueil</a> <a href="changelog.html">Changelog</a> <a href="livres.html">Livres</a> <a href="lois.html">Lois</a> <a href="ideologie.html">Idéologie</a> <a href="programme-2030.html">Programme 2030</a> <a href="propositions.html">Propositions</a> <a href="sources-externes.html">Sources externes</a> <a href="tout.html">Tout</a> <a href="moteurs.html">Moteurs</a> <a href="livre-blanc.html">Livre blanc</a> <a href="methodologie.html">Méthodologie</a> <a href="propriete-intellectuelle.html">PI</a>'''

html = f'''<!DOCTYPE html>
<html lang="fr">
<head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Données publiques — PMDQ v2.7.24</title><link rel="stylesheet" href="style.css"></head>
<body>
<div class="logo-banner"><div class="logo-banner__inner"><div class="logo-banner__lys">⚜</div><div class="logo-banner__text"><div class="logo-banner__name">PMDQ</div><div class="logo-banner__sub">Parti de la Mouvance Démocratique du Québec</div></div></div></div>
<header class="site-header"><div class="site-header__inner"><div class="brand">PMDQ v2.7.24<span>Données publiques</span></div><nav class="nav">{nav}</nav></div></header>
<main>
<section style="max-width:1000px;margin:2rem auto;padding:1rem 1.5rem;line-height:1.7;">
<h1 style="color:#1a3555;border-bottom:3px solid #2980b9;padding-bottom:0.5rem;">Données publiques</h1>
<p>Cette page est générée automatiquement par <code>moteur_donnees_quebec.py</code>, qui interroge l'API officielle de <a href="https://www.donneesquebec.ca/" target="_blank">Données Québec</a>. Aucune clé API, aucun scraping non autorisé, aucune donnée revendue.</p>
<p><strong>Dernière collecte :</strong> {data['date_collecte']} — <strong>Source :</strong> {data['source']}</p>
{sections}
<p style="margin-top:3rem;padding:1rem;background:#eaf5ea;border-left:4px solid #27ae60;border-radius:4px;"><em>Chaque jeu référencé est accessible directement via Données Québec. Le PMDQ cite ses sources, il ne les cache pas.</em></p>
<p style="margin-top:1.5rem;"><a href="index.html">← Retour à l'accueil</a></p>
</section></main>
<footer class="footer"><p><strong>PMDQ — Version 2.7.24 + Livre X</strong></p><p>Documentairement clos. Arithmétiquement propre. Techniquement arbitré. Non adopté.</p></footer>
</body></html>'''

Path("donnees-publiques.html").write_text(html, encoding="utf-8")
print(f"✓ donnees-publiques.html généré ({len(data['mots_cles'])} sections)")
