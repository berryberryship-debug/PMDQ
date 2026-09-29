#!/usr/bin/env python3
"""
collecteur.py — Récupération des références économiques actualisées
PMDQ v2.7.9

Deux familles de sources :
    - Banque du Canada (API Valet, GET JSON)
    - Statistique Canada (API WDS, POST JSON)

Cache local dans sources/cache_economique.json (secours + traçabilité).

Usage :
    python3 collecteur.py            met à jour le cache
    python3 collecteur.py --liste    liste les sources
    python3 collecteur.py --json     sortie JSON brute
"""

import argparse
import csv
import io
import json
import sys
import urllib.error
import urllib.request
from datetime import date
from pathlib import Path


CACHE = Path("sources/cache_economique.json")

# --- Sources Banque du Canada (Valet, GET) ---
SOURCES_VALET = {
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

# --- Sources Statistique Canada (WDS, POST) ---
STATCAN_URL = "https://www150.statcan.gc.ca/t1/wds/rest/getDataFromVectorsAndLatestNPeriods"

SOURCES_STATCAN = {
    "ipc_canada": {
        "nom": "IPC total Canada",
        "vector_id": 41690973,
        "unite": "indice (2002=100)",
        "source": "Statistique Canada (18-10-0004-01)",
        "latest_n": 1,
    },
}

# --- Sources Donnees Quebec (CKAN, CSV) ---
CKAN_BASE = "https://www.donneesquebec.ca/recherche/api/3/action"

SOURCES_CKAN = {
    "dette_brute_quebec": {
        "nom": "Dette brute du Quebec",
        "dataset_id": "dette-du-gouvernement-du-quebec",
        "colonne_annee": "Annee",
        "colonne_valeur": "Dette_directe_con_$",
        "colonne_ratio": "Dette_directe_con_%",
        "unite": "G$",
        "source": "Finances Quebec (via donneesquebec.ca)",
    },
}


def recuperer_valet(url, timeout=15):
    """Recupere une observation depuis l'API Valet (Banque du Canada)."""
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


def recuperer_statcan(vector_id, latest_n=1, timeout=20):
    """Recupere les dernieres observations d'un vecteur StatCan."""
    body = json.dumps([{"vectorId": vector_id, "latestN": latest_n}]).encode("utf-8")
    try:
        req = urllib.request.Request(
            STATCAN_URL,
            data=body,
            headers={
                "Content-Type": "application/json",
                "User-Agent": "PMDQ-collecteur/1.0",
            },
            method="POST",
        )
        with urllib.request.urlopen(req, timeout=timeout) as r:
            data = json.loads(r.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        return None, f"HTTP {e.code}"
    except urllib.error.URLError as e:
        return None, f"Reseau : {e.reason}"
    except (OSError, ValueError) as e:
        return None, f"Lecture : {e}"

    if not isinstance(data, list) or not data:
        return None, "Reponse vide"

    item = data[0]
    if item.get("status") != "SUCCESS":
        return None, f"Statut : {item.get('status')}"

    points = item.get("object", {}).get("vectorDataPoint", [])
    if not points:
        return None, "Aucun point"

    if latest_n == 1:
        p = points[-1]
        return {
            "valeur": p.get("value"),
            "date_observation": p.get("refPer"),
            "points": points,
        }, None
    else:
        return {
            "valeur": points[-1].get("value"),
            "date_observation": points[-1].get("refPer"),
            "points": points,
        }, None



def _nettoyer_nombre(s):
    """Convertit '262,871,000,000' en float. Gere formats canadiens."""
    if s is None:
        return None
    s = str(s).strip()
    # Normaliser les tirets longs et espaces
    s = s.replace("\u2013", "-").replace("\u2014", "-")
    s = s.replace("\xa0", "").replace(" ", "")
    # Format quebec : virgules = milliers, point = decimal
    # Ex: "262,871,000,000" -> 262871000000
    # Ex: "44,6" -> 44.6
    if "," in s and "." in s:
        # Les deux presents : la derniere est le decimal
        if s.rfind(",") > s.rfind("."):
            s = s.replace(".", "").replace(",", ".")
        else:
            s = s.replace(",", "")
    elif "," in s:
        # Seulement des virgules. Si c'est un montant a 3 chiffres apres
        # chaque virgule, c'est un separateur de milliers.
        parts = s.split(",")
        if all(len(p) == 3 for p in parts[1:]) and len(parts) > 1:
            s = s.replace(",", "")
        else:
            s = s.replace(",", ".")
    s = s.replace("$", "").replace("%", "").strip()
    try:
        return float(s)
    except ValueError:
        return None


def recuperer_ckan(dataset_id, timeout=30):
    """Recupere la derniere ressource CSV d'un dataset CKAN."""
    url = f"{CKAN_BASE}/package_show?id={dataset_id}"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "PMDQ/1.0"})
        with urllib.request.urlopen(req, timeout=timeout) as r:
            data = json.loads(r.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        return None, f"HTTP {e.code}"
    except urllib.error.URLError as e:
        return None, f"Reseau : {e.reason}"
    except (OSError, ValueError) as e:
        return None, f"Lecture : {e}"

    resources = data.get("result", {}).get("resources", [])
    if not resources:
        return None, "Aucune ressource"

    # Prendre la derniere ressource CSV
    csvs = [r for r in resources if (r.get("format") or "").upper() == "CSV"]
    if not csvs:
        return None, "Aucune ressource CSV"

    derniere = csvs[-1]
    url_csv = derniere.get("url")
    if not url_csv:
        return None, "URL CSV manquante"

    try:
        req2 = urllib.request.Request(url_csv, headers={"User-Agent": "PMDQ/1.0"})
        with urllib.request.urlopen(req2, timeout=timeout) as r2:
            contenu = r2.read().decode("utf-8", errors="replace")
    except urllib.error.HTTPError as e:
        return None, f"HTTP CSV {e.code}"
    except urllib.error.URLError as e:
        return None, f"Reseau CSV : {e.reason}"
    except OSError as e:
        return None, f"Lecture CSV : {e}"

    return {"nom": derniere.get("name", "?"), "url": url_csv, "contenu": contenu}, None



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

    # --- 1. Banque du Canada ---
    if verbose:
        print("  --- Banque du Canada ---")
    for cle, info in SOURCES_VALET.items():
        val, err = recuperer_valet(info["url"])

        if val is None:
            ancien = cache.get(cle, {})
            ancienne_valeur = ancien.get("valeur")
            resultats.append({
                "cle": cle, "nom": info["nom"], "statut": "ECHEC",
                "detail": err, "valeur_cache": ancienne_valeur,
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
            "cle": cle, "nom": info["nom"], "statut": "OK",
            "valeur": val["valeur"],
            "date_observation": val["date_observation"],
        })
        if verbose:
            print(f"  OK     {info['nom']:<38} {val['valeur']} ({val['date_observation']})")

    # --- 2. Statistique Canada ---
    if verbose:
        print()
        print("  --- Statistique Canada ---")
    for cle, info in SOURCES_STATCAN.items():
        val, err = recuperer_statcan(info["vector_id"], info.get("latest_n", 1))

        if val is None:
            ancien = cache.get(cle, {})
            ancienne_valeur = ancien.get("valeur")
            resultats.append({
                "cle": cle, "nom": info["nom"], "statut": "ECHEC",
                "detail": err, "valeur_cache": ancienne_valeur,
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
            "cle": cle, "nom": info["nom"], "statut": "OK",
            "valeur": val["valeur"],
            "date_observation": val["date_observation"],
        })
        if verbose:
            print(f"  OK     {info['nom']:<38} {val['valeur']} ({val['date_observation']})")

    # --- 3. Donnees Quebec (CKAN) ---
    if verbose:
        print()
        print("  --- Donnees Quebec (CKAN) ---")
    for cle, info in SOURCES_CKAN.items():
        res, err = recuperer_ckan(info["dataset_id"])

        if res is None:
            ancien = cache.get(cle, {})
            resultats.append({
                "cle": cle, "nom": info["nom"], "statut": "ECHEC",
                "detail": err, "valeur_cache": ancien.get("valeur"),
            })
            if verbose:
                print(f"  ECHEC  {info['nom']:<38} {err}")
            continue

        # Parser le CSV
        contenu_sans_bom = res["contenu"].lstrip("\ufeff")
        lecteur = csv.DictReader(io.StringIO(contenu_sans_bom))
        lignes = list(lecteur)
        if not lignes:
            resultats.append({
                "cle": cle, "nom": info["nom"], "statut": "ECHEC",
                "detail": "CSV vide",
            })
            if verbose:
                print(f"  ECHEC  {info['nom']:<38} CSV vide")
            continue

        # La premiere ligne est la plus recente
        ligne = lignes[0]
        col_v = info["colonne_valeur"]
        col_r = info.get("colonne_ratio")
        col_a = info.get("colonne_annee")

        val_brute = _nettoyer_nombre(ligne.get(col_v))
        val_ratio = _nettoyer_nombre(ligne.get(col_r)) if col_r else None
        annee = ligne.get(col_a, "").strip() if col_a else ""

        if val_brute is None and val_ratio is None:
            resultats.append({
                "cle": cle, "nom": info["nom"], "statut": "ECHEC",
                "detail": f"Colonnes vides ({col_v}, {col_r})",
            })
            if verbose:
                print(f"  ECHEC  {info['nom']:<38} Colonnes vides")
            continue

        # Stocker dans le cache
        cache[cle] = {
            "valeur": val_ratio if val_ratio is not None else val_brute,
            "valeur_g$": round(val_brute / 1e9, 3) if val_brute is not None else None,
            "ratio_pib_pct": val_ratio,
            "annee": annee,
            "date_observation": annee,
            "source": info["source"],
            "unite": info["unite"],
            "recupere_le": str(date.today()),
        }
        resultats.append({
            "cle": cle, "nom": info["nom"], "statut": "OK",
            "valeur": cache[cle]["valeur"],
            "date_observation": annee,
        })
        if verbose:
            det = f"{annee}"
            if val_ratio is not None:
                det += f" {val_ratio} %"
            if val_brute is not None:
                det += f" ({round(val_brute / 1e9, 1)} G$)"
            print(f"  OK     {info['nom']:<38} {det}")

    # --- 4. Valeurs derivees ---
    if verbose:
        print()
        print("  --- Valeurs derivees ---")

    # Taux d'inflation annuel = variation IPC sur 12 mois
    ipc_12, err = recuperer_statcan(41690973, latest_n=13)
    if ipc_12 is not None:
        pts = ipc_12["points"]
        if len(pts) >= 13:
            v_actuelle = pts[-1]["value"]
            v_12mois = pts[0]["value"]
            if v_12mois and v_12mois > 0:
                inflation = (v_actuelle / v_12mois - 1) * 100
                cache["taux_inflation_annuel"] = {
                    "valeur": round(inflation, 2),
                    "date_observation": pts[-1]["refPer"],
                    "source": "Statistique Canada (IPC 12 mois)",
                    "unite": "%",
                    "recupere_le": str(date.today()),
                }
                resultats.append({
                    "cle": "taux_inflation_annuel",
                    "nom": "Taux inflation annuel (IPC 12 mois)",
                    "statut": "OK",
                    "valeur": round(inflation, 2),
                    "date_observation": pts[-1]["refPer"],
                })
                if verbose:
                    print(f"  OK     {'Taux inflation annuel (IPC 12 mois)':<38} {round(inflation,2)} % ({pts[-1]['refPer']})")
        else:
            if verbose:
                print(f"  ECHEC  Taux inflation annuel : {len(pts)} points (13 requis)")

    cache["_meta"] = {
        "derniere_mise_a_jour": str(date.today()),
        "nb_sources": len(SOURCES_VALET) + len(SOURCES_STATCAN) + len(SOURCES_CKAN),
    }
    sauver_cache(cache)
    return resultats


def main():
    parser = argparse.ArgumentParser(description="Collecteur references economiques")
    parser.add_argument("--json", action="store_true", help="Sortie JSON")
    parser.add_argument("--liste", action="store_true", help="Liste les sources")
    args = parser.parse_args()

    if args.liste:
        print("Sources Banque du Canada :")
        for cle, info in SOURCES_VALET.items():
            print(f"  {cle:<28} {info['nom']}")
        print()
        print("Sources Statistique Canada :")
        for cle, info in SOURCES_STATCAN.items():
            print(f"  {cle:<28} {info['nom']} (vecteur {info['vector_id']})")
        return

    print()
    print("=" * 72)
    print("  COLLECTEUR REFERENCES ECONOMIQUES — PMDQ v2.7.9")
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
