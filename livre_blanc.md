# PMDQ — Livre blanc

**Version du socle** : v2.7.22
**Date de generation** : 2026-09-29
**Origine** : genere automatiquement depuis les moteurs et les caches de donnees

---


## Resume executif

Le socle PMDQ compte actuellement :

- **7 sections** de variables sensibles suivies
- **7 sections a jour**, 0 en retard, 0 a revoir
- **9 sources economiques officielles** collectees automatiquement
- **2 observations manuelles** enregistrees

**Aucune alerte** : toutes les sections sont a jour.


## References economiques officielles

| Cle | Valeur | Unite | Date observation | Source |
|---|---:|---|---|---|
| depenses totales quebec | 161.26 | G$ | 2024-2025 | Comptes publics Quebec vol.1 (donneesquebec.ca) |
| dette brute quebec | 44.6 | G$ | 2024-2025 | Finances Quebec (via donneesquebec.ca) |
| impot particuliers quebec | 44.7 | G$ | 2024-2025 | Finances Quebec (revenus, via donneesquebec.ca) |
| ipc canada | 169.8 | indice (2002=100) | 2026-08-01 | Statistique Canada (18-10-0004-01) |
| revenus totaux quebec | 156.09 | G$ | 2024-2025 | Comptes publics Quebec vol.1 (donneesquebec.ca) |
| taux change usd cad | 1.4188 | CAD par USD | 2026-09-29 | Banque du Canada |
| taux directeur | 2.25 | % | 2026-09-28 | Banque du Canada |
| taux inflation annuel | 3.03 | % | 2026-08-01 | Statistique Canada (IPC 12 mois) |
| taux obligations 10ans | 3.96 | % | 2026-09-28 | Banque du Canada |


## Observations manuelles

### prix essence quebec

| Date | Valeur | Unite | Lieu |
|---|---:|---|---|
| 2026-09-29 | 1.93 | $/L | Sherbrooke |
| 2026-09-29 | 1.92 | $/L | Magog |


## Analyses par moteur

### Variables sensibles

```

==========================================================================================
  MOTEUR VARIABLES SENSIBLES - PMDQ v2.7.7
==========================================================================================
  Date d'analyse      : 2026-09-29
  mtime du registre   : 2026-09-29

  Section                                              MAJ   Ecart   Freq             Statut
  ----------------------------------------------------------------------------------------
  1. Variables macroeconomiques                 2026-09-29     0 j    90 j             A JOUR
  2. Variables fiscales                         2026-09-29     0 j   365 j             A JOUR
  3. Variables budgetaires                      2026-09-29     0 j   365 j             A JOUR
  4. Variables de marche                        2026-09-29     0 j    30 j             A JOUR
  5. Variables legales                          2026-09-29     0 j   365 j             A JOUR
  6. Variables de projet                        2026-09-29     0 j   180 j             A JOUR
  7. Variables de contexte                      2026-09-29     0 j    30 j             A JOUR

  Detail des sources de date :
    - 1. Variables macroeconomiques          : date explicite (2026-09-29)
    - 2. Variables fiscales                  : date explicite (2026-09-29)
    - 3. Variables budgetaires               : date explicite (2026-09-29)
    - 4. Variables de marche                 : date explicite (2026-09-29)
    - 5. Variables legales                   : date explicite (2026-09-29)
    - 6. Variables de projet                 : date explicite (2026-09-29)
    - 7. Variables de contexte               : date explicite (2026-09-29)
References economiques officielles disponibles :
    - taux change usd cad              1.4188 CAD par USD (2026-09-29) - Banque du Canada
    - taux directeur                   2.25 % (2026-09-28) - Banque du Canada
    - taux obligations 10ans           3.96 % (2026-09-28) - Banque du Canada
    - ipc canada                       169.8 indice (2002=100) (2026-08-01) - Statistique Canada (18-10-0004-01)
    - taux inflation annuel            3.03 % (2026-08-01) - Statistique Canada (IPC 12 mois)
    - dette brute quebec               44.6 G$ (2024-2025) - Finances Quebec (via donneesquebec.ca)
    - impot particuliers quebec        44.7 G$ (2024-2025) - Finances Quebec (revenus, via donneesquebec.ca)
    - depenses totales quebec          161.26 G$ (2024-2025) - Comptes publics Quebec vol.1 (donneesquebec.ca)
    - revenus totaux quebec            156.09 G$ (2024-2025) - Comptes publics Quebec vol.1 (donneesquebec.ca)
Observations manuelles :
    - prix essence quebec              1.92 $/L (2026-09-29) (Magog)  [2 observations]



==========================================================================================
```

