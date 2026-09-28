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
