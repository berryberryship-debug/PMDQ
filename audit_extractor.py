#!/usr/bin/env python3
"""Extracteur amélioré : détecte claims par patterns + heuristiques."""
import re
from typing import List

from audit_schemas import FactualClaimTraceability, CialdiniTacticAudit


# Patterns pour détecter les affirmations chiffrées
PATTERNS_CHIFFRES = [
    # Montants en dollars
    re.compile(r"(\d+[.,]?\d*)\s*(milliards?|millions?|G\$|M\$|\$)", re.IGNORECASE),
    # Pourcentages
    re.compile(r"(\d+[.,]?\d*)\s*%"),
    # Ratios et fractions
    re.compile(r"(\d+[.,]?\d*)\s*(sur|/) ?(\d+[.,]?\d*)"),
    # Dates et horizons
    re.compile(r"(\d+)\s*(jours?|mois|ans?|semaines?)", re.IGNORECASE),
]

# Marqueurs d'absence de source
SOURCES_RECONNUES = (
    "isq", "statcan", "statistique canada", "revenu québec",
    "finances québec", "banque du canada", "budget",
    "mels", "msss", "inspq", "dgeq", "asfc",
    "https://", "http://", ".pdf", ".xlsx", ".csv",
)


def _a_une_source(phrase: str) -> bool:
    lower = phrase.lower()
    return any(s in lower for s in SOURCES_RECONNUES)


def extraire_claims(text: str) -> List[FactualClaimTraceability]:
    """Extrait les affirmations chiffrées par phrase."""
    claims = []
    phrases = re.split(r"[.!?]\s+", text)

    for phrase in phrases:
        phrase = phrase.strip()
        if not phrase or len(phrase) < 10:
            continue

        for pattern in PATTERNS_CHIFFRES:
            match = pattern.search(phrase)
            if match:
                a_source = _a_une_source(phrase)
                # Type : projection si "prévoit", "atteindra", "sera"
                if re.search(r"\b(prévoit|atteindra|sera|devrait|d'ici)\b", phrase, re.IGNORECASE):
                    claim_type = "economic_projection"
                elif re.search(r"\b(devrait|doit|il faut|nécessaire)\b", phrase, re.IGNORECASE):
                    claim_type = "normative_statement"
                else:
                    claim_type = "empirical_fact"

                claims.append(FactualClaimTraceability(
                    statement=phrase[:200],
                    claim_type=claim_type,
                    is_sourced=a_source,
                    source_reference=None if not a_source else "(détecté dans le texte)",
                ))
                break
    return claims


def extraire_tactiques(text: str) -> List[CialdiniTacticAudit]:
    """Détecte les tactiques de Cialdini par patterns étendus."""
    lower = text.lower()
    tactiques = []

    patterns = [
        ("Authority", "explicit",
         [r"les?\s+(économistes?|experts?|spécialistes?)",
          r"selon\s+(une|la|les)\s+(étude|recherche|source)",
          r"il est (prouvé|démontré|scientifiquement)"],
         "Le texte invoque une autorité pour renforcer sa crédibilité."),

        ("Scarcity", "possible",
         [r"(dernière|dernier)\s+(chance|occasion|fois)",
          r"il ne reste que",
          r"(maintenant|aujourd'hui) ou jamais",
          r"\b(urgent|urgence|immédiat)\b"],
         "Le texte crée un sentiment d'urgence ou de rareté."),

        ("Social_Proof", "possible",
         [r"tout le monde", r"la majorité", r"\d+\s*(millions|milliers) de (québécois|canadiens|gens)",
          r"chacun sait"],
         "Le texte invoque la preuve sociale ou le consensus."),

        ("Unity", "possible",
         [r"\bnous\b", r"\bnotre\b", r"\bensemble\b", r"\bcollectif\b"],
         "Le texte mobilise un sentiment d'appartenance collective."),

        ("Liking", "possible",
         [r"comme vous", r"vous qui", r"les vraies gens", r"le peuple"],
         "Le texte cherche à créer une connivence."),

        ("Consistency", "possible",
         [r"comme toujours", r"fidèle à", r"nous avons toujours"],
         "Le texte invoque la cohérence avec le passé."),

        ("Reciprocity", "possible",
         [r"nous vous offrons", r"en échange", r"gratuitement pour vous"],
         "Le texte mobilise la réciprocité."),
    ]

    for principle, presence, regexes, description in patterns:
        evidence = []
        for rx in regexes:
            m = re.search(rx, lower)
            if m:
                evidence.append(text[max(0, m.start()-20):m.end()+20].strip())
        if evidence:
            tactiques.append(CialdiniTacticAudit(
                principle=principle,
                presence=presence,
                application=description,
                evidence=evidence[:2],
            ))

    return tactiques


if __name__ == "__main__":
    test = """
    Tous les économistes sérieux s'accordent : le Québec doit agir.
    Il ne reste que 60 jours pour sécuriser nos PME. Notre fonds
    souverain est de 2,4 milliards $. Nous, Québécois, pouvons le faire.
    """
    print("[CLAIMS]")
    for c in extraire_claims(test):
        print(f"  {c.claim_type} | sourcé={c.is_sourced}")
        print(f"    « {c.statement} »")

    print("\n[TACTIQUES]")
    for t in extraire_tactiques(test):
        print(f"  {t.principle} ({t.presence}) : {t.evidence}")
