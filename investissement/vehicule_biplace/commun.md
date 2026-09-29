# Éléments mutualisés entre les trois scénarios

Ce document rassemble tout ce qui peut être conçu une seule fois et
réutilisé dans les trois scénarios. Cela évite de financer trois fois
la même recherche.

## Design du biplace

- Architecture générale : deux places côte à côte, portes latérales
- Empreinte au sol : 2,60–3,40 m de long, 1,30–1,70 m de large
- Habitacle fermé, chauffage électrique, ventilation
- Planche de bord standardisée (affichage vitesse, autonomie, état batterie)
- Ergonomie, sièges, ceintures : conception unique

## Chaîne de propulsion

Trois options selon le scénario :

| Scénario | Puissance | Type moteur | Batterie |
|---|---|---|---|
| A — VBV 40 | 8–12 kW | Brushless + réducteur | 12–15 kWh LFP |
| B — Voiture 50 | 15–25 kW | Synchrone ou brushless | 15–20 kWh LFP/NMC |
| C — Milieu fermé | 5–10 kW | Brushless | 8–15 kWh LFP |

Le moteur et le contrôleur peuvent être les mêmes, seule la puissance
crête change. Cela permet un volume d'achat mutualisé.

## Batterie

- Cellules LFP (First Phosphate ou équivalent importé)
- BMS et boîtier identiques sur les trois scénarios
- Capacité modulable (modules de 3 kWh empilables)
- Assemblage : SysNergie ou atelier interne au Québec

## Électronique embarquée

- Calculateur central unique
- Firmware commun aux trois versions
- OTA (mises à jour à distance) en option
- Interface diagnostic standardisée

## Propriété intellectuelle

Recommandation : créer une entité détentrice de la PI (design,
firmware, marque). Chaque scénario devient une société projet qui
licencie la PI. Cela protège la valeur en cas de succès d'un scénario
et de difficulté d'un autre.

## Approvisionnement

- Cellules : importation (Chine, Corée) — prix 2025-2026 bas
- Moteur : TESUP, FTEX, ou équivalent
- Châssis : sous-traitance métallique locale
- Assemblage final : atelier québécois

## Feuille de route commune

| Étape | Durée | Applicable à |
|---|---|---|
| Conception plateforme | 4–6 mois | A, B, C |
| Prototype roulant | 6–12 mois | A, B, C |
| Essais fonctionnels | 3–6 mois | A, B, C |
| Homologation VBV | 6–12 mois | A |
| Homologation voiture | 18–36 mois | B |
| Première série | 6–12 mois | C, puis A |

## Chiffres de référence

- Prix cellules LFP 2025 : 84–108 $US/kWh
- Prix moteur 10–15 kW : 2 000–5 000 $
- Assemblage batterie 15 kWh : 1 500–3 000 $
- Ingénierie complète plateforme : 150–400 k$

## Prochaine mise à jour

Ce document sera enrichi quand les spécifications d'un scénario
seront figées, et les autres scénarios hériteront des choix validés.
