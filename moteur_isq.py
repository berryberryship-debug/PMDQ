"""Moteur ISQ — API CKAN Données Québec."""
import json
import time
import urllib.request
import urllib.parse
import urllib.error
from datetime import date
from pathlib import Path

API_DQ = "https://www.donneesquebec.ca/api/3/action/"
USER_AGENT = "PMDQ/2.7.24 (plateforme citoyenne)"
TIMEOUT = 20
RETRIES = 3

ORGANISATIONS = ["isq", "institut-de-la-statistique-du-quebec"]

MOTS_CLES = [
    "population",
    "démographie",
    "emploi",
    "revenu",
    "économie régionale",
    "marché du travail",
]


def requete(action, params, retries=RETRIES):
    url = API_DQ + action + "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    derniere_erreur = None
    for tentative in range(retries):
        try:
            with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
                data = json.loads(r.read().decode("utf-8"))
                if not data.get("success"):
                    raise RuntimeError(f"API success=False : {data.get('error')}")
                return data
        except (urllib.error.URLError, urllib.error.HTTPError, json.JSONDecodeError, RuntimeError) as e:
            derniere_erreur = e
            if tentative < retries - 1:
                time.sleep(2 ** tentative)
    raise RuntimeError(f"Échec après {retries} tentatives : {derniere_erreur}")


def chercher(terme, organisation, limite=5):
    try:
        data = requete("package_search", {"q": terme, "fq": f"organization:{organisation}", "rows": limite})
        return data["result"]["results"]
    except Exception as e:
        print(f"  ⚠ '{terme}' ({organisation}) : {e}")
        return []


def collecter():
    resultat = {
        "source": "ISQ via Données Québec (API CKAN)",
        "url": API_DQ,
        "date_collecte": str(date.today()),
        "mots_cles": {},
        "total_jeux_uniques": 0,
    }
    jeux_vus = {}
    for terme in MOTS_CLES:
        for organisation in ORGANISATIONS:
            jeux = chercher(terme, organisation)
            for jeu in jeux:
                jid = jeu.get("name")
                if not jid or jid in jeux_vus:
                    continue
                jeux_vus[jid] = {
                    "titre": jeu.get("title"),
                    "id": jid,
                    "organisation": jeu.get("organization", {}).get("title"),
                    "notes": (jeu.get("notes") or "")[:200],
                    "date_modif": jeu.get("metadata_modified"),
                }
    resultat["mots_cles"] = {
        terme: [j for j in jeux_vus.values()
                if terme.lower() in (j["titre"] or "").lower()
                or terme.lower() in (j["notes"] or "").lower()]
        for terme in MOTS_CLES
    }
    resultat["total_jeux_uniques"] = len(jeux_vus)
    resultat["jeux"] = list(jeux_vus.values())
    return resultat


def ecrire_atomique(path, contenu):
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(contenu, encoding="utf-8")
    tmp.replace(path)


def main():
    print("=== Moteur ISQ ===")
    data = collecter()
    Path("sources").mkdir(exist_ok=True)
    sortie = Path("sources/donnees_isq.json")
    ecrire_atomique(sortie, json.dumps(data, indent=2, ensure_ascii=False))
    print(f"✓ Écrit : {sortie}")
    print(f"  {data['total_jeux_uniques']} jeu(x) unique(s) après déduplication")
    for terme, jeux in data["mots_cles"].items():
        print(f"    · '{terme}' : {len(jeux)}")


if __name__ == "__main__":
    main()
