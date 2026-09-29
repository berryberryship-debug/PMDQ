# Socle de fiabilité — v2.7.14

Ce document explique la chaîne qui relie les variables sensibles, les
références économiques officielles, et l'ensemble des moteurs du dossier.

## Vue d'ensemble

    sources/variables-sensibles.md   (registre humain)
              |
              |  moteur_variables.py -> analyse
              v
    sources/etat_variables.json      (etat des sections)
              |
              |  lu par chaque moteur au demarrage
              v
    moteur_domar.py, moteur_fiscal.py, ...

    +-- En parallele --------------------------------------------------+
    |                                                                  |
    |  Banque du Canada (API Valet)        -->  sources/               |
    |  Statistique Canada (API WDS)        -->  cache_economique.json  |
    |  Donnees Quebec (API CKAN, CSV)      -->                         |
    |                                                                  |
    +------------------------------------------------------------------+
                          |
                          v
                  moteur_variables.py affiche les references
                  moteur_domar.py --officiel utilise le cache
                  moteur_fiscal.py affiche les ecarts

## Les 4 statuts des sections

| Statut           | Signification                                              |
|------------------|------------------------------------------------------------|
| A JOUR           | Date lisible, dans la fenetre, fichier non modifie depuis  |
| EN RETARD        | Ecart > frequence de la section                            |
| A REVOIR         | Registre modifie apres la date declaree de la section      |
| SECTION ABSENTE  | Titre de la section introuvable                            |

## Les sources economiques officielles

| Source             | Famille   | Donnees collectees                              |
|--------------------|-----------|-------------------------------------------------|
| Banque du Canada   | API Valet | Taux de change USD/CAD, taux directeur, obligations 10 ans |
| Statistique Canada | API WDS   | IPC Canada (inflation derivee sur 12 mois)      |
| Donnees Quebec     | CKAN CSV  | Dette brute du Quebec, impot des particuliers   |

Toutes les valeurs sont stockees dans `sources/cache_economique.json`.
Le champ `recupere_le` indique la date de collecte, `date_observation`
la date officielle de la donnee.

## Mettre a jour une variable sensible

1. Ouvrir `sources/variables-sensibles.md`.
2. Modifier la valeur.
3. Mettre a jour la date de la section :

       **Derniere mise a jour** : AAAA-MM-JJ

4. Regenerer l'etat et tester :

       ./make_socle.sh

Sans l'etape 3, le moteur signalera `A REVOIR`.

## Commandes utiles

| Commande                              | Role                                              |
|---------------------------------------|---------------------------------------------------|
| python3 moteur_variables.py           | Affiche les sections + references officielles     |
| python3 collecteur.py                 | Rafraichit sources/cache_economique.json          |
| python3 ecrire_etat.py                | Regenere sources/etat_variables.json              |
| python3 moteur_domar.py --officiel    | Domar avec la dette officielle du cache           |
| python3 tests_moteurs.py              | Tests unitaires du socle                          |
| ./make_socle.sh                       | Chaine complete : collecte + etat + tests + moteurs |
| ./make_socle.sh --strict              | Idem, echoue si une section est en probleme       |
| PMDQ_BLOQUANT=1 python3 moteur_X.py   | Le moteur sort en code 2 si une section est en probleme |

## Mode bloquant et strict

- `PMDQ_BLOQUANT=1` : les moteurs sortent en code 2 si une section est
  `EN RETARD`, `A REVOIR` ou `SECTION ABSENTE`.
- `./make_socle.sh --strict` : le script sort en code 3 si une section
  est en probleme, en code 1 si un moteur echoue.

Utile pour un pre-commit ou une integration continue.

## Pre-commit hook

Installe dans `.git/hooks/pre-commit`. Bloque le commit si :
- les variables sont en retard ou a revoir ;
- les tests unitaires echouent ;
- un moteur plante.

Contournement ponctuel : `git commit --no-verify`.

## Mode --officiel

Certains moteurs peuvent lire le cache et utiliser les valeurs
officielles au lieu des constantes du code.

    python3 moteur_domar.py             # D = 42.3 % (code)
    python3 moteur_domar.py --officiel  # D = 44.6 % (cache 2024-2025)

L'ecart est toujours affiche, meme en mode normal. L'humain garde le
choix.

## Frequences de mise a jour du registre

| Section                          | Frequence  |
|----------------------------------|------------|
| 1. Variables macroeconomiques    | 90 jours   |
| 2. Variables fiscales            | 365 jours  |
| 3. Variables budgetaires         | 365 jours  |
| 4. Variables de marche           | 30 jours   |
| 5. Variables legales             | 365 jours  |
| 6. Variables de projet           | 180 jours  |

## Fichiers du socle

| Fichier                          | Role                                        |
|----------------------------------|---------------------------------------------|
| moteur_variables.py              | Analyse le registre, affiche le tableau     |
| collecteur.py                    | Recupere les donnees des APIs officielles   |
| ecrire_etat.py                   | Ecrit sources/etat_variables.json           |
| tests_moteurs.py                 | Tests unitaires du socle                    |
| make_socle.sh                    | Orchestration complete                      |
| sources/variables-sensibles.md   | Registre humain                             |
| sources/etat_variables.json      | Etat machine des sections                   |
| sources/cache_economique.json    | Valeurs officielles collectees              |
| etat_socle.txt                   | Journal d'execution de make_socle.sh        |

## Ajouter une nouvelle source economique

1. Identifier l'API (Valet, WDS, CKAN).
2. Ajouter l'entree dans le dictionnaire approprie de `collecteur.py`
   (`SOURCES_VALET`, `SOURCES_STATCAN`, `SOURCES_CKAN`, `SOURCES_CKAN_PIVOT`).
3. Ajouter un test dans `tests_moteurs.py`.
4. Lancer `python3 collecteur.py` pour valider.
5. Documenter ici la nouvelle source.

## Historique des versions

| Version | Apport principal                                              |
|---------|---------------------------------------------------------------|
| v2.7.7  | Socle initial : 4 statuts, avertissement dans les moteurs     |
| v2.7.8  | Collecteur Banque du Canada (3 series)                        |
| v2.7.9  | Ajout Statistique Canada (IPC + inflation derivee)            |
| v2.7.10 | moteur_ecarts.py : detection d'ecarts registre / cache        |
| v2.7.11 | Domar : option --officiel (dette brute Quebec)                |
| v2.7.12 | Collecteur : dette brute Quebec (CKAN)                        |
| v2.7.13 | Collecteur : revenus Quebec (format pivot)                    |
| v2.7.14 | Fiscal : affichage des references officielles + tests unitaires |
