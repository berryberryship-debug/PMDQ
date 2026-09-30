# PMDQ -- Integration du Volet 17

## 1. Objet

Ce document explique comment le moteur d'audit sémantique (Volet 17)
est branché au Dossier Maître PMDQ v2.6.3.

## 2. Architecture

pmdq_bridge.py charge :
- data/empreinte_pmdq.json (valeurs figées v2.6.3)
- engines.py (extraction sémantique)
- rules.py (règles légales)

## 3. Utilisation

En ligne de commande :

    python pmdq_bridge.py

En Python :

    from pmdq_bridge import audit_integre, afficher_rapport_integre
    rapport = audit_integre("texte a auditer")
    afficher_rapport_integre(rapport)

## 4. Les 3 niveaux de verification

Niveau 1 -- Empreinte PMDQ : le texte contient-il des valeurs
obsoletes ? (1.5119, 8.1, 96.43)

Niveau 2 -- Invariants : I2 (pas d'absolus), I7 (ventilation).

Niveau 3 -- Semantique : tracabilite, risque electoral, barrieres.

## 5. Verdict global

Priorite 1 -- Valeur obsolete -> RUPTURE DE VERSION
Priorite 2 -- Invariant viole -> NON CONFORME
Priorite 3 -- Score <= 49 -> RISQUE ELEVE
Priorite 4 -- Score 50-79 -> RISQUE MODERE
Priorite 5 -- Tout conforme -> CONFORME

## 6. Fichiers fournis

| Fichier | Role |
|---|---|
| pmdq_bridge.py | Pont moteur / PMDQ |
| data/empreinte_pmdq.json | Valeurs figees v2.6.3 |
| PMDQ_VOLET-17.md | Doc d'extension |
| PMDQ_INTEGRATION.md | Ce document |

## 7. Limites

1. Detection par mots-cles.
2. Tolerance 0.001 sur les nombres.
3. Signal, pas avis juridique.

## 8. Reproductibilite

Aucun appel reseau. Resultats identiques bit a bit.

---

*Fin du document d'integration.*