### Dynamique de la dette

```
========================================================================
MOTEUR DOMAR — PMDQ v2.7.7 (cohérent avec le Livre V)
========================================================================
d (dette brute / PIB) : 42.3 % [code]
PIB implicite 2026    : 644.55 G$ [C]

Scénario               i        g      i-g   s* (% PIB)      s* (G$)
------------------------------------------------------------------------
Favorable          4.00 %    3.20 %    0.80 %      0.328 %       2.11 G$
Central            4.60 %    2.71 %    1.89 %      0.778 %       5.02 G$
Défavorable        5.50 %    1.80 %    3.70 %      1.537 %       9.91 G$

  --- References officielles disponibles ---
  Dette brute / PIB (officiel) : 44.6 %  (2024-2025)
  Source                       : Finances Quebec (via donneesquebec.ca)
  Code utilise                 : 42.3 %
  ECART                        : 2.3 points

========================================================================
TRAJECTOIRES SUR 25 ANS — effort fixe = 5,29 G$/an
========================================================================
  Favorable       → d(25 ans) =   36.6 %  (baisse)
  Central         → d(25 ans) =   48.7 %  (explose)
  Défavorable     → d(25 ans) =   77.8 %  (explose)

Résultats sauvegardés : sources/domar_topologie.json
```

### Dynamique de la dette (officiel)

```
========================================================================
MOTEUR DOMAR — PMDQ v2.7.7 (cohérent avec le Livre V)
========================================================================
d (dette brute / PIB) : 44.6 % [cache (2024-2025)]
PIB implicite 2026    : 644.55 G$ [C]

Scénario               i        g      i-g   s* (% PIB)      s* (G$)
------------------------------------------------------------------------
Favorable          4.00 %    3.20 %    0.80 %      0.346 %       2.23 G$
Central            4.60 %    2.71 %    1.89 %      0.821 %       5.29 G$
Défavorable        5.50 %    1.80 %    3.70 %      1.621 %      10.45 G$

  --- References officielles disponibles ---
  Dette brute / PIB (officiel) : 44.6 %  (2024-2025)
  Source                       : Finances Quebec (via donneesquebec.ca)
  Code utilise                 : 44.6 % (coherent)

========================================================================
TRAJECTOIRES SUR 25 ANS — effort fixe = 5,29 G$/an
========================================================================
  Favorable       → d(25 ans) =   38.5 %  (baisse)
  Central         → d(25 ans) =   51.4 %  (explose)
  Défavorable     → d(25 ans) =   82.0 %  (explose)

Résultats sauvegardés : sources/domar_topologie.json
```

### Analyse fiscale

