# scripts/rev34 — Simulation torus 5D / GKSL

## Statut
**[É] — Exploratoire.** Module scientifique isolé, sans lien direct avec le cœur budgétaire ou institutionnel du PMDQ.

## Objet

Ce dossier contient une simulation numérique exploratoire sur la **robustesse d'une phase topologique** face à la décohérence, dans un système quantique ouvert à 5 niveaux.

## Fichier principal

- `rev34_torus_fixed.py` — Simulation de l'équation de Lindblad (forme GKSL — Gorini–Kossakowski–Sudarshan–Lindblad).

## Logique du modèle

### Hamiltonien « torus 5D »

- **5 états** (|0⟩ → |4⟩) formant un **cycle fermé** (graphe en anneau).
- Couplage voisin-à-voisin d'intensité `g(t)` — enveloppe gaussienne centrée.
- **Phase topologique** `exp(1j × 2π/5)` sur le lien de fermeture → équivalent d'un flux magnétique à travers le cycle (facteur de Berry / phase géométrique).

### Évolution ouverte (dissipation)

- Liouvillian GKSL construit avec un opérateur de bruit diagonal `A_bruit = diag([1.0, 0.7, 0.2, -0.4, -1.5])`.
- Taux de dissipation faible : `γ = 0,015`.
- Intégration par `solve_ivp` (méthode Radau, précise pour systèmes raides).
- État initial : pur |0⟩⟨0|.

### Sortie

- Pureté finale `Tr(ρ²)`.
- Populations des 5 niveaux.
- Mesure de la perte d'information (décohérence) induite par le bruit + la dynamique topologique.

## Exécution

```bash
cd scripts/rev34
python3 rev34_torus_fixed.py
ls -la CDLI/README.md scripts/rev34/README.md 2>&1
