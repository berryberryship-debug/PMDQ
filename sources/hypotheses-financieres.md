# Hypothèses financières — Note méthodologique

## Statut
Document de travail. Toutes les hypothèses sont [P] — prospectives, à valider.

## Objet
Ce document recense les hypothèses utilisées dans les modèles financiers du PMDQ, afin de permettre à un vérificateur indépendant d'en évaluer la pertinence.

## 1. Hypothèses macroéconomiques

| Paramètre | Valeur utilisée | Source / Justification | Statut |
|---|---|---|---|
| Taux d'intérêt effectif sur la dette (r) | À préciser | À documenter depuis les publications de Finances Québec | [T] |
| Taux de croissance nominale du PIB (g) | À préciser | À documenter depuis l'ISQ | [T] |
| Ratio dette brute / PIB (2026) | 42,3 % | [R1] — calculé sur dette brute / PIB implicite | [C] |
| PIB implicite dérivé | 644,55 G$ | Calculé : 272,644 / 0,423 | [C] |

## 2. Hypothèses du FQBC (Livre II)

| Paramètre | Valeur utilisée | Justification | Statut |
|---|---|---|---|
| Enveloppe FQBC | 8,40 G$ | Somme des scénarios A/B/C | [P] |
| Réaffectations (scénario B) | 5,14 G$ | À documenter par ministère | [P] |
| Économies structurelles (scénario B) | 2,57 G$ | Sous-matrice É-01 à É-06 | [P] |
| Redevances (scénario B) | 0,69 G$ | À documenter | [P] |
| Total portefeuille 17 projets | 12,090 G$ | Somme des projets | [P] |
| Écart enveloppe/portefeuille | 3,690 G$ | Statut [T] — à arbitrer | [T] |

## 3. Hypothèses Domar (Livre V)

| Paramètre | Valeur utilisée | Justification | Statut |
|---|---|---|---|
| Effort primaire minimal | 2,11 G$/an | Scénario favorable | [P] |
| Effort primaire maximal | 5,02 G$/an | Scénario défavorable | [P] |
| Horizon d'analyse | 25 ans | Standard de soutenabilité | [T] |

## 4. Hypothèses des dépassements de coûts

| Paramètre | Valeur utilisée | Justification | Statut |
|---|---|---|---|
| Malus de base | 50 % des revenus du contrat | Proposition PMDQ | [P] |
| Plafond de malus | 75 % | Limite supérieure | [P] |
| Plancher de malus | 25 % | Faute interne avérée | [P] |
| Seuil de publication | 10 % du coût initial | Palier d'alerte | [P] |
| Seuil d'audit | 20 % du coût initial | Palier d'audit | [P] |
| Seuil de taxation | 50 % du coût initial | Palier de pénalité | [P] |

## 5. Points de vigilance (relevés par un CPA)

1. **Incohérence potentielle** : le total du portefeuille (12,090 G$) dépasse l'enveloppe FQBC (8,40 G$) de 3,690 G$. Ce point est déjà documenté comme [T] dans `02_livre_II_finances.html`.
2. **Montant tronqué** : `campagne-financement.html` contient un « 000 $ » (probablement un placeholder).
3. **Dette brute vs nette** : les deux valeurs (272,644 et 250,289 G$) doivent être présentées avec leur définition précise.
4. **Absence de trésorerie réelle** : aucune transaction n'existe à ce jour, donc aucun état financier réel ne peut être produit.

## 6. Recommandations pour l'auditeur

1. Vérifier les sources [R1] et [R2] citées dans `05_livre_V_dette_domar.html`.
2. Valider les hypothèses r et g auprès de Finances Québec et de l'ISQ.
3. Confirmer la cohérence du calcul du PIB implicite (272,644 / 0,423 = 644,55).
4. Évaluer la pertinence des paliers de dépassement (10/20/50 %) contre les pratiques du Conseil du trésor.

## 7. Fichiers liés

- `02_livre_II_finances.html` — FQBC et scénarios
- `05_livre_V_dette_domar.html` — Dette et soutenabilité
- `depassements-couts.html` — Malus et paliers
- `03_livre_III_portefeuille_17_projets.html` — Portefeuille

Dernière mise à jour : 28 septembre 2026.

---

