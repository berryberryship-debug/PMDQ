# Note de transparence — Ajustement dette brute / PIB

**Date** : 30 septembre 2026
**Référence commit** : `7036803`
**Source** : Finances Québec 2024-2025 (via donneesquebec.ca)

## Contexte

Les premières versions du Livre V utilisaient un ratio de dette brute sur PIB de **42,3 %**.
Les comptes publics 2024-2025 fixent ce ratio à **44,6 %**.

Le PMDQ a recalibré son modèle Domar sur la valeur officielle.

## Impact sur les scénarios

| Scénario | Avant (42,3 %) | Après (44,6 %) |
|---|---:|---:|
| Favorable | 2,11 G$/an | **2,23 G$/an** |
| Central | 5,02 G$/an | **5,29 G$/an** |
| Défavorable | 9,91 G$/an | **10,45 G$/an** |

## Impact sur les trajectoires à 25 ans

| Scénario | Avant | Après |
|---|---:|---:|
| Favorable | 36,6 % | **38,5 %** |
| Central | 48,7 % | **51,4 %** |
| Défavorable | 77,8 % | **82,0 %** |

## Lecture

La conclusion politique ne change pas de nature : la dette monte en scénario central et explose en scénario défavorable. Mais l'ampleur de l'effort nécessaire augmente.

## Règle de gouvernance

Tout écart détecté entre les données sources officielles et les valeurs utilisées déclenche une révision ouverte, documentée dans `changelog.html`.

Le changement 42,3 % → 44,6 % est enregistré au commit `7036803` du 30 septembre 2026.

---

## Version radio (30 secondes)

> « En gestion publique rigoureuse, il n'y a pas de place pour le maquillage de chiffres. Quand Finances Québec a publié une dette brute à 44,6 % du PIB au lieu de 42,3 %, nous avons recalculé nos modèles et publié la correction. La conséquence est claire : l'effort de stabilisation passe de 5,02 à 5,29 G$ par an. Cacher un écart, c'est de l'irresponsabilité. Le publier et ajuster, c'est la base de la crédibilité. »