```

=================================================================
  MOTEUR FISCAL — PMDQ v2.7.7 (Module 7)
=================================================================

  --- Point de calibration (Quebec 2023) ---
  A0_G (revenu imposable)     : 372.261 G$
  T_REF (taux effectif)       : 10.96 %
  R_OBS (imput a payer)       : 40.79 G$
  EPSILON (scenaristique)     : 0.4

  --- Reforme simulee ---
  Taux nouveau                : 15.00 %
  Assiette nouvelle           : 338.892 G$
  Recettes nouvelles          : 50.834 G$
  Variation vs 2023           : +10.044 G$

  FQBC (9 %)         : 5.083 G$
  Etat net                    : 45.75 G$

=================================================================

  --- References officielles disponibles ---
  Impot des particuliers (officiel) : 44.7 G$  (2024-2025)
  Source                            : Finances Quebec (revenus, via donneesquebec.ca)
  Code utilise (R_OBS)              : 40.79 G$  (calibration 2023)
  Ecart brut                        : 3.91 G$
  Note : les annees different (2023 code, 2024-2025 officiel).

  --- Projection 2024-2025 (cache officiel) ---
  Source                          : Finances Quebec (revenus, via donneesquebec.ca)
  Base de calibration             : 2023 (A0_G = 372.261 G$)
  Impot officiel (2024-2025)       : 44.7 G$
  T_REF calibre 2023              : 10.96 %
  T_REF projete (A0_G constant)   : 12.01 %
  Ecart de taux                   : +1.05 points
  Note : projection indicative.
         Le T_REF reel de 2024-2025 exigerait le A0_G de 2024-2025.
```

### Etancheite budgetaire

```
========================================================================
MOTEUR D'ÉTANCHÉITÉ BUDGÉTAIRE — PMDQ v2.7.7
========================================================================

--- Topologie du graphe ---
  Nœuds       : 6
  Arêtes      : 4
  Sources     : R, Ré, É, Co
  Destinations: Décaissements, Réserve de contingence

--- Assiette exécutoire (Article 14) ---
  R + Ré + É  : 7.71 G$
  Co (exclu)  : 0.69 G$
  Total flux  : 8.40 G$

--- Violations structurelles ---
  ✅ Aucune violation détectée.

--- Anomalies financières déclarées ---
  FIN-001 — 0.85 G$ — Pénalités É-04 + É-05 mal classées en É
     Devrait être classé en : Co
  FIN-002 — 0.09 G$ — Double comptage MSSS/MCN

--- Assiette exécutoire corrigée (si FIN-001 résolu) ---
  Avant correction : 7.71 G$
  Après correction : 6.86 G$
  Impact           : -0.85 G$

Rapport sauvegardé : sources/etancheite_budgetaire.json

--- Test de robustesse du moteur ---
✅ Test de robustesse : violation correctement détectée.
   {'type': 'arête_interdite', 'source': 'Co', 'destination': 'Décaissements', 'regle': 'Article 14 — ressources admissibles'}
```

### Provisionnement actuariel

```
========================================================================
MOTEUR DE PROVISIONNEMENT ACTUARIEL — PMDQ v2.7.7
========================================================================
Taux de précaution (Article 13) : 15.0 %
Seuil de confiance bootstrap    : 95 %
Simulations Monte-Carlo         : 10000

--- 1. Triangle de développement ---
[[1.   1.5  1.8  1.95 2.  ]
 [1.1  1.65 1.95 2.1   nan]
 [1.2  1.8  2.1   nan  nan]
 [1.15 1.7   nan  nan  nan]
 [1.3   nan  nan  nan  nan]]

Facteurs de développement : [1.4944, 1.1818, 1.08, 1.0256]

--- 2. Triangle projeté ---
[[1.    1.5   1.8   1.95  2.   ]
 [1.1   1.65  1.95  2.1   2.154]
 [1.2   1.8   2.1   2.268 2.326]
 [1.15  1.7   2.009 2.17  2.225]
 [1.3   1.943 2.296 2.48  2.543]]

--- 3. Réserves par année de survenance (G$) ---
  Année 1 : 0.000 G$
  Année 2 : 0.054 G$
  Année 3 : 0.226 G$
  Année 4 : 0.525 G$
  Année 5 : 1.243 G$
  TOTAL    : 2.049 G$

--- 4. Erreur-type de Mack ---
  σ (approximation) : 0.455 G$

--- 5. Bootstrap (n=10000) ---
  Réserve médiane : 1.975 G$
  IC 95 % bas     : 0.334 G$
  IC 95 % haut    : 4.255 G$

--- 6. Réserve de précaution (Article 13) ---
  Plafond           : 8.40 G$
  Ressources prévues: 7.71 G$
  Écart             : 0.69 G$
  Réserve (15 %)    : 0.104 G$

--- 7. Réserve de contingence (Article 15) ---
  Revenus conditionnels (Co) : 0.69 G$
  Alimentation réserve       : 0.69 G$ (100 % de Co)

Rapport sauvegardé : sources/provisionnement_topologie.json
```

