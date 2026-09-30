# Fiches de lecture — Livres IV, V, VII

**Statut** : document de travail interne
**Date** : 30 septembre 2026

---

## Livre IV — Simulateur budgétaire

- **Fichier** : `04_livre_IV_simulateur_macro.html`
- **Objet** : simuler l'exécution budgétaire du FQBC sur 4 exercices
- **Règle** : Décaissements ≤ Ressources + Crédits + Report - Réserve
- **Réserve préventive** : 15 % de l'assiette
- **Taux d'exécution scénario central** : 84,85 %
- **Suspensions cumulées** : 1,273 G$
- **Réserve libérée** : 0,973 G$

---

## Livre V — Dette et Domar

- **Fichier** : `05_livre_V_dette_domar.html`
- **Objet** : soutenabilité de la dette du Québec
- **Dette brute** : 272,644 G$ (44,6 % du PIB)
- **Dette nette** : 250,289 G$
- **Formule** : s* = [(i - g) / (1 + g)] × d
- **Scénarios** : 2,23 / 5,29 / 10,45 G$/an
- **Trajectoires 25 ans** : 38,5 % / 51,4 % / 82,0 %
- **Note** : historique (25,3 / 42,3 / 83,5 %) préservé volontairement

---

## Livre VII — ModeleRatioD

- **Fichier** : `07_livre_VII_moteur_python.html`
- **Objet** : validation Pydantic du ratio D
- **Configuration** : strict=True, extra="forbid", allow_inf_nan=False
- **7 mécanismes anti-entropiques**
- **5 tests** : NaN, inf, champ inconnu, coercition, catégorie invalide
- **Taux de réussite** : 100 %
- **Exemple** : RESEAU-NARP-001 → D = 1,5948

---

## Règle d'usage

Ces fiches servent à documenter le contenu réel des livres, en contraste
avec les descriptions génériques qui circulent parfois. Si une page HTML
est modifiée, ces fiches doivent être mises à jour.

