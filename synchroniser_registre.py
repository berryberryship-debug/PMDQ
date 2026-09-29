#!/usr/bin/env python3
"""
synchroniser_registre.py — Synchronisation registre ↔ cache économique
PMDQ v2.7.5

Lit sources/cache_economique.json et met à jour les valeurs du registre
sources/variables-sensibles.md dont la variable est reconnue.

Correspondances (clé cache → motif registre) :
    dette_brute_quebec       → "Ratio dette/PIB" et "Dette brute (G$)"
    taux_inflation_annuel    → "Inflation observée (IPC 12 mois)"
    taux_change_usd_cad      → "Taux de change CAD/USD"
    taux_directeur           → "Taux directeur"
    taux_obligations_10ans   → "Taux d'intérêt effectif (r)"

Une sauvegarde .bak est créée à chaque exécution.

Usage :
    python3 synchroniser_registre.py            # mode simulation
    python3 synchroniser_registre.py --ecrire   # applique les changements
"""
import json
import re
import shutil
import argparse
from pathlib import Path
from datetime import date

REGISTRE = Path("sources/variables-sensibles.md")
CACHE = Path("sources/cache_economique.json")
SAUVEGARDE = Path("sources/variables-sensibles.md.bak")

# clé cache → liste de (motif à chercher dans le registre, format de valeur)
CORRESPONDANCES = {
    "dette_brute_quebec": [
        ("Ratio dette/PIB", "ratio_pib_pct", "%"),
        ("Dette brute (G$)", "valeur_g$", "G$"),
    ],
    "taux_inflation_annuel": [
        ("Inflation observée (IPC 12 mois)", "valeur", "%"),
    ],
    "taux_change_usd_cad": [
        ("Taux de change CAD/USD", "valeur", "CAD/USD"),
    ],
    "taux_directeur": [
        ("Taux directeur", "valeur", "%"),
    ],
    "taux_obligations_10ans": [
        ("Taux d'intérêt effectif (r)", "valeur", "%"),
    ],
}


def formater(valeur, unite):
    """Formate une valeur selon son unite."""
    if unite == "%":
        return f"{valeur:.2f}".rstrip("0").rstrip(".") + " %"
    if unite == "G$":
        return f"{valeur:.3f} G$"
    return str(valeur)


def mettre_a_jour_ligne(contenu, motif_variable, nouvelle_valeur):
    """
    Remplace la valeur dans une ligne de tableau markdown du type :
        | <motif_variable> | <valeur> | <source> | <usage> |
    Retourne (nouveau_contenu, change).
    """
    # Regex : ligne commençant par | motif | ancienne_valeur | ...
    pattern = re.compile(
        r"(\|\s*" + re.escape(motif_variable) + r"\s*\|\s*)"
        r"([^|]+)"
        r"(\s*\|)",
        re.IGNORECASE,
    )
    def remplacement(m):
        return m.group(1) + f" {nouvelle_valeur} " + m.group(3)
    nouveau = pattern.sub(remplacement, contenu, count=1)
    return nouveau, nouveau != contenu


def synchroniser(ecrire=False):
    if not REGISTRE.exists():
        print(f"Erreur : {REGISTRE} introuvable")
        return
    if not CACHE.exists():
        print(f"Erreur : {CACHE} introuvable")
        return

    try:
        cache = json.loads(CACHE.read_text(encoding="utf-8"))
    except ValueError as e:
        print(f"Erreur lecture cache : {e}")
        return

    contenu = REGISTRE.read_text(encoding="utf-8")
    original = contenu
    changements = []

    for cle_cache, cibles in CORRESPONDANCES.items():
        bloc = cache.get(cle_cache)
        if not isinstance(bloc, dict):
            continue
        for motif_variable, champ, unite in cibles:
            valeur = bloc.get(champ)
            if valeur is None:
                continue
            try:
                v = float(valeur)
            except (ValueError, TypeError):
                continue
            nouvelle = formater(v, unite)
            contenu, change = mettre_a_jour_ligne(contenu, motif_variable, nouvelle)
            if change:
                changements.append((motif_variable, nouvelle))
            else:
                # Aucune ligne existante pour cette variable
                changements.append((motif_variable, f"[ABSENT] {nouvelle}"))

    # Rapport
    print()
    print("=" * 72)
    print("  SYNCHRONISATION REGISTRE ← CACHE ÉCONOMIQUE")
    print("=" * 72)
    print(f"  Date           : {date.today().isoformat()}")
    print(f"  Mode           : {'ÉCRITURE' if ecrire else 'SIMULATION (dry-run)'}")
    print()
    if not changements:
        print("  Aucune variable reconnue. Rien à faire.")
    else:
        for motif, valeur in changements:
            print(f"  · {motif:45s} → {valeur}")
    print()

    if ecrire:
        if contenu == original:
            print("  Aucune modification effective.")
        else:
            shutil.copy2(REGISTRE, SAUVEGARDE)
            REGISTRE.write_text(contenu, encoding="utf-8")
            print(f"  Sauvegarde : {SAUVEGARDE}")
            print(f"  Registre mis à jour : {REGISTRE}")
    else:
        print("  Mode simulation : relancer avec --ecrire pour appliquer.")
    print("=" * 72)
    print()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ecrire", action="store_true",
                        help="Applique les changements (sinon simulation)")
    args = parser.parse_args()
    synchroniser(ecrire=args.ecrire)
