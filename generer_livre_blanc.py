#!/usr/bin/env python3
"""
generer_livre_blanc.py — Generation du livre blanc PMDQ
v2.7.22

Assemble un document Markdown a partir de tout le socle :
    - etat_variables.json
    - cache_economique.json
    - observations_manuelles.json
    - sorties des moteurs
    - fichier etat_socle.txt (journal)

Usage :
    python3 generer_livre_blanc.py
    python3 generer_livre_blanc.py --sortie livre_blanc.md
"""

import argparse
import json
import subprocess
import sys
from datetime import date
from pathlib import Path


SORTIE_DEFAUT = "livre_blanc.md"


def lire_json(chemin, defaut=None):
    p = Path(chemin)
    if not p.exists():
        return defaut
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return defaut


def executer_moteur(nom, args=None):
    """Execute un moteur et retourne sa sortie (stdout)."""
    cmd = ["python3", nom] + (args or [])
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        return r.stdout
    except (subprocess.TimeoutExpired, OSError) as e:
        return f"[ECHEC {nom}: {e}]"


def section_titre(version):
    return f"""# PMDQ — Livre blanc

**Version du socle** : {version}
**Date de generation** : {date.today()}
**Origine** : genere automatiquement depuis les moteurs et les caches de donnees

---

"""


def section_resume_executif(etat, cache, obs):
    r = etat.get("resume", {}) if etat else {}
    nb_sources = len([k for k in cache if not k.startswith("_")]) if cache else 0
    nb_obs = sum(len(v) for v in obs.get("observations", {}).values()) if obs else 0

    lignes = ["## Resume executif\n"]
    lignes.append(f"Le socle PMDQ compte actuellement :\n")
    lignes.append(f"- **{r.get('total', 0)} sections** de variables sensibles suivies")
    lignes.append(f"- **{r.get('a_jour', 0)} sections a jour**, {r.get('en_retard', 0)} en retard, {r.get('a_revoir', 0)} a revoir")
    lignes.append(f"- **{nb_sources} sources economiques officielles** collectees automatiquement")
    lignes.append(f"- **{nb_obs} observations manuelles** enregistrees")

    alertes = []
    if r.get("en_retard", 0):
        alertes.append(f"{r['en_retard']} section(s) en retard")
    if r.get("a_revoir", 0):
        alertes.append(f"{r['a_revoir']} section(s) a revoir")
    if alertes:
        lignes.append(f"\n**Alertes** : {', '.join(alertes)}.")
    else:
        lignes.append(f"\n**Aucune alerte** : toutes les sections sont a jour.")

    lignes.append("")
    return "\n".join(lignes) + "\n"


def section_references(cache):
    if not cache:
        return "## References economiques\n\nAucune source collectee.\n\n"

    lignes = ["## References economiques officielles\n"]
    lignes.append("| Cle | Valeur | Unite | Date observation | Source |")
    lignes.append("|---|---:|---|---|---|")
    for cle, info in sorted(cache.items()):
        if cle.startswith("_") or not isinstance(info, dict):
            continue
        nom = cle.replace("_", " ")
        val = info.get("valeur", "?")
        unite = info.get("unite", "")
        d = info.get("date_observation", info.get("annee", "?"))
        src = info.get("source", "?")
        lignes.append(f"| {nom} | {val} | {unite} | {d} | {src} |")
    lignes.append("")
    return "\n".join(lignes) + "\n"


def section_observations(obs):
    if not obs or not obs.get("observations"):
        return ""
    lignes = ["## Observations manuelles\n"]
    for cle, items in obs.get("observations", {}).items():
        if not items:
            continue
        nom = cle.replace("_", " ")
        lignes.append(f"### {nom}\n")
        lignes.append("| Date | Valeur | Unite | Lieu |")
        lignes.append("|---|---:|---|---|")
        for item in sorted(items, key=lambda x: x.get("date", "")):
            v = item.get("valeur", "?")
            u = item.get("unite", "")
            d = item.get("date", "?")
            lieu = item.get("ville", item.get("lieu", ""))
            lignes.append(f"| {d} | {v} | {u} | {lieu} |")
        lignes.append("")
    return "\n".join(lignes) + "\n"


def section_moteurs():
    lignes = ["## Analyses par moteur\n"]
    moteurs = [
        ("moteur_variables.py", [], "Variables sensibles"),
        ("moteur_domar.py", [], "Dynamique de la dette"),
        ("moteur_domar.py", ["--officiel"], "Dynamique de la dette (officiel)"),
        ("moteur_fiscal.py", [], "Analyse fiscale"),
        ("moteur_etancheite.py", [], "Etancheite budgetaire"),
        ("moteur_provisionnement.py", [], "Provisionnement actuariel"),
        ("moteur_rendement.py", [], "Rendement"),
        ("moteur_vehicule.py", [], "Analyse vehicule"),
        ("moteur_coherence.py", [], "Coherence inter-moteurs"),
        ("moteur_ecarts.py", [], "Ecarts registre / officiel"),
        ("moteur_nomenclature.py", [], "Nomenclature vehicule biplace"),
    ]
    for nom, args, titre in moteurs:
        lignes.append(f"### {titre}\n")
        lignes.append("```")
        sortie = executer_moteur(nom, args)
        lignes.append(sortie.rstrip())
        lignes.append("```")
        lignes.append("")
    return "\n".join(lignes) + "\n"


def section_journal():
    p = Path("etat_socle.txt")
    if not p.exists():
        return ""
    contenu = p.read_text(encoding="utf-8")
    lignes = ["## Journal du socle\n", "```", contenu.rstrip(), "```", ""]
    return "\n".join(lignes) + "\n"


def section_sources_inactives():
    lignes = ["## Sources inactives\n"]
    lignes.append("### Series StatCan arretees\n")
    lignes.append("- **735059** (Prix de detail essence, Quebec) : serie non publiee depuis 2025-09. Le tableau 18-10-0001 n'est plus alimente. Remplacement : saisie manuelle.\n")
    lignes.append("")
    return "\n".join(lignes) + "\n"


def compter_mots(texte):
    return len(texte.split())


def main():
    parser = argparse.ArgumentParser(description="Generer le livre blanc")
    parser.add_argument("--sortie", type=str, default=SORTIE_DEFAUT)
    args = parser.parse_args()

    etat = lire_json("sources/etat_variables.json", {})
    cache = lire_json("sources/cache_economique.json", {})
    obs = lire_json("sources/observations_manuelles.json", {})

    version = "v2.7.22"

    blocs = [
        section_titre(version),
        section_resume_executif(etat, cache, obs),
        section_references(cache),
        section_observations(obs),
        section_moteurs(),
        section_journal(),
        section_sources_inactives(),
    ]

    document = "\n".join(blocs)
    Path(args.sortie).write_text(document, encoding="utf-8")

    mots = compter_mots(document)
    pages_400 = mots / 400
    pages_500 = mots / 500

    print()
    print("=" * 72)
    print("  LIVRE BLANC GENERE — PMDQ")
    print("=" * 72)
    print(f"  Fichier    : {args.sortie}")
    print(f"  Mots       : {mots:,}")
    print(f"  Pages (~400 mots/p) : {pages_400:.1f}")
    print(f"  Pages (~500 mots/p) : {pages_500:.1f}")
    print("=" * 72)
    print()


if __name__ == "__main__":
    main()
