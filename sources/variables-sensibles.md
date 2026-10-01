# Variables sensibles — Registre de mise à jour

Ce document recense les chiffres du dossier qui changent avec le temps.
Il doit être mis à jour à chaque nouveau budget, élection, ou changement légal.

## 1. Variables macroéconomiques (trimestriel)

**Dernière mise à jour** : 2026-10-01


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

**Dernière mise à jour** : 2026-10-01


| Variable | Valeur actuelle | Source | Utilisée dans |
|---|---|---|---|
| A0 (revenu imposable agrégé) | 372,261 G$ [M] | Revenu Québec | moteur_fiscal.py |
| R_OBS (impôt à payer) | 40,79 G$ [M] | Revenu Québec | moteur_fiscal.py |
| T_REF (taux effectif) | 10,96 % [C] | Calculé | moteur_fiscal.py |

## 3. Variables budgétaires (annuel)

**Dernière mise à jour** : 2026-10-01


| Variable | Valeur actuelle | Source | Utilisée dans |
|---|---|---|---|
| Enveloppe FQBC | 8,40 G$ [P] | Livre II | Tout |
| Scénarios A/B/C | 9,63 / 8,40 / 5,14 | Livre II | Tout |
| Portefeuille 17 projets | 12,090 G$ [P] | Livre III | Tout |
| Dépassements observés | SIFA, REM, tramway | Médias | depassements-couts.html |

## 4. Variables de marché (continu)

**Dernière mise à jour** : 2026-10-01


| Variable | Valeur actuelle | Source | Utilisée dans |
|---|---|---|---|
| Prix batteries | [P] | Marché | moteur_vehicule.py |
| Prix essence | Variable | Régie | moteur_vehicule.py |
| Coût transport | Variable | Marché | Monte-Carlo |
| Prix logement | Variable | ISQ | classe-moyenne.html |

## 5. Variables légales (réforme)

**Dernière mise à jour** : 2026-10-01


| Variable | Valeur actuelle | Source | Utilisée dans |
|---|---|---|---|
| Plafond DGEQ | 100 $ / 200 $ | DGEQ | moteur_dgeq.py |
| Seuil comptant | 50 $ | DGEQ | moteur_dgeq.py |
| Sanctions Loi 29 | 5 % du CA | Loi 29 | obsolescence |
| Garanties Loi 29 | 3 à 6 ans | Loi 29 | obsolescence |

## 6. Variables de projet (par projet)

**Dernière mise à jour** : 2026-10-01


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

**Dernière mise à jour** : 2026-10-01

| Variable | Valeur actuelle | Source | Utilisée dans |
|---|---|---|---|
| Prix essence ordinaire (Québec) | 1,93 $/L (Sherbrooke, 2026-09-29) | Observation directe | contexte macro, dossier véhicule |
| Indice boursier S&P/TSX | à saisir manuellement | Bourse de Toronto | contexte macro |

**Note** : ces variables ne sont pas collectées automatiquement. Les séries StatCan correspondantes sont soit inactives (prix essence, série 735059 arrêtée), soit d'accès non fiable (bourse, HTTP 406). Mise à jour mensuelle manuelle recommandée.

---

## 8. Données de contexte ISQ (annuel)

**Dernière mise à jour** : 2026-10-01
**Source** : ISQ, *Le Québec chiffres en main*, édition 2026
**Mise à jour** : annuelle, à la parution de la nouvelle édition
**Usage** : ces données ne sont pas des hypothèses de calcul. Ce sont des faits mesurés par un organisme indépendant. Ils servent à fixer des cibles politiques mesurables et à porter les enjeux du Québec devant la population.

**Pourquoi elles comptent** : ces chiffres décrivent des réalités vécues par les Québécois — vieillissement, accès aux soins, écart de revenus entre régions, crise du logement. Ce sont des enjeux auxquels le PMDQ accorde une attention particulière. Nous nous battrons pour les gens concernés par ces réalités, pas seulement pour des principes.

Toutes les valeurs sont **[M]** (mesurées).

