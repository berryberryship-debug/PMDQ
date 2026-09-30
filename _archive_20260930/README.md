# PMDQ — Moteur d'audit sémantique (Volet 17)

Moteur d'analyse déterministe de messages politiques liés au Fonds
québécois du bien commun (FQBC). Aucune clé API, aucun réseau.

## Installation

    pkg update && pkg upgrade -y
    pkg install python -y
    pip install -r requirements.txt

## Utilisation

    python main.py                    # rapport lisible (texte par défaut)
    python export_json.py --out r.json  # sortie machine
    python test_cas.py                # calibration 5 cas
    pytest test_main.py -v            # 6 tests unitaires
    python audit_batch.py --dir textes/  # audit en lot

## Architecture

- `schemas.py`       : modèles Pydantic stricts (extra="forbid")
- `engines.py`       : extraction regex (Cialdini, CTA, chiffres)
- `rules.py`         : règles légales + chiffrage paramétrique
- `main.py`          : rapport lisible
- `export_json.py`   : export structuré JSON
- `audit_batch.py`   : audit multi-fichiers
- `test_main.py`     : tests unitaires
- `test_cas.py`      : calibration sur 5 textes contrastés

## Barèmes

| Score | Verdict | Action |
|---|---|---|
| 80-100 | CONFORME | Aucune |
| 50-79  | RISQUE MODÉRÉ | Révision |
| 0-49   | RISQUE ÉLEVÉ | Blocage recommandé |

## Barrières légales détectées

**Fédéral** : Loi canadienne sur la santé (art. 10-11).
**Québec** : S-4.2, A-29, E-3.3, art. 75 Loi financement.
**Ontario** : Public Hospitals Act, Health Insurance Act.

## Limites

1. Détection par mots-clés (regex). Vocabulaire non répertorié = manqué.
2. Chiffrage paramétrique — hypothèses à valider sur données officielles.
3. Signal, pas avis juridique.

## Reproductibilité

- Aucun appel réseau.
- Résultats identiques bit à bit pour une même entrée.
- 5 cas de calibration + 6 tests unitaires fournis.
