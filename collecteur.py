#!/usr/bin/env python3
"""
collecteur.py — Récupération des références économiques actualisées
PMDQ v2.7.8

Récupère les données depuis l'API Valet de la Banque du Canada.
Cache local dans sources/cache_economique.json (secours + traçabilité).

Usage :
    python3 collecteur.py            met à jour le cache
    python3 collecteur.py --liste    liste les sources
    python3 collecteur.py --json     sortie JSON brute
"""

import argparse
import json
import sys
import urllib.error
import urllib.request
from datetime import date
from pathlib import Path


CACHE = Path("sources/cache_economique.json")

SOURCES = {
    "taux_change_usd_cad": {
        "nom": "Taux de change USD/CAD",
        "url": "https://www.bankofcanada.ca/valet/observations/FXUSDCAD/json?recent=1",
        "unite": "CAD par USD",
        "source": "Banque du Canada",
    },
    "taux_directeur": {
        "nom": "Taux directeur Banque du Canada",
        "url": "https://www.bankofcanada.ca/valet/observations/V39079/json?recent=1",
        "unite": "%",
        "source": "Banque du Canada",
    },
    "taux_obligations_10ans": {
        "nom": "Rendement obligations 10 ans",
        "url": "https://www.bankofcanada.ca/valet/observations/BD.CDN.10YR.DQ.YLD/json?recent=1",
        "unite": "%",
        "source": "Banque du Canada",
    },
}


def recuperer_valet(url, timeout=15):
    """Recupere une observation depuis l'API Valet."""
    try:
        req = urllib.request.Request(
            url, headers={"User-Agent": "PMDQ-collecteur/1.0"}
        )
        with urllib.request.urlopen(req, timeout=timeout) as r:
            data = json.loads(r.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        return None, f"HTTP {e.code}"
    except urllib.error.URLError as e:
        return None, f"Reseau : {e.reason}"
    except (OSError, ValueError) as e:
        return None, f"Lecture : {e}"

    obs = data.get("observations", [])
    if not obs:
        return None, "Aucune observation"

    derniere = obs[-1]
    date_obs = derniere.get("d")
    for cle, val in derniere.items():
        if cle != "d" and isinstance(val, dict) and "v" in val:
            return {
                "valeur": float(val["v"]),
                "date_observation": date_obs,
            }, None
    return None, "Format inattendu"


def charger_cache():
    if CACHE.exists():
        try:
            return json.loads(CACHE.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            return {}
    return {}


def sauver_cache(cache):
    CACHE.parent.mkdir(parents=True, exist_ok=True)
    CACHE.write_text(
        json.dumps(cache, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )


def collecter(verbose=True):
    cache = charger_cache()
    resultats = []

    for cle, info in SOURCES.items():
        val, err = recuperer_valet(info["url"])

        if val is None:
            ancien = cache.get(cle, {})
            ancienne_valeur = ancien.get("valeur")
            resultats.append({
                "cle": cle,
                "nom": info["nom"],
                "statut": "ECHEC",
                "detail": err,
                "valeur_cache": ancienne_valeur,
            })
            if verbose:
                msg = f"  ECHEC  {info['nom']:<38} {err}"
                if ancienne_valeur is not None:
                    msg += f" (cache : {ancienne_valeur})"
                print(msg)
            continue

        cache[cle] = {
            "valeur": val["valeur"],
            "date_observation": val["date_observation"],
            "source": info["source"],
            "unite": info["unite"],
            "recupere_le": str(date.today()),
        }
        resultats.append({
            "cle": cle,
            "nom": info["nom"],
            "statut": "OK",
            "valeur": val["valeur"],
            "date_observation": val["date_observation"],
        })
        if verbose:
            print(f"  OK     {info['nom']:<38} {val['valeur']} ({val['date_observation']})")

    cache["_meta"] = {
        "derniere_mise_a_jour": str(date.today()),
        "nb_sources": len(SOURCES),
    }
    sauver_cache(cache)
    return resultats


def main():
    parser = argparse.ArgumentParser(description="Collecteur references economiques")
    parser.add_argument("--json", action="store_true", help="Sortie JSON")
    parser.add_argument("--liste", action="store_true", help="Liste les sources")
    args = parser.parse_args()

    if args.liste:
        for cle, info in SOURCES.items():
            print(f"  {cle:<28} {info['nom']:<40} {info['source']}")
        return

    print()
    print("=" * 72)
    print("  COLLECTEUR REFERENCES ECONOMIQUES — PMDQ v2.7.8")
    print("=" * 72)
    print(f"  Date : {date.today()}")
    print()

    res = collecter(verbose=not args.json)

    if args.json:
        print(json.dumps(res, indent=2, ensure_ascii=False))
    else:
        print()
        ok = sum(1 for r in res if r["statut"] == "OK")
        ko = sum(1 for r in res if r["statut"] == "ECHEC")
        print(f"  Bilan : {ok} OK, {ko} ECHEC")
        print(f"  Cache : {CACHE}")
        print("=" * 72)
        print()

    if any(r["statut"] == "ECHEC" for r in res):
        sys.exit(1)


if __name__ == "__main__":
    main()
