# VOLET 17 — Audit sémantique des messages publics
## Extension proposée du Livre V — Dossier Maître PMDQ v2.6.3

---

## §17.1 — Objet

Le protocole d'audit en 16 volets (Livre V) couvre la conformité
juridique, comptable, arithmétique, environnementale, sociale et
autochtone des **actes** du dispositif FQBC.

Il ne couvre pas un objet distinct : **l'analyse sémantique des
messages publics** diffusés en lien avec le FQBC (communications,
pétitions, publicités électorales, prises de parole publiques).

Le Volet 17 comble cette lacune.

---

## §17.2 — Les 4 axes d'analyse

### Axe 1 — Traçabilité factuelle
Chaque affirmation chiffrée (montant, pourcentage, volume) doit être
sourcée. Sans source explicite, l'affirmation devient une hypothèse
cachée — et doit être traitée comme telle.

**Règle** : blocage pour les affirmations `empirical_fact` et
`economic_projection` non sourcées.

### Axe 2 — Leviers rhétoriques (Cialdini)
Détection des mécanismes de persuasion :

- Reciprocity, Scarcity, Authority, Consistency, Liking,
  Social_Proof, Unity.

**Règle** : signalement, sans pénalité directe. L'usage de ces
leviers est légitime en soi ; leur cumul avec des affirmations
trompeuses devient problématique.

### Axe 3 — Risques électoraux (DGEQ)
Détection des appels à l'action et des dépenses de tiers.

**Règle** : imprimatur obligatoire en cas de CTA. Surveillance si
dépense de tiers > 1 000 $.

### Axe 4 — Barrières légales et chiffrage
Analyse des références légales applicables (fédéral, Québec, Ontario)
et chiffrage paramétrique du dispositif promu.

**Règle** : verdict CONFORME / MODÉRÉ / ÉLEVÉ selon score cumulé.

---

## §17.3 — Insertion dans le protocole existant

| Volet | Interaction avec V17 |
|---|---|
| V1-V3 | V17 alimente les volets juridiques en signalant les manquements |
| V6 | V17 vérifie la cohérence des chiffres cités avec la spec |
| V7 | V17 signale les affirmations non sourcées = hypothèses cachées |
| V12 | V17 détecte les messages discriminatoires |
| V15 | V17 est implémenté comme extension Python testable |

**V17 ne se substitue à aucun volet.** Il les complète.

---

## §17.4 — Chaîne de traitement

    Texte brut
        │
        ▼
    [1] Extraction déterministe (regex + dictionnaires)
        │
        ▼
    [2] Règles de traçabilité (sourcé / non sourcé)
        │
        ▼
    [3] Évaluation du risque électoral (DGEQ)
        │
        ▼
    [4] Analyse des barrières légales (fédéral, QC, ON)
        │
        ▼
    [5] Chiffrage paramétrique
        │
        ▼
    [6] Verdict : CONFORME / MODÉRÉ / ÉLEVÉ

**5 étapes sur 6 sont déterministes.**

---

## §17.5 — Seuils et verdicts

| Score | Verdict | Action recommandée |
|---|---|---|
| 80-100 | CONFORME | Aucune |
| 50-79  | RISQUE MODÉRÉ | Révision avant diffusion |
| 0-49   | RISQUE ÉLEVÉ | Blocage recommandé |

**Barème des pénalités** :
- Affirmation non sourcée : −10 par occurrence.
- Accès prioritaire payant : −30.
- Mention de non-résidents : −25.
- Appel à l'action électoral : −15.
- Financement étranger : −20.
- Cumul (≥3 facteurs) : −10 × (n − 2).

---

## §17.6 — Référentiel légal

### Fédéral
- Loi canadienne sur la santé (L.R.C. 1985, ch. C-6, art. 10-11).

### Québec
- Loi sur les services de santé (RLRQ c. S-4.2, art. 108).
- Loi sur l'assurance maladie (RLRQ c. A-29, art. 30-33).
- Loi électorale (RLRQ c. E-3.3, art. 427-430).
- Loi sur le financement des partis (art. 75).

### Ontario
- Public Hospitals Act (art. 29).
- Health Insurance Act (art. 27-30).

---

## §17.7 — Implémentation logicielle

Le volet est implémenté par le moteur `pmdq-audit-1.0` :

| Fichier | Rôle |
|---|---|
| `schemas.py` | Modèles Pydantic stricts |
| `engines.py` | Extraction déterministe |
| `rules.py` | Règles légales + chiffrage |
| `main.py` | Rapport lisible |
| `export_json.py` | Export machine |
| `audit_batch.py` | Audit multi-fichiers |
| `test_main.py` | Tests unitaires (6) |
| `test_cas.py` | Calibration (5 cas) |

**Reproductibilité** : aucun appel réseau, résultats identiques
bit à bit pour une même entrée.

---

## §17.8 — Limites explicites

1. **Détection par mots-clés** : un texte qui reformule avec un
   vocabulaire non répertorié peut échapper au moteur.
2. **Chiffrage non officiel** : les hypothèses (prix, coûts,
   volumes) sont des valeurs de test.
3. **Avis juridique non rendu** : le verdict est un signal, pas une
   conclusion opposable.

---

## §17.9 — Statut d'activation

**Proposition documentée, non activée.**

Pour activer le Volet 17 :

1. Validation par le Conseil de surveillance.
2. Ajout formel au Livre V (16 → 17 volets).
3. Bump de version du dossier PMDQ → v2.7.0.
4. Publication du présent document en annexe.

---

## §17.10 — Cas d'usage validé

**CAS_1 gold card évident** → score 0/100 → RISQUE ÉLEVÉ.
- 4 facteurs cumulés (prioritaire + non-résidents + CTA + financement).
- Pénalités : −30 −25 −15 −20 −20 (cumul) = −110 → plancher 0.

**CAS_4 chiffres non sourcés** → score 70/100 → RISQUE MODÉRÉ.
- 3 affirmations non sourcées : −30.
- Aucun autre facteur → pas de cumul.

Ces deux cas démontrent la capacité du moteur à distinguer
un texte dangereux (RISQUE ÉLEVÉ) d'un texte à réviser (MODÉRÉ).

---

*Fin du Volet 17.*
