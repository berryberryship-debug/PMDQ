"""Moteur socio-économique — API CKAN Données Québec.
Garde-fous : fallback si API plante, validation avant écrasement, enrichissement métadonnées."""
import json
import time
import urllib.request
import urllib.parse
import urllib.error
from datetime import date, datetime
from pathlib import Path

API_DQ = "https://www.donneesquebec.ca/api/3/action/"
USER_AGENT = "PMDQ/2.7.24 (plateforme citoyenne)"
TIMEOUT = 20
RETRIES = 3
SEUIL_REGRESSION = 0.5
SEUIL_OBSOLESCENCE_JOURS = 730

CIBLES = {
    "travaill": ["emploi", "marché du travail", "revenu", "aide sociale"],
    "mifi": ["immigration", "francisation", "intégration"],
    "affaires-municipales-et-occupation-du-territoire": ["population", "habitation", "municipalités"],
    "inspq": ["population", "santé publique", "déterminants sociaux"],
    "revenu-quebec": ["revenu", "fiscalité", "impôt"],
    "mfq": ["finances publiques", "budget", "dette"],
    "mels": ["diplomation", "décrochage", "étudiants"],
    "msss": ["santé", "urgences", "services sociaux"],
    "mtrav": ["travail", "normes du travail", "santé et sécurité"],
    "cnestt": ["normes du travail", "équité salariale"],
    "frqs": ["recherche", "santé", "société"],
}


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
        except (urllib.error.URLError, urllib.error.HTTPError,
                json.JSONDecodeError, RuntimeError) as e:
            derniere_erreur = e
            if tentative < retries - 1:
                time.sleep(2 ** tentative)
    raise RuntimeError(f"Échec après {retries} tentatives : {derniere_erreur}")


def chercher(terme, organisation, limite=10):
    try:
        data = requete("package_search", {"q": terme, "fq": f"organization:{organisation}", "rows": limite})
        return data["result"]["results"]
    except Exception as e:
        print(f"  ⚠ '{terme}' ({organisation}) : {e}")
        return []


def enrichir_fiche(jeu):
    ressources = jeu.get("resources") or []
    formats = sorted({r.get("format", "").upper() for r in ressources if r.get("format")})
    date_modif = jeu.get("metadata_modified") or jeu.get("modified")
    obsolescence = None
    if date_modif:
        try:
            dt = datetime.fromisoformat(date_modif.replace("Z", "+00:00"))
            age = (datetime.now(dt.tzinfo) - dt).days
            obsolescence = age > SEUIL_OBSOLESCENCE_JOURS
        except Exception:
            pass
    return {
        "titre": jeu.get("title"),
        "id": jeu.get("name"),
        "organisation": jeu.get("organization", {}).get("title"),
        "notes": (jeu.get("notes") or "")[:200],
        "date_modif": date_modif,
        "obsolète": obsolescence,
        "licence": jeu.get("license_title") or jeu.get("license_id"),
        "formats": formats,
        "nb_ressources": len(ressources),
    }


def collecter():
    resultat = {
        "source": "Données Québec (API CKAN) — socio-économique",
        "url": API_DQ,
        "date_collecte": str(date.today()),
        "par_organisation": {},
        "jeux_uniques": {},
    }
    for organisation, mots_cles in CIBLES.items():
        resultat["par_organisation"][organisation] = {"mots_cles": {}}
        for terme in mots_cles:
            jeux = chercher(terme, organisation)
            resultat["par_organisation"][organisation]["mots_cles"][terme] = []
            for jeu in jeux:
                jid = jeu.get("name")
                if not jid:
                    continue
                fiche = enrichir_fiche(jeu)
                resultat["par_organisation"][organisation]["mots_cles"][terme].append(fiche)
                resultat["jeux_uniques"][jid] = fiche
    resultat["total_jeux_uniques"] = len(resultat["jeux_uniques"])
    return resultat


def lire_ancien(path):
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return None


def valider(ancien, nouveau):
    if ancien is None:
        return True, "premier passage"
    ancien_n = ancien.get("total_jeux_uniques", 0)
    nouveau_n = nouveau.get("total_jeux_uniques", 0)
    if ancien_n == 0:
        return True, "ancien vide"
    ratio = nouveau_n / ancien_n
    if ratio < SEUIL_REGRESSION:
        return False, f"régression : {nouveau_n}/{ancien_n} ({ratio:.0%})"
    return True, f"OK : {nouveau_n}/{ancien_n} ({ratio:.0%})"


def ecrire_atomique(path, contenu):
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(contenu, encoding="utf-8")
    tmp.replace(path)


def main():
    print("=== Moteur socio-économique ===")
    sortie = Path("sources/donnees_socioeco.json")
    ancien = lire_ancien(sortie)

    try:
        nouveau = collecter()
    except Exception as e:
        print(f"  ✗ Échec collecte : {e}")
        if ancien:
            print(f"  → Conservation du dernier JSON valide ({ancien.get('total_jeux_uniques', 0)} jeux)")
            return
        raise

    ok, motif = valider(ancien, nouveau)
    if not ok:
        print(f"  ✗ Écriture refusée : {motif}")
        return

    print(f"  ✓ Validation : {motif}")
    Path("sources").mkdir(exist_ok=True)
    ecrire_atomique(sortie, json.dumps(nouveau, indent=2, ensure_ascii=False))

    n_obs = sum(1 for j in nouveau["jeux_uniques"].values() if j.get("obsolète"))
    print(f"✓ Écrit : {sortie}")
    print(f"  {nouveau['total_jeux_uniques']} jeu(x) unique(s) — {n_obs} obsolète(s)")


if __name__ == "__main__":
    main()