### Rendement

```
========================================================================
MOTEUR DE RENDEMENT D — PMDQ v2.7.7
========================================================================
Taux d'actualisation social : 3.5 % [T]
Seuil D (Article 18)        : 1.3 [M]

Projet                                         Cat.   VAN (G$)       D       Statut
----------------------------------------------------------------------------------
Plantation d'arbres — 20 quartiers                É       1.63    1.71     CONFORME
MOD-ECO-CIRC-2025                                 É       9.21    2.54     CONFORME
Mobilité urbaine — prototype                     Co          —       —        EXCLU

========================================================================
TEST DE SENSIBILITÉ AU TAUX D'ACTUALISATION
========================================================================
Projet                                            2.0 %     3.5 %     5.0 %     7.0 %
----------------------------------------------------------------------------------
Plantation d'arbres — 20 quartiers               1.85    1.71    1.59    1.45
MOD-ECO-CIRC-2025                                2.61    2.54    2.46    2.38

Note : le seuil D > 1,30 doit être atteint pour tout projet admissible.
       Les catégories Co sont automatiquement exclues.

Rapport sauvegardé : sources/rendement_topologie.json
```

### Analyse vehicule

```
======================================================================
  MOTEUR VEHICULE — PMDQ v2.7.7 — Module 5
======================================================================

--- 1. Enveloppe budgetaire ---
  Total calcule : 25.0 M$
  Total attendu : 25.0 M$
  Statut : OK

--- 2. Service de la dette ---
  Principal : 25.0 M$
  Taux : 4.00 %
  Annuite : 5.616 M$/an
  Total rembourse : 28.078 M$
  Interets cumules : 3.078 M$

--- 3. Ratio de rendement collectif D ---
  Valeur creee : 11.21 M$
  Cout total : 25.0 M$
  Ratio D : 0.448
  Seuil : 1.3
  Statut : REJETE

--- 4. Impact Domar (Livre V) ---
  Dette ajoutee : 0.025 G$
  PIB Quebec : 644.55 G$
  Impact : 0.00388 % du PIB
  Statut : [C] marginal

--- 5. Etancheite budgetaire (Article 14) ---
  Categories : Co, E, R, Re
  Co present : True
  Note : Les categories Co sont exclues de l'assiette executoire.

======================================================================

Rapport sauvegarde : sources/vehicule_topologie.json

======================================================================
  SCENARIOS D'ENVELOPPE — Recherche du seuil D > 1,30
======================================================================

  Valeur creee (benefices documentes) : 11.21 M$
  Seuil requis : D > 1.3
  Enveloppe maximale pour D = 1,30 : 8.623 M$

     Enveloppe    Ratio D       Statut
  ------------------------------------
       25.00 M$      0.448       REJETE
       22.00 M$      0.510       REJETE
       20.00 M$      0.560       REJETE
       18.00 M$      0.623       REJETE
       15.00 M$      0.747       REJETE
       12.00 M$      0.934       REJETE
       11.12 M$      1.008       REJETE

  Note : les phases sont reduites proportionnellement dans chaque scenario.
======================================================================

======================================================================
  REQUALIFICATION — DEUX REGIMES DISTINCTS
======================================================================

  Regime 1 - R&D et capacites (phases 1-4)
    Montant  : 22.5 M$
    Critere  : Creation d'actifs immateriels + capacites documentees
    Statut   : [T] - Investissement en capacites industrielles

  Regime 2 - Pilote industriel (phase 5)
    Montant  : 2.5 M$
    Critere  : Ratio D > 1,30 sur horizon 10 ans
    Statut   : [P] - Decision d'industrialisation

  --- Regime 2 — Calcul du ratio D sur 10 ans ---
    Economies (10 ans) : 1.62 M$
    Part robotique     : 2.0 M$
    Part PI            : 2.22 M$
    Valeur creee       : 5.84 M$
    Cout total         : 2.5 M$
    Ratio D            : 2.337 (CONFORME)

  Note : le seuil D > 1,30 s'applique au pilote industriel,
         pas a l'investissement en capacites R&D.
======================================================================
```

