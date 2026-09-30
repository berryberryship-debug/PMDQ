"""pmdq_bridge.py -- Pont entre Volet 17 et PMDQ v2.6.3."""
import json
import re
from pathlib import Path

from engines import ExtractionEngine
from rules import (
    enforce_traceability,
    evaluate_electoral_risk,
    evaluate_gold_card_legal_risks,
)


CHEMIN_EMPREINTE = Path(__file__).parent / "data" / "empreinte_pmdq.json"


def charger_empreinte():
    if not CHEMIN_EMPREINTE.exists():
        raise FileNotFoundError(str(CHEMIN_EMPREINTE))
    return json.loads(CHEMIN_EMPREINTE.read_text(encoding="utf-8"))


def _extraire_nombres(texte):
    motif = re.compile(r"\b(\d+(?:[.,]\d+)?)\b")
    nombres = []
    for m in motif.finditer(texte):
        brut = m.group(1).replace(",", ".")
        try:
            valeur = float(brut)
            if valeur >= 1.0:
                nombres.append((valeur, m.group(0)))
        except ValueError:
            continue
    return nombres


def verifier_empreinte(texte, tolerance=0.001):
    empreinte = charger_empreinte()
    resultat = {
        "valeurs_obsoletes_detectees": [],
        "valeurs_conformes_detectees": [],
    }
    nombres = _extraire_nombres(texte)
    for incompat in empreinte["incompatibilites_connues"]["valeurs_a_ne_jamais_accepter"]:
        cible = incompat["valeur_fausse"]
        for valeur, brut in nombres:
            if abs(valeur - cible) < tolerance:
                resultat["valeurs_obsoletes_detectees"].append({
                    "valeur_trouvee": valeur,
                    "contexte": incompat["contexte"],
                    "valeur_correcte": incompat["valeur_correcte"],
                    "extrait": brut,
                })
    for nom, cible in empreinte["invariants_numeriques"].items():
        if cible < 1.0:
            continue
        for valeur, brut in nombres:
            if abs(valeur - cible) < tolerance:
                resultat["valeurs_conformes_detectees"].append({
                    "nom": nom,
                    "valeur": cible,
                    "extrait": brut,
                })
    resultat["conforme"] = len(resultat["valeurs_obsoletes_detectees"]) == 0
    return resultat


def verifier_invariants(texte):
    texte_norm = texte.lower()
    absolus = [
        r"\btoujours\b", r"\bjamais\b", r"\bcertain\b",
        r"\bgaranti\b", r"\binfaillible\b",
        r"\b100\s*%\s*de\s*succes",
        r"\bsans\s+aucun\s+doute\b",
    ]
    absolus_trouves = []
    for motif in absolus:
        for m in re.finditer(motif, texte_norm):
            extrait = texte[max(0, m.start() - 20): m.end() + 20].strip()
            absolus_trouves.append({"motif": m.group(0), "extrait": extrait})
    montants = re.findall(r"\d[\d\s,\.]*\s*(?:G\$|M\$|\$)", texte)
    mentions_ventilation = any(
        mot in texte_norm
        for mot in ["recette", "reaffectation", "reaffectations",
                    "economie", "economies", "conditionnel"]
    )
    return {
        "I2_statut_descriptif": {
            "conforme": len(absolus_trouves) == 0,
            "absolus_detectes": absolus_trouves,
        },
        "I7_ventilation": {
            "conforme": (len(montants) == 0) or mentions_ventilation,
            "montants_detectes": montants,
            "ventilation_mentionnee": mentions_ventilation,
        },
    }


