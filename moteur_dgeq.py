"""Moteur DGEQ — interroge Données Québec pour les données électorales,
et documente les sources officielles du Directeur général des élections du Québec.

Note : le DGEQ ne publie pas d'API REST publique. Ses données sont sur
https://www.electionsquebec.qc.ca/donnees-ouvertes/ (fichiers CSV).
Ce moteur croise donc Données Québec + liste les liens DGEQ de référence."""
import json
import urllib.request
from pathlib import Path
from urllib.parse import urlencode

API_DQ = "https://www.donneesquebec.ca/api/3/action/"
USER_AGENT = "PMDQ/2.7.24 (plateforme citoyenne)"
TIMEOUT = 20

MOTS_CLES = [
    "élections",
    "financement politique",
    "partis politiques",
    "dépenses électorales",
]

# Sources de référence (non-API, à consulter manuellement ou via CSV)
SOURCES_REFERENCE = [
    {"nom": "DGEQ — Données ouvertes", "url": "https://www.electionsquebec.qc.ca/donnees-ouvertes/"},
    {"nom": "DGEQ — Financement politique", "url": "https://www.electionsquebec.qc.ca/financement-politique/"},
    {"nom": "DGEQ — Résultats électoraux", "url": "https://www.electionsquebec.qc.ca/resultats/"},
    {"nom": "Élections Canada — Données ouvertes", "url": "https://www.elections.ca/content.aspx?section=res&dir=rep&document=index&lang=f"},
]


def requete(action: str, params: dict) -> dict:
    url = API_DQ + action + "?" + urlencode(params)
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
        return json.loads(r.read().decode("utf-8"))


def chercher(terme: str, limite: int = 10) -> list:
    try:
        data = requete("package_search", {"q": terme, "rows": limite})
        if not data.get("success"):
            return []
        return data["result"]["results"]
    except Exception as e:
        print(f"  ⚠ Erreur sur '{terme}' : {e}")
        return []


def main():
    print("=== Moteur DGEQ ===")
    resultat = {
        "source_principale": "Données Québec (API CKAN) + DGEQ (fichiers CSV)",
        "date_collecte": "2026-10-01",
        "note": "Le DGEQ ne publie pas d'API REST. Voir 'sources_reference' pour les accès directs.",
        "mots_cles": {},
        "sources_reference": SOURCES_REFERENCE,
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
                }
                for j in jeux
            ],
        }
        print(f"  ✓ '{terme}' : {len(jeux)} jeu(x)")

    Path("sources").mkdir(exist_ok=True)
    Path("sources/donnees_dgeq.json").write_text(
        json.dumps(resultat, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    print("✓ Écrit : sources/donnees_dgeq.json")
    print(f"  {len(SOURCES_REFERENCE)} sources de référence documentées")


if __name__ == "__main__":
    main()
