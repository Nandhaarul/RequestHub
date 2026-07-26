import json
import re
from typing import Any

from app.config.settings import (
    GEMINI_API_KEY,
    GEMINI_MODEL,
    OPENAI_API_KEY,
    OPENAI_MODEL,
    REQUEST_TYPES,
    URGENCY_LEVELS,
)
from app.models.case import ClassificationResult

try:
    from google import genai
except ImportError:
    genai = None

try:
    from openai import OpenAI
except ImportError:
    OpenAI = None


CLASSIFICATION_PROMPT = """
You are an operations workflow classifier.

Classify the customer request into exactly one request_type:
- Complaint
- General Enquiry
- Service Request
- Urgent Escalation

Also assign urgency:
- Low
- Medium
- High
- Critical

Guidance:
- Complaint: dissatisfaction, unfair treatment, bad experience, refund, cancellation complaint, repeated failure.
- General Enquiry: customer is asking for information only.
- Service Request: customer needs repair, technical support, appointment, cancellation assistance, account support, or operational action.
- Urgent Escalation: business-critical impact, legal risk, severe outage, payment processing blocked, supervisor escalation.

Return ONLY valid JSON:
{
  "request_type": "...",
  "urgency": "...",
  "confidence": 0.0,
  "reasoning": "short explanation"
}
"""


def classify_request(request_text: str) -> ClassificationResult:
    if GEMINI_API_KEY and genai is not None:
        try:
            return _classify_with_gemini(request_text)
        except Exception as exc:
            fallback = _classify_with_rules(request_text)
            return ClassificationResult(
                request_type=fallback.request_type,
                urgency=fallback.urgency,
                confidence=fallback.confidence,
                reasoning=f"Gemini classification unavailable. {fallback.reasoning}",
                mode="Fallback Rules",
            )

    if OPENAI_API_KEY and OpenAI is not None:
        try:
            return _classify_with_openai(request_text)
        except Exception:
            fallback = _classify_with_rules(request_text)
            return ClassificationResult(
                request_type=fallback.request_type,
                urgency=fallback.urgency,
                confidence=fallback.confidence,
                reasoning=f"OpenAI classification unavailable. {fallback.reasoning}",
                mode="Fallback Rules",
            )

    return _classify_with_rules(request_text)


def _classify_with_gemini(request_text: str) -> ClassificationResult:
    client = genai.Client(api_key=GEMINI_API_KEY)
    response = client.models.generate_content(
        model=GEMINI_MODEL,
        contents=f"{CLASSIFICATION_PROMPT}\n\nCustomer request:\n{request_text}",
    )

    data = _json_from_text(response.text or "{}")
    result = _normalize_classification(data)

    return ClassificationResult(
        request_type=result.request_type,
        urgency=result.urgency,
        confidence=result.confidence,
        reasoning=result.reasoning,
        mode="Gemini",
    )


def _classify_with_openai(request_text: str) -> ClassificationResult:
    client = OpenAI(api_key=OPENAI_API_KEY)
    response = client.chat.completions.create(
        model=OPENAI_MODEL,
        messages=[
            {"role": "system", "content": CLASSIFICATION_PROMPT},
            {"role": "user", "content": request_text},
        ],
        temperature=0.2,
    )

    raw_text = response.choices[0].message.content or "{}"
    data = _json_from_text(raw_text)
    result = _normalize_classification(data)

    return ClassificationResult(
        request_type=result.request_type,
        urgency=result.urgency,
        confidence=result.confidence,
        reasoning=result.reasoning,
        mode="OpenAI",
    )


