"""Moteur Lobbyisme — documente les sources officielles du Commissaire au lobbyisme
du Québec et cherche des données complémentaires sur Données Québec.

Note : le registre des lobbyistes est sur https://www.commissairelobby.qc.ca/registre/
Il n'y a pas d'API REST publique. Ce moteur documente les accès et croise Données Québec."""
import json
import urllib.request
from pathlib import Path
from urllib.parse import urlencode

API_DQ = "https://www.donneesquebec.ca/api/3/action/"
USER_AGENT = "PMDQ/2.7.24 (plateforme citoyenne)"
TIMEOUT = 20

MOTS_CLES_DQ = ["lobbyisme", "lobbyistes", "influence", "transparence"]

SOURCES_REFERENCE = [
    {"nom": "Commissaire au lobbyisme — Registre", "url": "https://www.commissairelobby.qc.ca/registre/"},
    {"nom": "Commissaire au lobbyisme — Données ouvertes", "url": "https://www.commissairelobby.qc.ca/publications/donnees-ouvertes/"},
    {"nom": "Commissaire au lobbyisme — Rapports annuels", "url": "https://www.commissairelobby.qc.ca/publications/"},
    {"nom": "Registre des entreprises du Québec (REQ)", "url": "https://www.registreentreprises.gouv.qc.ca/"},
    {"nom": "Autorité des marchés publics", "url": "https://www.amp.quebec/"},
]


def requete(action, params):
    url = API_DQ + action + "?" + urlencode(params)
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
        return json.loads(r.read().decode("utf-8"))


def chercher(terme, limite=10):
    try:
        data = requete("package_search", {"q": terme, "rows": limite})
        if not data.get("success"):
            return []
        return data["result"]["results"]
    except Exception as e:
        print(f"  ⚠ Erreur sur '{terme}' : {e}")
        return []


def main():
    print("=== Moteur Lobbyisme ===")
    resultat = {
        "source_principale": "Commissaire au lobbyisme du Québec (registre) + Données Québec (CKAN)",
        "date_collecte": "2026-10-01",
        "note": "Le registre des lobbyistes n'a pas d'API REST publique. Voir 'sources_reference'.",
        "mots_cles": {},
        "sources_reference": SOURCES_REFERENCE,
    }
    for terme in MOTS_CLES_DQ:
        jeux = chercher(terme)
        resultat["mots_cles"][terme] = {
            "total": len(jeux),
            "jeux": [
                {"titre": j.get("title"), "id": j.get("name"),
                 "organisation": j.get("organization", {}).get("title")}
                for j in jeux
            ],
        }
        print(f"  ✓ '{terme}' : {len(jeux)} jeu(x)")

    Path("sources").mkdir(exist_ok=True)
    Path("sources/donnees_lobbyisme.json").write_text(
        json.dumps(resultat, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    print("✓ Écrit : sources/donnees_lobbyisme.json")
    print(f"  {len(SOURCES_REFERENCE)} sources de référence documentées")


if __name__ == "__main__":
    main()
