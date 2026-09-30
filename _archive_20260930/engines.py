"""
Moteur d'extraction 100 % déterministe. Aucune clé API, aucun réseau.
"""
import re
from typing import List

from schemas import (
    CialdiniTacticAudit,
    FactualClaimTraceability,
    MessageExtraction,
)


CIALDINI_PATTERNS = {
    "Reciprocity": [r"\bgratuit", r"\boffert", r"\bcadeau", r"\bdon", r"\bcontrepartie"],
    "Scarcity": [r"\bdernière chance", r"\bplaces limitées", r"\burgent", r"\bmenace",
                 r"\bà deux vitesses", r"\baccès prioritaire", r"\baccéléré", r"\bmoins de 48 heures"],
    "Authority": [r"\bselon un rapport", r"\bexperts", r"\bofficiel", r"\bétude",
                  r"\bconseil de la santé", r"\bgouvernement", r"\bministre"],
    "Consistency": [r"\bnous avons toujours", r"\bcomme promis", r"\bnotre engagement"],
    "Liking": [r"\bnos familles", r"\bnos enfants", r"\bnos aînés", r"\bnos concitoyens"],
    "Social_Proof": [r"\bla majorité", r"\bdes milliers", r"\bplus de \d+", r"\bde nombreux"],
    "Unity": [r"\bnous", r"\bnotre nation", r"\bnotre peuple", r"\bensemble"],
}

CTA_PATTERNS = [r"\bsignez", r"\bmobilisez", r"\bvotez", r"\bjoignez",
                r"\bsoutenez", r"\bappuyez", r"\bavant le vote", r"\bpétition"]

THIRD_PARTY_PATTERNS = [r"\bfinancement", r"\bdons", r"\bcontributions",
                        r"\bpublicité", r"\bcampagne", r"\btiers"]

NUMERIC_RE = re.compile(
    r"(\d[\d\s,\.]*)\s*(%|\$|M\$|G\$|millions?|milliards?|dollars?|patients?|personnes?|ans?)",
    re.IGNORECASE,
)
SOURCE_RE = re.compile(
    r"(selon\s+[^,\.\n]+|d'après\s+[^,\.\n]+|rapport\s+[^,\.\n]+|"
    r"étude\s+[^,\.\n]+|source\s*:\s*[^,\.\n]+|réf\.?\s*:\s*[^,\.\n]+|en\s+\d{4})",
    re.IGNORECASE,
)
NORMATIVE_RE = re.compile(
    r"\b(doit|devrait|il faut|nécessaire|essentiel|mérite|inacceptable|"
    r"scandaleux|injuste|équitable|universel)\b",
    re.IGNORECASE,
)

# --- NOUVEAU : séparateurs d'affirmations ---
# En plus de la ponctuation forte (. ! ?), on coupe aussi sur les
# locutions causales/explicatives qui introduisent un fait distinct
# ("à cause de", "en raison de", "grâce à", "parce que", "puisque").
# Cela permet de détecter séparément une affirmation non sourcée
# introduite par une proposition causale.
CLAIM_SEPARATORS = re.compile(
    r"[\.!?]+"
    r"|\s+à cause de\s+"
    r"|\s+en raison de\s+"
    r"|\s+grâce à\s+"
    r"|\s+parce que\s+"
    r"|\s+puisque\s+",
    re.IGNORECASE,
)


class ExtractionEngine:
    def __init__(self, model: str = None, temperature: float = None):
        self.model = model
        self.temperature = temperature

    def extract(self, text: str) -> MessageExtraction:
        text = re.sub(r"\s+", " ", text).strip()
        return MessageExtraction(
            target_audience=self._target_audience(text),
            cialdini_audit=self._cialdini(text),
            traceability_audit=self._claims(text),
            has_call_to_action=self._has_cta(text),
            mentions_third_party_spending=self._has_third_party(text),
            raw_text=text,
        )

    def _target_audience(self, text: str) -> str:
        t = text.lower()
        if "vote" in t or "pétition" in t:
            return "Électeurs / citoyens mobilisables"
        if "famille" in t or "enfants" in t:
            return "Familles"
        if "patient" in t or "santé" in t:
            return "Patients / usagers du système de santé"
        return "Grand public"

    def _cialdini(self, text: str) -> List[CialdiniTacticAudit]:
        t = text.lower()
        resultats = []
        for principle, patterns in CIALDINI_PATTERNS.items():
            matches = []
            for pattern in patterns:
                for m in re.finditer(pattern, t):
                    matches.append(text[max(0, m.start() - 30): m.end() + 30].strip())
            if not matches:
                p, a = "absent", "Aucun signal détecté."
            elif len(matches) == 1:
                p, a = "possible", f"Un signal faible de {principle}."
            else:
                p, a = "explicit", f"Signaux multiples de {principle}."
            resultats.append(CialdiniTacticAudit(
                principle=principle, presence=p,
                application=a, evidence=matches[:3],
            ))
        return resultats

    def _claims(self, text: str) -> List[FactualClaimTraceability]:
        claims = []
        # Découpage sur ponctuation forte + locutions causales
        for sentence in CLAIM_SEPARATORS.split(text):
            sentence = sentence.strip()
            if len(sentence) < 15:
                continue
            has_number = bool(NUMERIC_RE.search(sentence))
            has_source = bool(SOURCE_RE.search(sentence))
            is_normative = bool(NORMATIVE_RE.search(sentence))

            if has_number and not is_normative:
                ct = "economic_projection" if "$" in sentence else "empirical_fact"
                ref = SOURCE_RE.search(sentence)
                claims.append(FactualClaimTraceability(
                    statement=sentence,
                    claim_type=ct,
                    is_sourced=has_source,
                    source_reference=ref.group(0) if ref else None,
                ))
            elif is_normative:
                claims.append(FactualClaimTraceability(
                    statement=sentence,
                    claim_type="normative_statement",
                    is_sourced=False,
                    source_reference=None,
                ))
        return claims

    def _has_cta(self, text: str) -> bool:
        return any(re.search(p, text, re.IGNORECASE) for p in CTA_PATTERNS)

    def _has_third_party(self, text: str) -> bool:
        return any(re.search(p, text, re.IGNORECASE) for p in THIRD_PARTY_PATTERNS)
