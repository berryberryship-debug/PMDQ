# 07 — LIVRE IV
## Simulateur budgétaire (réserve 15 %)

Version : PMDQ v2.7.1 — 22 septembre 2026.

## 1. Règle appliquée

Réserve_t = 0,15 × ( R_admissible_t + Report_{t-1} ) pour t ∈ {1, 2, 3}
Réserve_4 = 0

Décaissement net : Δ_net_t = min( Π_t, R_admissible_t + Report_{t-1} − Réserve_t )

## 2. Tableau d'exécution (scénario B central)

| Exercice | R_adm | Report | Assiette | Réserve | Plafond | Prévu | Décaissé | Susp. |
|---|---|---|---|---|---|---|---|---|
| An 1 | 2,100 | 0,000 | 2,100 | 0,315 | 1,785 | 1,600 | 1,600 | 0,000 |
| An 2 | 2,100 | 0,185 | 2,285 | 0,343 | 1,942 | 2,400 | 1,942 | 0,458 |
| An 3 | 2,100 | 0,000 | 2,100 | 0,315 | 1,785 | 2,600 | 1,785 | 0,815 |
| An 4 | 2,100 | 0,000 | 2,100 | 0,000 | 2,100 | 1,800 | 1,800 | 0,000 |
| **Total** | **8,400** | — | — | **0,973** | — | **8,400** | **7,127** | **1,273** |

## 3. Taux d'exécution

Taux = 7,127 / 8,400 = 84,85 %

## 4. Lecture

- Suspensions cumulées : 0,458 + 0,815 = 1,273 G$
- Réserve libérée en fin de mandat : 0,973 G$
- Reliquat final reversé au Fonds consolidé : 0,300 G$

## 5. Convention d'arrondi

Mode documentaire : réserve arrondie à 0,001 G$ avant calcul du plafond.
Mode normatif exact : calcul sans arrondi intermédiaire.

Mode retenu : documentaire (permet la reproduction exacte).

## 6. Vérification arithmétique

| Contrôle | Valeur | Résultat |
|---|---|---|
| Somme enveloppe 4 ans | 4 × 2,100 | 8,400 ✓ |
| Somme prévu 4 ans | 1,600 + 2,400 + 2,600 + 1,800 | 8,400 ✓ |
| Somme décaissé 4 ans | 1,600 + 1,942 + 1,785 + 1,800 | 7,127 ✓ |
| Taux d'exécution | 7,127 / 8,400 | 84,85 % ✓ |
