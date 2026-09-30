from schemas import MessageExtraction

SEUIL_DEPENSE_TIERS_QC = 1_000
SCORE_INITIAL = 100
PENALITE_PAR_AFFIRMATION_NON_SOURCEE = 10


def _normaliser(texte: str) -> str:
    """Retire les accents pour rendre les recherches insensibles."""
    remplacements = str.maketrans(
        "àâäéèêëîïôöùûüçÀÂÄÉÈÊËÎÏÔÖÙÛÜÇ",
        "aaaeeeeiioouuucAAAEEEEIIOOUUUC",
    )
    return texte.translate(remplacements).lower()


def enforce_traceability(extraction: MessageExtraction) -> MessageExtraction:
    for claim in extraction.traceability_audit:
        if claim.claim_type in ["empirical_fact", "economic_projection"]:
            if not claim.is_sourced:
                claim.compliance_status = ("BLOCAGE : Affirmation non sourcée. "
                                           "Rétrograder en hypothèse ou fournir une source.")
            elif claim.is_sourced and not claim.source_reference:
                claim.compliance_status = ("RÉVISION : Source déclarée mais référence "
                                           "manquante dans le texte.")
            else:
                claim.compliance_status = "CONFORME : Donnée traçable."
        else:
            claim.compliance_status = ("INFO : Jugement normatif "
                                       "(ne requiert pas de source stricte).")
    return extraction


def evaluate_electoral_risk(extraction: MessageExtraction) -> dict:
    risk = {"requires_imprimatur": False, "warnings": []}
    if extraction.has_call_to_action:
        risk["requires_imprimatur"] = True
        risk["warnings"].append("Un appel à l'action exige l'autorisation officielle "
                                "de l'agent officiel (Imprimatur).")
    if extraction.mentions_third_party_spending:
        risk["warnings"].append("Surveillance requise : Risque de qualification "
                                f"en dépense de tiers (> {SEUIL_DEPENSE_TIERS_QC} $).")
    return risk


