# Module 5 — Les 5 constantes du calcul D

**Moteur associé** : `moteur_vehicule.py`
**Statut global** : hypothèses [SCÉN] non sourcées
**Ratio D actuel** : 2,337

---

## Constante 1 — Économies d'exploitation (base 5 ans)

- **Définition** : économies annuelles attendues sur un pilote industriel de 5 ans, exprimées en M$ par période.
- **Valeur** : 0,81 M$ / 5 ans
- **Règle** : doublée pour couvrir 10 ans → 0,81 × 2 = 1,62 M$
- **Exemple** : `economies_10ans = 0.81 * 2`
- **Anti-exemple** : ce n'est PAS un revenu brut, c'est un différentiel de coûts.
- **Source** : [à obtenir — comparable : gains d'exploitation d'un pilote industriel au Québec]
- **Statut** : [SCÉN]
- **Condition d'arrêt** : si le scénario central change d'horizon, réévaluer.

---

## Constante 2 — Investissement robots total

- **Définition** : montant total présumé pour équiper un site industriel en robots.
- **Valeur** : 8,0 M$
- **Règle** : sert de **dénominateur** pour calculer la quote-part du pilote (2,5 M$).
- **Exemple** : `part_robotique = (2.5 / 8.0) * 6.40`
- **Anti-exemple** : ce n'est PAS la valeur résiduelle des robots (voir constante 3).
- **Source** : [à obtenir — devis intégrateur type, ABB / KUKA / Fanuc / Revtech]
- **Statut** : [SCÉN]
- **Condition d'arrêt** : si un devis formel est reçu, remplacer.

---

## Constante 3 — Valeur actifs robotiques

- **Définition** : valeur résiduelle estimée du parc robotique après amortissement.
- **Valeur** : 6,40 M$
- **Règle** : multipliée par la quote-part du pilote (2,5/8,0) → 2,00 M$.
- **Exemple** : `(2.5 / 8.0) * 6.40 = 2.00`
- **Anti-exemple** : ce n'est PAS le coût d'acquisition initial (voir constante 2).
- **Source** : [à obtenir — rapport d'évaluation actifs industriels]
- **Statut** : [SCÉN]
- **Condition d'arrêt** : si un devis ou une valeur résiduelle officielle est obtenue.

---

## Constante 4 — Investissement PI total

- **Définition** : montant total présumé investi en propriété intellectuelle.
- **Valeur** : 4,5 M$
- **Règle** : sert de **dénominateur** pour calculer la quote-part PI (2,5 M$).
- **Exemple** : `part_PI = (2.5 / 4.5) * 4.00`
- **Anti-exemple** : ce n'est PAS la valeur du portefeuille PI (voir constante 5).
- **Source** : [à obtenir — Axelys, cabinet d'évaluation PI]
- **Statut** : [SCÉN]
- **Condition d'arrêt** : si un rapport d'évaluation PI est obtenu.

---

## Constante 5 — Valeur PI totale

- **Définition** : valeur estimée du portefeuille de propriété intellectuelle.
- **Valeur** : 4,00 M$
- **Règle** : multipliée par la quote-part du pilote (2,5/4,5) → 2,22 M$.
- **Exemple** : `(2.5 / 4.5) * 4.00 = 2.22`
- **Anti-exemple** : ce n'est PAS le coût d'acquisition (voir constante 4).
- **Source** : [à obtenir — méthode du coût de remplacement ou DCF]
- **Statut** : [SCÉN]
- **Condition d'arrêt** : si un évaluateur indépendant produit une valeur différente.

---

## Récapitulatif du calcul

economies_10ans = 0,81 × 2         = 1,62 M$
part_robotique  = (2,5/8,0) × 6,40 = 2,00 M$
part_PI         = (2,5/4,5) × 4,00 = 2,22 M$
                                  ─────────
valeur_creee                       = 5,84 M$

coût_total (phase 5)               = 2,50 M$

D = 5,84 / 2,50                    = 2,337

---

## Règle éditoriale

Tant que les 5 constantes ne sont pas sourcées, le ratio D = 2,337 doit porter le marqueur [P] dans toute communication publique.

---

## Prochaines actions

1. Contacter 2-3 intégrateurs robotiques (devis formels)
2. Contacter Investissement Québec
3. Contacter Axelys (évaluation PI)
4. Mettre à jour ce document
5. Recalculer D
