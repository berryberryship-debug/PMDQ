# Socle de fiabilité — v2.7.7

Ce document explique la chaîne de traçabilité qui relie le registre des
variables sensibles à l'ensemble des moteurs du dossier PMDQ.

## Vue d'ensemble

    sources/variables-sensibles.md   (registre humain, Markdown)
              |
              |  moteur_variables.py  -> analyse
              v
    sources/etat_variables.json      (point de verite machine)
              |
              |  chaque moteur lit ce fichier au demarrage
              v
    moteur_domar.py, moteur_fiscal.py, ... (avertissement si necessaire)

## Les 4 statuts

| Statut           | Signification                                                  |
|------------------|----------------------------------------------------------------|
| A JOUR           | Date lisible, dans la fenetre de frequence, fichier non modifie depuis |
| EN RETARD        | Date lisible, ecart > frequence de la section                  |
| A REVOIR         | Le registre a ete modifie apres la date declaree de la section |
| SECTION ABSENTE  | Le titre de la section n'a pas ete trouve dans le registre     |

## Mettre a jour une variable

1. Ouvrir sources/variables-sensibles.md.
2. Modifier la valeur souhaitee.
3. Mettre a jour la date de la section :

       **Derniere mise a jour** : AAAA-MM-JJ

4. Regenerer l'etat machine :

       python3 ecrire_etat.py

5. Verifier l'etat global :

       ./make_socle.sh

Sans l'etape 3, le moteur affichera A REVOIR au prochain lancement.

## Commandes utiles

| Commande                              | Role                                             |
|---------------------------------------|--------------------------------------------------|
| python3 moteur_variables.py           | Affiche le tableau des 6 sections                |
| python3 ecrire_etat.py                | Regenere sources/etat_variables.json             |
| ./make_socle.sh                       | Regenere l'etat + teste les 8 moteurs            |
| ./make_socle.sh --strict              | Idem, mais echoue (code 3) si une section est en probleme |
| PMDQ_BLOQUANT=1 python3 moteur_X.py   | Echoue (code 2) si une section est en probleme   |

## Mode bloquant

Par defaut, les moteurs avertissent puis continuent. Pour un usage en
chaine automatisee (CI, publication), activer le mode bloquant :

    PMDQ_BLOQUANT=1 ./make_socle.sh --strict

Le script sortira en code different de 0 si :
- un moteur echoue (code 1),
- une section est en probleme (code 3).

## Frequences de mise a jour

| Section                          | Frequence  |
|----------------------------------|------------|
| 1. Variables macroeconomiques    | 90 jours   |
| 2. Variables fiscales            | 365 jours  |
| 3. Variables budgetaires         | 365 jours  |
| 4. Variables de marche           | 30 jours   |
| 5. Variables legales             | 365 jours  |
| 6. Variables de projet           | 180 jours  |

## Fichiers du socle

| Fichier                          | Role                                       |
|----------------------------------|--------------------------------------------|
| moteur_variables.py              | Analyse le registre, affiche le tableau    |
| ecrire_etat.py                   | Ecrit sources/etat_variables.json          |
| make_socle.sh                    | Orchestration : etat + tests               |
| sources/etat_variables.json      | Etat machine consomme par les moteurs      |
| sources/variables-sensibles.md   | Registre humain                            |