### Démographie
| Variable | Valeur | Année |
|---|---:|---:|
| Population totale | 9 058 297 | 2025 |
| Accroissement naturel | −2 250 | 2025 |
| Solde migratoire international | +466 | 2025 |
| Solde résidents non permanents | −51 413 | 2025 |
| Âge médian | 42,8 ans | 2025 |
| Personnes 65 ans et + | 1 089 833 | 2025 |
| Indice de fécondité | 1,36 | 2025 |

### Santé
| Variable | Valeur | Année |
|---|---:|---:|
| Médecins pour 1 000 hab. | 2,38 | 2024 |
| Lits soins physiques pour 1 000 | 1,78 | 2025 |
| Lits soins longue durée pour 1 000 | 4,26 | 2025 |
| Dépenses santé (G$) | 84,4 | 2025 |
| Dépenses santé (% PIB) | 13,5 | 2025 |
| Taux d'hébergement 65+ | 2,4 % | 2025 |
| Consommation cannabis 15-20 ans | 16,9 % | 2025 |

### Éducation
| Variable | Valeur | Année |
|---|---:|---:|
| Diplômations secondaire | 146 629 | 2025 |
| Accès au collégial | 66,6 % | 2024-25 |
| Accès à l'université | 48,6 % | 2024-25 |
| Étudiants internationaux | 50 661 | automne 2025 |
| Dépense par élève prim-sec | 19 112 $ | 2023-24 |
| Droits scolarité 1er cycle (QC) | 3 963 $ | 2025-26 |
| Droits scolarité 1er cycle (ON) | 8 958 $ | 2025-26 |

### Économie et finances
| Variable | Valeur | Année |
|---|---:|---:|
| PIB réel (croissance) | +0,6 % | 2025 |
| PIB par hab. PPA | 59 597 $ US | 2024 |
| Taux de chômage | 5,6 % | 2025 |
| Taux d'activité | 64,9 % | 2025 |
| Revenu disponible par hab. | 38 426 $ | 2024 |
| Salaire minimum | 16,10 $ | 2025 |
| Investissements totaux | 65,7 G$ | 2025 |
| Exportations | 121,6 G$ | 2025 |

### Environnement et énergie
| Variable | Valeur | Année |
|---|---:|---:|
| Aires protégées | 16,53 % | 2026 |
| Émissions GES (Mt éq. CO₂) | 78,0 | 2023 |
| Transport (% des GES) | 34,9 | 2023 |
| Industries (% des GES) | 24,7 | 2023 |
| Matières résiduelles par hab. | 685 kg | 2023 |
| Recyclage organique | 64 % | 2023 |
| Production électricité hydraulique | 93,9 % | 2025 |

### Logement et conditions de vie
| Variable | Valeur | Année |
|---|---:|---:|
| Logements mis en chantier | 59 864 | 2025 |
| Valeur unifamiliale | 499 250 $ | 2026 |
| Valeur copropriété | 453 725 $ | 2026 |
| Ménages à faible revenu | 14,2 % | 2023 |
| Prestataires aide sociale | 343 883 | 2025 |
| Allocation moyenne | 1 122,89 $ | 2025 |

### Régions
| Région | Population 2025 | Chômage 2025 | Revenu disp./hab. 2024 |
|---|---:|---:|---:|
| Montréal | 2 172 259 | 8,0 % | 39 061 $ |
| Québec (Capitale-Nationale) | 814 004 | 4,3 % | 39 597 $ |
| Montérégie | 1 522 372 | 4,6 % | 39 798 $ |
| Estrie | 527 340 | 4,9 % | 38 047 $ |
| Bas-Saint-Laurent | 204 755 | 5,0 % | 35 024 $ |
| Abitibi-Témiscamingue | 149 441 | 3,9 % | 38 890 $ |
| Côte-Nord | 89 291 | 4,3 % | 39 160 $ |
| Gaspésie–Îles-de-la-Madeleine | 92 084 | — | — |

### Note d'usage
Pas d'API ISQ publique. Mise à jour manuelle annuelle. Si une nouvelle édition sort, comparer ligne par ligne et mettre à jour uniquement les valeurs qui ont changé — ne pas tout réécrire.
