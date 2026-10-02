"""Génère donnees-socioeco.html depuis sources/donnees_socioeco.json."""
import json
from pathlib import Path

data = json.loads(Path("sources/donnees_socioeco.json").read_text(encoding="utf-8"))

sections = ""
for org, contenu in sorted(data["par_organisation"].items()):
    jeux_org = {}
    for terme, jeux in contenu["mots_cles"].items():
        for j in jeux:
            jeux_org[j["id"]] = j
    if not jeux_org:
        continue
    lignes = ""
    for j in sorted(jeux_org.values(), key=lambda x: (x["titre"] or "").lower()):
        obs = ' <span style="color:#e67e22;font-size:0.85em;">[données anciennes]</span>' if j.get("obsolète") else ""
        formats = ", ".join(j.get("formats", [])) or "—"
        licence = j.get("licence") or "—"
        date_m = (j.get("date_modif") or "")[:10] or "—"
        lignes += f'<tr><td><a href="https://www.donneesquebec.ca/recherche/dataset/{j["id"]}" target="_blank">{j["titre"]}</a>{obs}</td><td>{j.get("organisation") or org}</td><td>{date_m}</td><td>{formats}</td><td>{licence}</td></tr>\n'
    sections += f'\n<h2 style="color:#1a3555;margin-top:2rem;">{org} <span style="font-size:0.8em;color:#666;">({len(jeux_org)} jeu(x))</span></h2>\n<div style="overflow-x:auto;">\n<table style="width:100%;border-collapse:collapse;font-size:0.9em;">\n<thead><tr style="background:#1a3555;color:white;"><th style="padding:0.5rem;text-align:left;">Titre</th><th style="padding:0.5rem;text-align:left;">Organisation</th><th style="padding:0.5rem;text-align:left;">Mise à jour</th><th style="padding:0.5rem;text-align:left;">Formats</th><th style="padding:0.5rem;text-align:left;">Licence</th></tr></thead>\n<tbody>\n{lignes}</tbody></table></div>\n'

html = f'''<!DOCTYPE html>
<html lang="fr">
<head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Données socio-économiques — PMDQ v2.7.24</title><link rel="stylesheet" href="style.css"></head>
<body>
<div class="logo-banner"><div class="logo-banner__inner"><div class="logo-banner__lys">⚜</div><div class="logo-banner__text"><div class="logo-banner__name">PMDQ</div><div class="logo-banner__sub">Parti de la Mouvance Démocratique du Québec</div></div></div></div>
<header class="site-header"><div class="site-header__inner"><div class="brand">PMDQ v2.7.24<span>Données socio-économiques</span></div>
<nav class="nav">
<a href="index.html">Accueil</a>
<a href="changelog.html">Changelog</a>
<a href="livres.html">Livres</a>
<a href="lois.html">Lois</a>
<a href="ideologie.html">Idéologie</a>
<a href="programme-2030.html" class="bouton-vedette">Programme 2030</a>
<a href="tout.html">Tout</a>
<a href="moteurs.html">Moteurs</a>
<a href="livre-blanc.html">Livre blanc</a>
<a href="methodologie.html">Méthodologie</a>
<a href="propriete-intellectuelle.html">PI</a>
</nav></div></header>
<main>
<section style="max-width:1200px;margin:2rem auto;padding:1rem 1.5rem;line-height:1.7;">
<h1 style="color:#1a3555;border-bottom:3px solid #2980b9;padding-bottom:0.5rem;">Données socio-économiques</h1>
<p>Page générée automatiquement par <code>moteur_socioeco.py</code> depuis l'API officielle de <a href="https://www.donneesquebec.ca/" target="_blank">Données Québec</a>. Elle regroupe les jeux de données publiés par 11 organisations québécoises sur l'emploi, le revenu, la population, l'immigration, la santé, l'éducation et les finances.</p>
<p><strong>Dernière collecte :</strong> {data['date_collecte']} — <strong>{data['total_jeux_uniques']} jeux uniques</strong></p>
{sections}
<p style="margin-top:3rem;padding:1rem;background:#eaf5ea;border-left:4px solid #27ae60;border-radius:4px;"><em>Chaque jeu est accessible directement via Données Québec. Les jeux marqués « données anciennes » n'ont pas été mis à jour depuis plus de 2 ans.</em></p>
<p style="margin-top:1.5rem;"><a href="index.html">← Retour à l'accueil</a></p>
</section></main>
<footer class="footer"><p><strong>PMDQ — Version 2.7.24 + Livre X</strong></p><p>Documentairement clos. Arithmétiquement propre. Techniquement arbitré. Non adopté.</p></footer>
</body></html>'''

Path("donnees-socioeco.html").write_text(html, encoding="utf-8")
print(f"✓ donnees-socioeco.html généré ({data['total_jeux_uniques']} jeux)")
