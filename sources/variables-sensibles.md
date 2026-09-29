# Variables sensibles — Registre de mise à jour

Ce document recense les chiffres du dossier qui changent avec le temps.
Il doit être mis à jour à chaque nouveau budget, élection, ou changement légal.

## 1. Variables macroéconomiques (trimestriel)

**Dernière mise à jour** : 2026-09-29


| Variable | Valeur actuelle | Source | Utilisée dans |
|---|---|---|---|
| Croissance PIB (g) | 1,1 % [M] | Finances Québec | moteur_domar.py |
| Taux d'intérêt effectif (r) |   3.96 % | Finances Québec | moteur_domar.py |
| Inflation observée (IPC 12 mois) |   3.03 % | Statistique Canada | Tous |
| Cible d'inflation BdC | 2,0 % [C] | Banque du Canada | moteur_domar.py |
| Taux de change CAD/USD |   1.4188 | Banque du Canada | NARP, importations |
| Taux directeur |  2.25 % | Banque du Canada | moteur_domar.py |
| Ratio dette/PIB |   44.6 % | Finances Québec | moteur_domar.py |
| Dette brute (G$) |   262.871 G$ | Finances Québec (2024-2025) | moteur_domar.py |

## 2. Variables fiscales (annuel)

**Dernière mise à jour** : 2026-09-29


| Variable | Valeur actuelle | Source | Utilisée dans |
|---|---|---|---|
| A0 (revenu imposable agrégé) | 372,261 G$ [M] | Revenu Québec | moteur_fiscal.py |
| R_OBS (impôt à payer) | 40,79 G$ [M] | Revenu Québec | moteur_fiscal.py |
| T_REF (taux effectif) | 10,96 % [C] | Calculé | moteur_fiscal.py |

## 3. Variables budgétaires (annuel)

**Dernière mise à jour** : 2026-09-29


| Variable | Valeur actuelle | Source | Utilisée dans |
|---|---|---|---|
| Enveloppe FQBC | 8,40 G$ [P] | Livre II | Tout |
| Scénarios A/B/C | 9,63 / 8,40 / 5,14 | Livre II | Tout |
| Portefeuille 17 projets | 12,090 G$ [P] | Livre III | Tout |
| Dépassements observés | SIFA, REM, tramway | Médias | depassements-couts.html |

## 4. Variables de marché (continu)

**Dernière mise à jour** : 2026-09-29


| Variable | Valeur actuelle | Source | Utilisée dans |
|---|---|---|---|
| Prix batteries | [P] | Marché | moteur_vehicule.py |
| Prix essence | Variable | Régie | moteur_vehicule.py |
| Coût transport | Variable | Marché | Monte-Carlo |
| Prix logement | Variable | ISQ | classe-moyenne.html |

## 5. Variables légales (réforme)

**Dernière mise à jour** : 2026-09-29


| Variable | Valeur actuelle | Source | Utilisée dans |
|---|---|---|---|
| Plafond DGEQ | 100 $ / 200 $ | DGEQ | moteur_dgeq.py |
| Seuil comptant | 50 $ | DGEQ | moteur_dgeq.py |
| Sanctions Loi 29 | 5 % du CA | Loi 29 | obsolescence |
| Garanties Loi 29 | 3 à 6 ans | Loi 29 | obsolescence |

## 6. Variables de projet (par projet)

**Dernière mise à jour** : 2026-09-29


| Variable | Valeur actuelle | Source | Utilisée dans |
|---|---|---|---|
| Coût pilote véhicule | 25 M$ [P] | Mobilite | moteur_vehicule.py |
| Économies exploitation | 0,81 M$ [T] | Étude | moteur_vehicule.py |
| Triangle provisionnement | [P] | Exemple | moteur_provisionnement.py |

## Prochaine mise à jour

- Budget du Québec 2027 : toutes les variables macro
- Élections 2026 : variables budgétaires et légales
- Chaque projet : variables de projet

## 7. Variables de contexte (mensuel)

**Dernière mise à jour** : 2026-09-29

| Variable | Valeur actuelle | Source | Utilisée dans |
|---|---|---|---|
| Prix essence ordinaire (Québec) | 1,93 $/L (Sherbrooke, 2026-09-29) | Observation directe | contexte macro, dossier véhicule |
| Indice boursier S&P/TSX | à saisir manuellement | Bourse de Toronto | contexte macro |

**Note** : ces variables ne sont pas collectées automatiquement. Les séries StatCan correspondantes sont soit inactives (prix essence, série 735059 arrêtée), soit d'accès non fiable (bourse, HTTP 406). Mise à jour mensuelle manuelle recommandée.
