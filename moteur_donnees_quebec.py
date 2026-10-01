"""Moteur Données Québec — interroge l'API CKAN pour des jeux de données publiques.
Source : https://www.donneesquebec.ca/api/3/action/
Aucune clé API requise. Lecture seule. User-Agent explicite (bonne pratique)."""
import json
import urllib.request
from pathlib import Path

API_BASE = "https://www.donneesquebec.ca/api/3/action/"
USER_AGENT = "PMDQ/2.7.24 (plateforme citoyenne)"
TIMEOUT = 20

# Mots-clés utiles pour le PMDQ
MOTS_CLES = [
    "contrats",
    "subventions",
    "financement politique",
    "entreprises",
    "budget",
    "dépenses",
    "environnement",
]

# Note : les données de lobbyisme ne sont PAS dans Données Québec.
# Source distincte : https://www.commissairelobby.qc.ca/ (registre des lobbyistes)


def requete(action: str, params: dict) -> dict:
    """Appelle l'API Données Québec et renvoie le JSON."""
    from urllib.parse import urlencode
    url = API_BASE + action + "?" + urlencode(params)
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
        return json.loads(r.read().decode("utf-8"))


def chercher(terme: str, limite: int = 10) -> list:
    """Recherche un terme et renvoie la liste des jeux de données."""
    try:
        data = requete("package_search", {"q": terme, "rows": limite})
        if not data.get("success"):
            return []
        return data["result"]["results"]
    except Exception as e:
        print(f"  ⚠ Erreur sur '{terme}' : {e}")
        return []


def collecter() -> dict:
    """Interroge l'API pour tous les mots-clés et renvoie un dict structuré."""
    resultat = {
        "source": "Données Québec (API CKAN)",
        "url": API_BASE,
        "date_collecte": "2026-10-01",
        "mots_cles": {},
    }
    for terme in MOTS_CLES:
        jeux = chercher(terme)
        resultat["mots_cles"][terme] = {
            "total": len(jeux),
            "jeux": [
                {
                    "titre": j.get("title"),
                    "id": j.get("name"),
                    "organisation": j.get("organization", {}).get("title"),
                    "notes": (j.get("notes") or "")[:200],
                }
                for j in jeux
            ],
        }
        print(f"  ✓ '{terme}' : {len(jeux)} jeu(x)")
    return resultat


def main():
    print("=== Moteur Données Québec ===")
    data = collecter()
    Path("sources").mkdir(exist_ok=True)
    sortie = Path("sources/donnees_quebec.json")
    sortie.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"\n✓ Écrit : {sortie}")
    print(f"  Total mots-clés : {len(data['mots_cles'])}")


if __name__ == "__main__":
    main()
