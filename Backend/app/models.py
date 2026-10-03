from pydantic import BaseModel


# ===== Vamsi (B1) =====


# ===== Abhyuday (B2) =====
# Exchange status is always one of:
#   proposed, accepted, locked, completed, declined


class SkillRef(BaseModel):
    skill_id: str
    label: str


class PersonRef(BaseModel):
    id: str
    name: str
    file_code: str | None = None


class TermsIn(BaseModel):
    requester_gives: str
    recipient_gives: str
    when: str
    where: str
    mode: str
    note: str | None = None


class ExchangeIn(BaseModel):
    recipient_id: str
    requester_listing_id: str
    recipient_listing_id: str
    terms: TermsIn
    source: str  # "browse" or "match"


class ExchangeOut(BaseModel):
    id: str
    status: str
    created_at: str
    source: str
    requester: PersonRef
    recipient: PersonRef
    terms: TermsIn
    locked_at: str | None = None
    requester_completed: bool
    recipient_completed: bool
    thread_id: str | None = None


class ExchangeSummary(BaseModel):
    id: str
    status: str
    other: PersonRef
    summary: str
    created_at: str


class LedgerOut(BaseModel):
    incoming: list[ExchangeSummary]
    pending: list[ExchangeSummary]
    active: list[ExchangeSummary]
    closed: list[ExchangeSummary]


class Breakdown(BaseModel):
    skills: int
    timing: int
    location: int


class MatchOut(BaseModel):
    user_id: str
    name: str
    file_code: str | None = None
    score: int
    mutual: bool
    they_give: SkillRef
    you_give: SkillRef
    breakdown: Breakdown


class RespondIn(BaseModel):
    action: str  # "accept" or "decline"
    reason: str | None = None


class ReviewIn(BaseModel):
    exchange_id: str
    stars: int
    note: str | None = None


class ReviewOut(BaseModel):
    id: str
    exchange_id: str
    reviewer: PersonRef
    stars: int
    note: str | None = None
    created_at: str