## 8. Écart historique — Trajectoires Domar (25 ans)

### 8.1 Définition de l'effort

Le moteur `moteur_domar.py` calcule l'effort primaire stabilisant selon :

    s* = [(i - g) / (1 + g)] × d

où :
- `i` = taux d'intérêt effectif
- `g` = taux de croissance **nominal** (et non réel)
- `d` = ratio dette brute / PIB

### 8.2 Valeurs d'effort confirmées

| Scénario | i | g | i - g | s* (% PIB) | Effort (G$/an) |
|---|---|---|---|---|---|
| Favorable | 4,00 % | 3,20 % | +0,80 % | 0,328 % | 2,11 |
| Central | 4,60 % | 2,71 % | +1,89 % | 0,778 % | 5,02 |
| Défavorable | 5,50 % | 1,80 % | +3,70 % | 1,537 % | 9,91 |

Ces trois valeurs sont reproduites à l'identique par le Livre V et par le moteur.

### 8.3 Méthode de calcul des trajectoires

Le moteur applique une **simulation discrète annuelle** :

    d_t = [(1 + i) / (1 + g)] × d_{t-1} − s_t
    s_t = effort_G / PIB_t
    PIB_t = PIB_0 × (1 + g)^t

L'effort est **constant en dollars** (5,02 G$/an), mais sa **fraction du PIB décroît** chaque année.

### 8.4 Résultats actuels (cohérents avec le moteur)

| Année | Favorable | Central | Défavorable |
|---|---|---|---|
| 0 | 42,3 % | 42,3 % | 42,3 % |
| 5 | 40,4 % | 42,6 % | 46,6 % |
| 10 | 38,9 % | 43,4 % | 52,1 % |
| 15 | 37,8 % | 44,7 % | 58,9 % |
| 20 | 37,0 % | 46,5 % | 67,4 % |
| 25 | **36,6 %** | **48,7 %** | **77,8 %** |

### 8.5 Ancienne méthode — écart non résolu

Une version antérieure du Livre V affichait :

| Année | Favorable | Central | Défavorable |
|---|---|---|---|
| 25 | **25,3 %** | **42,3 %** | **83,5 %** |

**Constat :** aucune formule actuellement identifiée ne reproduit exactement ces trois valeurs à partir des paramètres du moteur. L'écart peut provenir :
- d'une définition différente de l'effort (constant en % du PIB vs constant en G$),
- d'une hypothèse de `g` différente (réel vs nominal),
- d'un traitement spécifique des ajustements stock-flux (`a_t`),
- d'une erreur de calcul non documentée.

**Statut : [T] — Validation CPA requise.**

### 8.6 Action prise

Le Livre V a été harmonisé avec le moteur (36,6 / 48,7 / 77,8 %).
Les valeurs historiques (25,3 / 42,3 / 83,5 %) sont conservées dans cette note pour traçabilité.
Toute correction future doit s'appuyer sur une validation comptable indépendante.

Dernière mise à jour : 28 septembre 2026.

---


---

## 9. Moteur fiscal — Calibration et limites

### 9.1 Point de calibration (Québec, 2023)

| Paramètre | Valeur | Définition | Statut |
|---|---|---|---|
| A0_G | 372,261 G$ | Revenu imposable agrégé des particuliers | [M] |
| R_OBS | 40,790 G$ | Impôt à payer observé | [M] |
| T_REF | 10,96 % | Taux effectif agrégé (R_OBS / A0_G) | [C] |
| EPSILON | 0,40 | Paramètre de contraction de l'assiette | [P] scénaristique |
| POWER | 1,5 | Exposant de la fonction de contraction | [P] scénaristique |

### 9.2 Résultats de la courbe

| Taux | Recettes | Écart vs 2023 |
|---|---|---|
| 10,96 % (2023) | 40,79 G$ | — |
| 18,00 % (optimal) | 53,196 G$ | +12,406 G$ |
| 20,00 % | 52,126 G$ | +11,336 G$ |
| 25,00 % | 39,057 G$ | −1,733 G$ |

### 9.3 Avertissements

