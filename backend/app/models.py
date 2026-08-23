from typing import List, Optional
from pydantic import BaseModel


class JobPostingRequest(BaseModel):
    jobText: str


class EvidenceItem(BaseModel):
    category: str
    title: str
    detail: str
    severity: str
    status: Optional[str] = None
    organization: Optional[str] = None
    domain: Optional[str] = None


class ScamCheckResponse(BaseModel):
    score: int
    riskLevel: str
    flaggedReasons: List[str]
    extractedEntities: dict
    evidence: List[EvidenceItem] = []
    disclaimer: Optional[str] = (
        "Web information may be incomplete. Verify independently before taking action."
    )