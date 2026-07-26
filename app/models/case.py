from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass(frozen=True)
class ClassificationResult:
    request_type: str
    urgency: str
    confidence: float
    reasoning: str
    mode: str = "Fallback Rules"


@dataclass(frozen=True)
class WorkflowResult:
    status: str
    assigned_team: str
    assigned_agent: str
    assigned_manager: str
    follow_up_at: Optional[datetime]
    actions: list[str]
    review_required: bool
    review_reason: str
    current_stage: str
    progress_percent: int


@dataclass(frozen=True)
class IncomingRequest:
    requester_name: str
    requester_email: str
    source: str
    issue_category: str
    request_text: str