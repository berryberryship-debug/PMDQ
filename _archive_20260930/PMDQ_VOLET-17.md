# VOLET 17 — Audit sémantique des messages publics
## Extension proposée du Livre V — Dossier Maître PMDQ v2.6.3

---

## §17.1 — Objet

Le protocole d'audit en 16 volets couvre la conformité juridique,
comptable, arithmétique, environnementale, sociale et autochtone des
actes du dispositif FQBC.

Il ne couvre pas l'analyse sémantique des messages publics diffusés en
lien avec le FQBC (communications, pétitions, publicités électorales).
Le Volet 17 comble cette lacune.

---

## §17.2 — Les 4 axes d'analyse

### Axe 1 — Traçabilité factuelle
Chaque affirmation chiffrée doit être sourcée. Sans source explicite,
l'affirmation devient une hypothèse cachée.

### Axe 2 — Leviers rhétoriques (Cialdini)
Détection des mécanismes de persuasion : Reciprocity, Scarcity,
Authority, Consistency, Liking, Social_Proof, Unity.

### Axe 3 — Risques électoraux (DGEQ)
Détection des appels à l'action et des dépenses de tiers.

### Axe 4 — Barrières légales et chiffrage
Analyse des références légales applicables et chiffrage paramétrique.

---

## §17.3 — Insertion dans le protocole existant

| Volet | Interaction avec V17 |
|---|---|
| V1-V3 | V17 alimente les volets juridiques |
| V6 | V17 vérifie la cohérence des chiffres |
| V7 | V17 signale les hypothèses cachées |
| V12 | V17 détecte les messages discriminatoires |
| V15 | V17 est implémenté en Python testable |

V17 ne se substitue à aucun volet. Il les complète.

---

## §17.4 — Chaîne de traitement

Texte brut, puis extraction déterministe, règles de traçabilité,
risque électoral, barrières légales, chiffrage, verdict.

5 étapes sur 6 sont déterministes.

---

## §17.5 — Seuils et verdicts

| Score | Verdict | Action |
|---|---|---|
| 80-100 | CONFORME | Aucune |
| 50-79 | RISQUE MODÉRÉ | Révision |
| 0-49 | RISQUE ÉLEVÉ | Blocage |

Barème des pénalités :
- Affirmation non sourcée : -10 par occurrence
- Accès prioritaire payant : -30
- Mention de non-résidents : -25
- Appel à l'action électoral : -15
- Financement étranger : -20
- Cumul (3 facteurs ou plus) : -10 fois (n - 2)

---

## §17.6 — Référentiel légal

Fédéral : Loi canadienne sur la santé, art. 10-11.

Québec : S-4.2 art. 108, A-29 art. 30-33, E-3.3 art. 427-430,
Loi sur le financement des partis art. 75.

Ontario : Public Hospitals Act art. 29, Health Insurance Act
art. 27-30.

---

## §17.7 — Implémentation logicielle

Fichiers : schemas.py, engines.py, rules.py, main.py,
export_json.py, audit_batch.py, pmdq_bridge.py, test_main.py,
test_cas.py.

Reproductibilité : aucun appel réseau.

---

## §17.8 — Limites explicites

1. Détection par mots-clés : vocabulaire non répertorié = manqué.
2. Chiffrage non officiel : hypothèses à valider.
3. Signal, pas avis juridique.

---

## §17.9 — Statut d'activation

Proposition non activée. Pour activer :
1. Validation par le Conseil de surveillance
2. Ajout formel au Livre V
3. Bump de version vers v2.7.0

---

## §17.10 — Cas d'usage validé

CAS_1 gold card : score 0/100, RISQUE ÉLEVÉ.

CAS_4 chiffres non sourcés : score 70/100, RISQUE MODÉRÉ.

Ces deux cas démontrent la capacité du moteur à distinguer un texte
dangereux d'un texte à réviser.

---

## §17.11 — Articulation avec le dossier PMDQ v2.6.3

Le Volet 17 se branche via pmdq_bridge.py, qui charge l'empreinte de
contrôle, détecte les valeurs obsolètes et vérifie les invariants I2
et I7.

Voir PMDQ_INTEGRATION.md pour la documentation complète.

---

*Fin du Volet 17.*