### Coherence inter-moteurs

```

==============================================================================
  MOTEUR COHERENCE INTER-MOTEURS — PMDQ v2.7.7
==============================================================================
  Date : 2026-09-29

  Regle                               Statut             Detail
  --------------------------------------------------------------------------
  Presence domar                      OK                 830 octets
  Presence etancheite                 OK                 668 octets
  Presence provisionnement            OK                 573 octets
  Presence rendement                  OK                 747 octets
  Presence vehicule                   OK                 2283 octets
  PIB 2026                            NON VERIFIABLE     Aucune valeur trouvee
  Dette initiale (domar)              ABSENTE            Cle introuvable
  Cles domar                          OK                 1 cle(s) attendue(s) presente(s)

  Bilan : 8 regles, 6 OK, 0 alerte(s)
==============================================================================
```

### Ecarts registre / officiel

```

==============================================================================
  MOTEUR ECARTS REGISTRE / CACHE OFFICIEL — PMDQ v2.7.10
==============================================================================
  Date : 2026-09-29

  Variable                               Declare   Officiel    Ecart Statut         
  --------------------------------------------------------------------------
  Taux d'intérêt effectif (r)         [T] à déte       2.25        - NON NUMERIQUE  
  Inflation                                  2.0       3.03     1.03 ECART          
  Taux de change CAD/USD                Variable     1.4188        - NON NUMERIQUE  

  Bilan : 3 comparees, 0 OK, 1 ecart(s), 2 non verifiable(s)
==============================================================================
```

### Nomenclature vehicule biplace

```

==============================================================================
  NOMENCLATURE — Scenario C - Milieu ferme (v0.1)
==============================================================================
  Composants             : 35
  Cout prototype         :    32,240.00 $
  Part quebecoise        :    22,607.00 $ (70.1 %)

  Volume cible serie     : 10
  Cout unitaire serie    :    25,604.00 $
  Marge                  : 25 %
  Prix de vente unitaire :    32,005.00 $
  Revenu serie           :   320,050.00 $
  Cout serie total       :   256,040.00 $

  Ventilation par sous-systeme :
    Sous-systeme             Cout ($)  Part QC ($)   Nb
    ----------------------------------------------------
    Assemblage              12,000.00    12,000.00    3
    Structure                6,350.00     5,080.00    4
    Propulsion               3,000.00     1,120.00    4
    Mecanique                2,860.00       596.00    6
    Batterie                 2,800.00     1,245.00    4
    Interieur                2,100.00     1,060.00    3
    Electrique               1,250.00       405.00    4
    Finition                 1,050.00       680.00    3
    Securite                   830.00       421.00    4

==============================================================================
```


## Journal du socle