def evaluate_gold_card_legal_risks(extraction: MessageExtraction) -> dict:
    legal = {
        "federal_barriers": [],
        "provincial_barriers_qc": [],
        "provincial_barriers_on": [],
        "electoral_risks": [],
        "financial_feasibility": {},
        "compliance_score": SCORE_INITIAL,
    }

    # Normaliser le texte (retire accents + minuscules)
    texte_brut = extraction.raw_text or " ".join(
        c.statement for c in extraction.traceability_audit
    )
    text_lower = _normaliser(texte_brut)

    facteurs_declenches = 0

    # --- Affirmations non sourcées : pénalité proportionnelle -----------
    unsourced = [c for c in extraction.traceability_audit
                 if c.claim_type in ["empirical_fact", "economic_projection"]
                 and not c.is_sourced]
    if unsourced:
        penalite = PENALITE_PAR_AFFIRMATION_NON_SOURCEE * len(unsourced)
        legal["federal_barriers"].append(
            "Loi canadienne sur la santé (art. 10-11) : interdit la facturation "
            f"supplémentaire pour services couverts. {len(unsourced)} affirmation(s) "
            f"non sourcée(s) détectée(s). Pénalité : -{penalite}.")
        legal["compliance_score"] -= penalite
        facteurs_declenches += 1

    # --- Accès prioritaire ----------------------------------------------
    priority_kw = ["prioritaire", "acces accelere", "moins de 48 heures",
                   "fast-track", "gold card", "a deux vitesses"]
    if any(kw in text_lower for kw in priority_kw):
        legal["provincial_barriers_qc"].append(
            "Loi sur les services de santé (RLRQ c. S-4.2, art. 108) : priorité "
            "aux résidents. Accès prioritaire payant = risque constitutionnel.")
        legal["provincial_barriers_on"].append(
            "Public Hospitals Act (Ontario, art. 29) : priorité aux résidents ontariens.")
        legal["compliance_score"] -= 30
        facteurs_declenches += 1

    # --- Non-résidents ---------------------------------------------------
    non_resident_kw = ["americain", "etranger", "non-resident", "touriste", "riche"]
    if any(kw in text_lower for kw in non_resident_kw):
        legal["provincial_barriers_qc"].append(
            "Loi sur l'assurance maladie (RLRQ c. A-29, art. 30-33) : services "
            "couverts réservés aux assurés (résidents).")
        legal["provincial_barriers_on"].append(
            "Health Insurance Act (Ontario, art. 27-30) : OHIP réservé aux résidents.")
        legal["compliance_score"] -= 25
        facteurs_declenches += 1

    # --- CTA électoral ---------------------------------------------------
    if extraction.has_call_to_action:
        legal["electoral_risks"].append(
            f"Loi électorale (RLRQ c. E-3.3, art. 427-430) : dépenses de tiers "
            f"> {SEUIL_DEPENSE_TIERS_QC} $ = déclaration obligatoire.")
        legal["electoral_risks"].append(
            "Règlement sur la publicité électorale (art. 15) : imprimatur requis.")
        legal["compliance_score"] -= 15
        facteurs_declenches += 1

    # --- Financement étranger --------------------------------------------
    foreign_kw = ["financement", "dons", "contributions", "americain", "etranger"]
    if extraction.mentions_third_party_spending or any(kw in text_lower for kw in foreign_kw):
        legal["electoral_risks"].append(
            "Loi sur le financement des partis (art. 75) : interdiction de "
            "contributions par des non-résidents.")
        legal["compliance_score"] -= 20
        facteurs_declenches += 1

    # --- Pénalité de cumul -----------------------------------------------
    if facteurs_declenches >= 3:
        penalite_cumul = (facteurs_declenches - 2) * 10
        legal["compliance_score"] -= penalite_cumul
        legal["federal_barriers"].append(
            f"⚠ Cumul de {facteurs_declenches} facteurs de risque : "
            f"pénalité additionnelle de -{penalite_cumul} points.")

    legal["financial_feasibility"] = _chiffrer_modele_gold_card()

    legal["compliance_score"] = max(0, legal["compliance_score"])
    score = legal["compliance_score"]
    if score >= 80:
        legal["verdict"] = "CONFORME"
    elif score >= 50:
        legal["verdict"] = "RISQUE MODÉRÉ"
    else:
        legal["verdict"] = "RISQUE ÉLEVÉ"
    return legal


def _chiffrer_modele_gold_card(
    prix_gold_card: float = 50_000,
    franchise_chirurgie: float = 10_000,
    cout_moyen_chirurgie: float = 25_000,
    volume_chirurgies_par_patient: float = 1.2,
    patients_cible_an3: int = 3_000,
) -> dict:
    hypothese = {
        "prix_gold_card": prix_gold_card,
        "franchise_par_chirurgie": franchise_chirurgie,
        "cout_moyen_chirurgie": cout_moyen_chirurgie,
        "volume_chirurgies_par_patient": volume_chirurgies_par_patient,
        "patients_cible_an3": patients_cible_an3,
    }
    revenus = (patients_cible_an3 * prix_gold_card
               + patients_cible_an3 * volume_chirurgies_par_patient * franchise_chirurgie)
    couts = patients_cible_an3 * volume_chirurgies_par_patient * cout_moyen_chirurgie
    marge = revenus - couts
    marge_par_patient = marge / patients_cible_an3 if patients_cible_an3 else 0
    return {
        "hypothese": hypothese,
        "revenus_annuels_millions": round(revenus / 1_000_000, 2),
        "couts_directs_millions": round(couts / 1_000_000, 2),
        "marge_brute_millions": round(marge / 1_000_000, 2),
        "marge_brute_par_patient": round(marge_par_patient, 2),
        "faisabilite": "OUI" if marge > 0 else "NON",
    }