- **EPSILON = 0,40 est scénaristique**, pas économétrique. Il ne provient pas d'une estimation du comportement fiscal des contribuables québécois.
- Le **taux optimal (18 %)** est un **taux effectif agrégé**, pas un taux marginal. L'atteindre impliquerait de hausser les tranches marginales bien au-delà.
- Le modèle concerne **les particuliers seulement**. Les entreprises ont leur propre régime.
- **Ne pas présenter** ce résultat comme une estimation empirique du taux optimal québécois.

### 9.4 Usage du moteur

    python3 moteur_fiscal.py --courbe --taux 0.18
    python3 moteur_fiscal.py --taux 0.20 --json resultat.json


---

## Module 5 — Véhicule urbain léger : hypothèses du moteur

**Moteur associé** : `moteur_vehicule.py`
**Chiffrage technique** : `verifier_projet.py`
**Dernière mise à jour** : 2026-09-29

### Deux régimes distincts

Le projet est évalué selon deux régimes budgétaires distincts :

| Régime | Phases | Montant | Critère | Statut |
|---|---|---|---|---|
| **Régime 1 — R&D et capacités** | 1 à 4 | 22,5 M$ | Création d'actifs immatériels + capacités documentées | [T] |
| **Régime 2 — Pilote industriel** | 5 | 2,5 M$ | Ratio D > 1,30 sur horizon 10 ans | [P] D = 2,337 |

Le seuil D > 1,30 s'applique aux projets d'infrastructure et d'industrialisation. Une phase de R&D pré-industrielle est jugée différemment : création d'actifs immatériels, capacités techniques, effets structurants.

### Régime 1 — R&D et capacités (22,5 M$)

**Statut** : [T] — Investissement en capacités industrielles
**Critère** : création d'actifs immatériels + capacités documentées
**Décomposition** : à documenter — le montant est codé en dur dans `moteur_vehicule.py:249` sans ventilation visible.

### Régime 2 — Pilote industriel (2,5 M$)

**Statut** : [P] — Décision d'industrialisation
**Critère** : ratio D > 1,30 sur 10 ans

**Calcul détaillé :**

| Élément | Valeur | Formule dans le code |
|---|---|---|
| Économies d'exploitation (10 ans) | 1,62 M$ | `0,81 × 2` |
| Part robotique (quote-part) | 2,00 M$ | `(2,5 / 8,0) × 6,40` |
| Part PI (quote-part) | 2,22 M$ | `(2,5 / 4,5) × 4,00` |
| **Valeur créée totale** | **5,84 M$** | Somme |
| Coût total (phase 5) | 2,50 M$ | — |
| **Ratio D** | **2,337** | `5,84 / 2,50` |
| Seuil requis | 1,30 | Méthodologie |
| **Conforme** | ✅ | `2,337 > 1,30` |

### Hypothèses à documenter

Les constantes suivantes sont utilisées dans le calcul mais **n'ont pas de source documentée** :

| Constante | Valeur | Signification présumée | Source à établir |
|---|---|---|---|
| Économies / 5 ans | 0,81 M$ | Économies d'exploitation par période de 5 ans | ? |
| Valeur actifs robotiques | 6,40 M$ | Valeur résiduelle totale des robots | ? |
| Investissement robots total | 8,0 M$ | Base de calcul de la quote-part (2,5 / 8,0) | ? |
| Valeur PI totale | 4,00 M$ | Valeur totale de la propriété intellectuelle | ? |
| Investissement PI total | 4,5 M$ | Base de calcul de la quote-part (2,5 / 4,5) | ? |

**Action requise** : ajouter des commentaires dans `moteur_vehicule.py` justifiant ces cinq constantes, ou les remplacer par une lecture depuis `sources/cache_economique.json`.

### Articulation avec le chiffrage technique

Le chiffrage du prototype unique (480 k – 1 215 k$, voir `verifier_projet.py`) est une **étape distincte** du Régime 1.

| Élément | Prototype unique | Régime 1 (R&D) |
|---|---|---|
| Objet | Un véhicule fonctionnel | Actifs immatériels, capacités industrielles |
| Coût | 480 k – 1 215 k$ | 22,5 M$ |
| Horizon | Cycle unique | Programme pluriannuel |
| Inclus | Ingénierie, prototypage, essais | Industrialisation, PI, robotisation, formation |

Le prototype est une **condition préalable** au Régime 1 — il permet de valider la faisabilité technique avant l'engagement industriel.

