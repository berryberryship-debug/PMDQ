from typing import List, Literal, Optional
from pydantic import BaseModel, Field, ConfigDict


class CialdiniTacticAudit(BaseModel):
    model_config = ConfigDict(extra="forbid")
    principle: Literal["Reciprocity", "Scarcity", "Authority", "Consistency",
                       "Liking", "Social_Proof", "Unity"]
    presence: Literal["absent", "possible", "explicit"]
    application: str
    evidence: List[str] = Field(default_factory=list)


class FactualClaimTraceability(BaseModel):
    model_config = ConfigDict(extra="forbid")
    statement: str
    claim_type: Literal["empirical_fact", "economic_projection", "normative_statement"]
    is_sourced: bool
    source_reference: Optional[str] = None
    compliance_status: Optional[str] = None


class MessageExtraction(BaseModel):
    model_config = ConfigDict(extra="forbid")
    target_audience: str
    cialdini_audit: List[CialdiniTacticAudit]
    traceability_audit: List[FactualClaimTraceability]
    has_call_to_action: bool
    mentions_third_party_spending: bool
    raw_text: str = ""