def audit_integre(texte):
    engine = ExtractionEngine()
    raw = engine.extract(texte)
    validated = enforce_traceability(raw)
    electoral = evaluate_electoral_risk(validated)
    gold = evaluate_gold_card_legal_risks(validated)
    empreinte = verifier_empreinte(texte)
    invariants = verifier_invariants(texte)

    verdicts = {
        "semantique": gold["verdict"],
        "empreinte": "CONFORME" if empreinte["conforme"] else "RUPTURE",
        "invariants": (
            "CONFORME"
            if invariants["I2_statut_descriptif"]["conforme"]
            and invariants["I7_ventilation"]["conforme"]
            else "NON CONFORME"
        ),
    }

    verdict_global = "CONFORME"
    if verdicts["empreinte"] != "CONFORME":
        verdict_global = "RUPTURE DE VERSION"
    elif verdicts["invariants"] != "CONFORME":
        verdict_global = "NON CONFORME"
    elif verdicts["semantique"] == "RISQUE ELEVE":
        verdict_global = "RISQUE ELEVE"
    elif verdicts["semantique"] == "RISQUE MODERE":
        verdict_global = "RISQUE MODERE"

    return {
        "verdict_global": verdict_global,
        "verdicts_partiels": verdicts,
        "semantique": {
            "score": gold["compliance_score"],
            "verdict": gold["verdict"],
            "public_cible": validated.target_audience,
            "nb_affirmations": len(validated.traceability_audit),
            "nb_non_sourcees": sum(
                1 for c in validated.traceability_audit
                if c.claim_type != "normative_statement" and not c.is_sourced
            ),
            "imprimatur_requis": electoral["requires_imprimatur"],
        },
        "empreinte": empreinte,
        "invariants": invariants,
    }


def afficher_rapport_integre(rapport):
    sep = "=" * 72
    print(sep)
    print("RAPPORT D'AUDIT INTEGRE -- " + rapport["verdict_global"])
    print(sep)
    print("\n[ AUDIT SEMANTIQUE (Volet 17) ]")
    s = rapport["semantique"]
    print("  Score            : " + str(s["score"]) + "/100")
    print("  Verdict          : " + s["verdict"])
    print("  Public cible     : " + s["public_cible"])
    print("  Affirmations     : " + str(s["nb_affirmations"]) + " (dont " + str(s["nb_non_sourcees"]) + " non sourcees)")
    print("  Imprimatur       : " + str(s["imprimatur_requis"]))
    print("\n[ CONFORMITE EMPREINTE PMDQ v2.6.3 ]")
    e = rapport["empreinte"]
    if e["conforme"]:
        print("  OK -- Aucune valeur obsolete detectee.")
    else:
        print("  ALERTE -- VALEURS OBSOLETES DETECTEES :")
        for v in e["valeurs_obsoletes_detectees"]:
            print("    - Trouve " + str(v["valeur_trouvee"]) + " (" + v["contexte"] + ")")
            print("      Valeur correcte : " + str(v["valeur_correcte"]))
    if e["valeurs_conformes_detectees"]:
        print("  OK -- " + str(len(e["valeurs_conformes_detectees"])) + " valeur(s) conforme(s).")
    print("\n[ INVARIANTS PMDQ ]")
    inv = rapport["invariants"]
    i2 = inv["I2_statut_descriptif"]
    i7 = inv["I7_ventilation"]
    print("  I2 (statut descriptif) : " + ("CONFORME" if i2["conforme"] else "NON CONFORME"))
    for a in i2["absolus_detectes"]:
        print("    - Absolu interdit : " + a["motif"])
    print("  I7 (ventilation) : " + ("CONFORME" if i7["conforme"] else "NON CONFORME"))
    if not i7["conforme"]:
        print("    - " + str(len(i7["montants_detectes"])) + " montant(s) sans ventilation")
    print("\n" + sep)
    print("VERDICT GLOBAL : " + rapport["verdict_global"])
    print(sep)


if __name__ == "__main__":
    exemple = (
        "Le programme FQBC a un ratio RESEAU-NARP-001 de 1.5119 et un "
        "decaisement total de 8.1 G$. Le taux est de 96.43 pourcent. "
        "Ce programme garantit toujours un succes a 100 pourcent."
    )
    rapport = audit_integre(exemple)
    afficher_rapport_integre(rapport)