def _classify_with_rules(request_text: str) -> ClassificationResult:
    text = request_text.lower()

    urgent_terms = [
        "urgent",
        "immediately",
        "critical",
        "legal",
        "supervisor",
        "escalate",
        "escalation",
        "account locked",
        "locked out",
        "cannot process",
        "business stopped",
        "severe outage",
    ]

    complaint_terms = [
        "complaint",
        "angry",
        "unhappy",
        "disappointed",
        "unfair",
        "bad experience",
        "poor service",
        "not acceptable",
        "frustrated",
        "refund",
        "charged twice",
        "price that i am paying",
        "paying",
        "wasn't able",
        "wasnt able",
        "not able",
        "could not",
        "need a fix",
        "fix as soon as possible",
        "as soon as possible",
        "this is very unfair",
    ]

    service_terms = [
        "network down",
        "network was down",
        "internet down",
        "internet was down",
        "not working",
        "service issue",
        "repair",
        "install",
        "installation",
        "appointment",
        "technician",
        "schedule",
        "connection issue",
        "outage",
        "technical support",
        "cancel",
        "cancelling",
        "order",
        "account",
        "login",
    ]

    enquiry_terms = [
        "what documents",
        "can you tell me",
        "how do i",
        "what is",
        "where can i",
        "information",
        "details",
        "clarification",
    ]

    urgent_score = _score_terms(text, urgent_terms)
    complaint_score = _score_terms(text, complaint_terms)
    service_score = _score_terms(text, service_terms)
    enquiry_score = _score_terms(text, enquiry_terms)

    if urgent_score >= 1 and any(
        term in text
        for term in ["immediately", "critical", "legal", "supervisor", "escalate"]
    ):
        return ClassificationResult(
            request_type="Urgent Escalation",
            urgency="Critical",
            confidence=0.88,
            reasoning="Detected business-critical or escalation-related language.",
            mode="Fallback Rules",
        )

    if complaint_score >= 1:
        return ClassificationResult(
            request_type="Complaint",
            urgency="High",
            confidence=0.86,
            reasoning="Detected dissatisfaction, unfairness, payment concern, or complaint-style wording.",
            mode="Fallback Rules",
        )

    if service_score >= 1:
        return ClassificationResult(
            request_type="Service Request",
            urgency="Medium",
            confidence=0.82,
            reasoning="Detected a request that needs support or operational action.",
            mode="Fallback Rules",
        )

    if enquiry_score >= 1:
        return ClassificationResult(
            request_type="General Enquiry",
            urgency="Low",
            confidence=0.78,
            reasoning="Detected an information-seeking enquiry.",
            mode="Fallback Rules",
        )

    return ClassificationResult(
        request_type="General Enquiry",
        urgency="Low",
        confidence=0.7,
        reasoning="No strong complaint, service, or escalation signal detected.",
        mode="Fallback Rules",
    )


def _json_from_text(text: str) -> dict[str, Any]:
    cleaned = text.strip()

    if cleaned.startswith("```"):
        cleaned = re.sub(r"^```(?:json)?", "", cleaned).strip()
        cleaned = re.sub(r"```$", "", cleaned).strip()

    match = re.search(r"\{.*\}", cleaned, flags=re.DOTALL)
    if match:
        cleaned = match.group(0)

    return json.loads(cleaned)


def _score_terms(text: str, terms: list[str]) -> int:
    return sum(1 for term in terms if term in text)


def _normalize_classification(data: dict[str, Any]) -> ClassificationResult:
    request_type = str(data.get("request_type", "General Enquiry")).strip()
    urgency = str(data.get("urgency", "Low")).strip()

    if request_type not in REQUEST_TYPES:
        request_type = "General Enquiry"

    if urgency not in URGENCY_LEVELS:
        urgency = "Low"

    try:
        confidence = float(data.get("confidence", 0.7))
    except (TypeError, ValueError):
        confidence = 0.7

    confidence = max(0.0, min(confidence, 1.0))
    reasoning = str(data.get("reasoning", "Classification completed.")).strip()

    return ClassificationResult(
        request_type=request_type,
        urgency=urgency,
        confidence=confidence,
        reasoning=reasoning or "Classification completed.",
        mode="AI",
    )