```
2026-09-29 15:47 — SOCLE v2.7.7
  Variables : 6/6 A JOUR
  Moteurs   : 8/8 OK
  Commit    : 9160648

2026-09-29 15:48 — SOCLE v2.7.7
  Variables : 6/6 A JOUR
  Moteurs   : 8/8 OK
  Commit    : 9160648

2026-09-29 15:49 — SOCLE v2.7.7
  Variables : 6/6 A JOUR
  Moteurs   : 8/8 OK
  Commit    : a5da8ab

2026-09-29 15:49 — SOCLE v2.7.7
  Variables : 6/6 A JOUR
  Moteurs   : 8/8 OK
  Commit    : a5da8ab

2026-09-29 15:54 — SOCLE v2.7.7
  Variables : 6/6 A JOUR
  Moteurs   : 8/8 OK
  Commit    : a5da8ab

2026-09-29 16:03 — SOCLE v2.7.7
  Variables : 6/6 A JOUR
  Moteurs   : 8/8 OK
  Commit    : a5da8ab

2026-09-29 16:06 — SOCLE v2.7.7
  Variables : 6/6 A JOUR
  Moteurs   : 9/9 OK
  Commit    : ee55128

2026-09-29 16:07 — SOCLE v2.7.7
  Variables : 6/6 A JOUR
  Moteurs   : 9/9 OK
  Commit    : ee55128

2026-09-29 16:13 — SOCLE v2.7.7
  Variables : 6/6 A JOUR
  Moteurs   : 9/9 OK
  Commit    : 73a372e

2026-09-29 16:14 — SOCLE v2.7.7
  Variables : 6/6 A JOUR
  Moteurs   : 9/9 OK
  Commit    : 73a372e

2026-09-29 16:20 — SOCLE v2.7.7
  Variables : 6/6 A JOUR
  Moteurs   : 9/9 OK
  Commit    : 4774efa

2026-09-29 16:20 — SOCLE v2.7.7
  Variables : 6/6 A JOUR
  Moteurs   : 9/9 OK
  Commit    : 4774efa

2026-09-29 16:23 — SOCLE v2.7.7
  Variables : 6/6 A JOUR
  Moteurs   : 10/10 OK
  Commit    : cbd4fcc

2026-09-29 16:24 — SOCLE v2.7.7
  Variables : 6/6 A JOUR
  Moteurs   : 10/10 OK
  Commit    : cbd4fcc

2026-09-29 16:33 — SOCLE v2.7.7
  Variables : 6/6 A JOUR
  Moteurs   : 10/10 OK
  Commit    : b911fa5

2026-09-29 16:47 — SOCLE v2.7.7
  Variables : 6/6 A JOUR
  Moteurs   : 10/10 OK
  Commit    : b911fa5

2026-09-29 16:47 — SOCLE v2.7.7
  Variables : 6/6 A JOUR
  Moteurs   : 10/10 OK
  Commit    : b911fa5

2026-09-29 16:49 — SOCLE v2.7.7
  Variables : 6/6 A JOUR
  Moteurs   : 10/10 OK
  Commit    : 0424e9a

2026-09-29 16:49 — SOCLE v2.7.7
  Variables : 6/6 A JOUR
  Moteurs   : 10/10 OK
  Commit    : 0424e9a

2026-09-29 16:53 — SOCLE v2.7.7
  Variables : 6/6 A JOUR
  Moteurs   : 10/10 OK
  Commit    : f1e4cce

2026-09-29 16:53 — SOCLE v2.7.7
  Variables : 6/6 A JOUR
  Moteurs   : 10/10 OK
  Commit    : f1e4cce

2026-09-29 16:55 — SOCLE v2.7.7
  Variables : 6/6 A JOUR
  Moteurs   : 10/10 OK
  Commit    : 6f42941

2026-09-29 16:56 — SOCLE v2.7.7
  Variables : 6/6 A JOUR
  Moteurs   : 10/10 OK
  Commit    : 6f42941

2026-09-29 17:07 — SOCLE v2.7.7
  Variables : 6/6 A JOUR
  Moteurs   : 10/10 OK
  Commit    : ec3b3aa

2026-09-29 17:07 — SOCLE v2.7.7
  Variables : 6/6 A JOUR
  Moteurs   : 10/10 OK
  Commit    : ec3b3aa

2026-09-29 17:11 — SOCLE v2.7.7
  Variables : 6/6 A JOUR
  Moteurs   : 10/10 OK
  Commit    : 2ee111e

2026-09-29 17:12 — SOCLE v2.7.7
  Variables : 6/6 A JOUR
  Moteurs   : 10/10 OK
  Commit    : 2ee111e

2026-09-29 17:13 — SOCLE v2.7.7
  Variables : 6/6 A JOUR
  Moteurs   : 10/10 OK
  Commit    : 1d50970

2026-09-29 17:14 — SOCLE v2.7.7
  Variables : 6/6 A JOUR
  Moteurs   : 10/10 OK
  Commit    : 1d50970

2026-09-29 17:23 — SOCLE v2.7.7
  Variables : 6/6 A JOUR
  Moteurs   : 10/10 OK
  Commit    : 997d6c6

2026-09-29 17:24 — SOCLE v2.7.7
  Variables : 6/6 A JOUR
  Moteurs   : 10/10 OK
  Commit    : 997d6c6

2026-09-29 17:29 — SOCLE v2.7.7
  Variables : 6/6 A JOUR
  Moteurs   : 10/10 OK
  Commit    : 7362379

2026-09-29 17:29 — SOCLE v2.7.7
  Variables : 6/6 A JOUR
  Moteurs   : 10/10 OK
  Commit    : 7362379

2026-09-29 18:00 — SOCLE v2.7.7
  Variables : 7/7 A JOUR
  Moteurs   : 10/10 OK
  Commit    : 74c6541

2026-09-29 18:00 — SOCLE v2.7.7
  Variables : 7/7 A JOUR
  Moteurs   : 10/10 OK
  Commit    : 74c6541

2026-09-29 18:03 — SOCLE v2.7.7
  Variables : 7/7 A JOUR
  Moteurs   : 10/10 OK
  Commit    : b76b103

2026-09-29 18:03 — SOCLE v2.7.7
  Variables : 7/7 A JOUR
  Moteurs   : 10/10 OK
  Commit    : b76b103

2026-09-29 18:06 — SOCLE v2.7.7
  Variables : 7/7 A JOUR
  Moteurs   : 10/10 OK
  Commit    : aca9009

2026-09-29 18:06 — SOCLE v2.7.7
  Variables : 7/7 A JOUR
  Moteurs   : 10/10 OK
  Commit    : aca9009

2026-09-29 18:07 — SOCLE v2.7.7
  Variables : 7/7 A JOUR
  Moteurs   : 10/10 OK
  Commit    : c1df9b7

2026-09-29 18:09 — SOCLE v2.7.7
  Variables : 7/7 A JOUR
  Moteurs   : 10/10 OK
  Commit    : c1df9b7

2026-09-29 18:10 — SOCLE v2.7.7
  Variables : 7/7 A JOUR
  Moteurs   : 10/10 OK
  Commit    : c1df9b7

2026-09-29 18:11 — SOCLE v2.7.7
  Variables : 7/7 A JOUR
  Moteurs   : 10/10 OK
  Commit    : a1b9149

2026-09-29 18:11 — SOCLE v2.7.7
  Variables : 7/7 A JOUR
  Moteurs   : 10/10 OK
  Commit    : a1b9149

2026-09-29 18:13 — SOCLE v2.7.7
  Variables : 7/7 A JOUR
  Moteurs   : 10/10 OK
  Commit    : 534dd7c

2026-09-29 18:14 — SOCLE v2.7.7
  Variables : 7/7 A JOUR
  Moteurs   : 11/11 OK
  Commit    : 4772a4b

2026-09-29 18:14 — SOCLE v2.7.7
  Variables : 7/7 A JOUR
  Moteurs   : 11/11 OK
  Commit    : 4772a4b

2026-09-29 18:15 — SOCLE v2.7.7
  Variables : 7/7 A JOUR
  Moteurs   : 11/11 OK
  Commit    : 3006956
```


## Sources inactives

### Series StatCan arretees

- **735059** (Prix de detail essence, Quebec) : serie non publiee depuis 2025-09. Le tableau 18-10-0001 n'est plus alimente. Remplacement : saisie manuelle.


