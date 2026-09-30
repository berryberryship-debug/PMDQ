#!/usr/bin/env python3
"""test_empreinte.py -- Verifie la coherence de l'empreinte PMDQ v2.6.3."""
import json
from pathlib import Path

CHEMIN = Path(__file__).parent / "data" / "empreinte_pmdq.json"


def charger():
    with open(CHEMIN, encoding="utf-8") as f:
        return json.load(f)


def test_version():
    e = charger()
    assert e["version"] == "2.6.3", "Version attendue 2.6.3, trouvee " + str(e["version"])


def test_ratio_narp():
    e = charger()
    r = e["invariants_numeriques"]["RESEAU-NARP-001_ratio"]
    assert r == 1.5948, "Ratio NARP attendu 1.5948, trouve " + str(r)


def test_ratio_comm_autog():
    e = charger()
    r = e["invariants_numeriques"]["COMM-AUTOG-013_ratio"]
    assert r == 1.2667, "Ratio COMM-AUTOG attendu 1.2667, trouve " + str(r)


def test_enveloppe():
    e = charger()
    v = e["invariants_numeriques"]["enveloppe_FQBC_G"]
    assert v == 8.40, "Enveloppe attendue 8.40, trouvee " + str(v)


def test_nb_articles():
    e = charger()
    n = e["invariants_structurels"]["nb_articles"]
    assert n == 47, "Articles attendus 47, trouve " + str(n)


def test_nb_volets():
    e = charger()
    n = e["invariants_structurels"]["nb_volets_audit"]
    assert n == 16, "Volets attendus 16, trouve " + str(n)


def test_nb_projets():
    e = charger()
    n = e["invariants_structurels"]["nb_projets_types"]
    assert n == 17, "Projets attendus 17, trouve " + str(n)


def test_valeurs_obsoletes():
    e = charger()
    incomp = e["incompatibilites_connues"]["valeurs_a_ne_jamais_accepter"]
    assert len(incomp) == 3, "3 incompatibilites attendues, trouve " + str(len(incomp))


if __name__ == "__main__":
    tests = [
        ("Version 2.6.3", test_version),
        ("Ratio RESEAU-NARP-001", test_ratio_narp),
        ("Ratio COMM-AUTOG-013", test_ratio_comm_autog),
        ("Enveloppe FQBC", test_enveloppe),
        ("Nombre d'articles", test_nb_articles),
        ("Nombre de volets", test_nb_volets),
        ("Nombre de projets", test_nb_projets),
        ("Valeurs obsoletes", test_valeurs_obsoletes),
    ]
    ok = 0
    for nom, fn in tests:
        try:
            fn()
            print("[OK]   " + nom)
            ok += 1
        except AssertionError as e:
            print("[FAIL] " + nom + " : " + str(e))
    print("\nBilan : " + str(ok) + "/" + str(len(tests)) + " reussis")
