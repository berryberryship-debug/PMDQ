# 09 — LIVRE VI
## Pydantic + 17 projets types + API

Version : PMDQ v2.7.1 — 22 septembre 2026.

## ModeleRatioD (Pydantic strict)

Classe ModeleRatioD avec ConfigDict :
- strict=True (interdit la coercition)
- extra=forbid (rejette champs inconnus)
- allow_inf_nan=False (bloque NaN et infinis)
- Validateur field_validator verifier_valeur_finie
- Property cout_total = cout_cycle_vie + cout_risque
- Methode evaluer_ratio = valeur_creee_nette / cout_total
- Methode statut : CONFORME si ratio > 1.30, sinon REJETE

## 7 mécanismes de protection

1. strict=True
2. extra=forbid
3. allow_inf_nan=False
4. isfinite(valeur)
5. Field(gt)/Field(ge)
6. Literal[M,C,P,T]
7. min_length/max_length

## Les 17 projets types

| # | Identifiant | VAN | CV | Risque | Ratio D | Statut |
|---|---|---|---|---|---|---|
| 1 | RESEAU-NARP-001 | 1,850 | 0,980 | 0,180 | 1,5948 | CONFORME |
| 2 | LOGEMENT-MOD-002 | 3,420 | 2,100 | 0,300 | 1,4250 | CONFORME |
| 3 | DEJEUNER-SCOL-003 | 1,780 | 1,050 | 0,150 | 1,4833 | CONFORME |
| 4 | INST-POLY-004 | 1,240 | 0,720 | 0,180 | 1,3778 | CONFORME |
| 5 | GARDE-DOM-005 | 0,980 | 0,620 | 0,080 | 1,4000 | CONFORME |
| 6 | PRIM7-006 | 0,890 | 0,540 | 0,060 | 1,4833 | CONFORME |
| 7 | CONTING-FQBC-007 | 0,640 | 0,440 | 0,010 | 1,4222 | CONFORME |
| 8 | AUTOR-FLUV-008 | 0,610 | 0,410 | 0,040 | 1,3556 | CONFORME |
| 9 | BRIG-FORET-009 | 0,560 | 0,360 | 0,040 | 1,4000 | CONFORME |
| 10 | RD-VONKARMAN-010 | 0,400 | 0,270 | 0,030 | 1,3333 | CONFORME |
| 11 | RECH-REG-011 | 0,340 | 0,220 | 0,030 | 1,3600 | CONFORME |
| 12 | URB-SOUT-012 | 0,270 | 0,180 | 0,020 | 1,3500 | CONFORME |
| 13 | COMM-AUTOG-013 | 0,190 | 0,130 | 0,020 | 1,2667 | REJETE |
| 14 | FISC-LISS-014 | 2,100 | 1,300 | 0,200 | 1,4000 | CONFORME |
| 15 | CONT-PUB-015 | 0,910 | 0,560 | 0,090 | 1,4000 | CONFORME |
| 16 | IMM-COHES-016 | 0,470 | 0,320 | 0,030 | 1,3429 | CONFORME |
| 17 | AUTOCH-PART-017 | 0,580 | 0,380 | 0,050 | 1,3488 | CONFORME |

## Statistiques

- Projets conformes : 16/17 (94,12 %)
- Somme VAN : 17,230 G$
- Somme coûts : 12,090 G$
- Écart enveloppe FQBC : +3,690 G$
- Ratio D moyen (16 conformes) : 1,4048

## Instanciation RESEAU-NARP-001

identifiant_projet=RESEAU-NARP-001
axe_rattachement=Santé
valeur_creee_nette=1_850_000_000.0
cout_cycle_vie=980_000_000.0
cout_risque=180_000_000.0
taux_actualisation=0.045
horizon_annees=10
categorie=T

Resultat : ratio 1,5948, statut CONFORME

## API de validation

- POST /api/v1/projets : JSON conforme → Ratio D + statut
- GET /api/v1/projets/{id} : identifiant → fiche complète
- GET /api/v1/portefeuille : → liste 17 projets
- GET /api/v1/audit/tests : → rapport tests
