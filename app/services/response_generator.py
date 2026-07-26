from app.config.settings import GEMINI_API_KEY, GEMINI_MODEL

try:
    from google import genai
except ImportError:
    genai = None


def generate_response(
    request_text: str,
    request_type: str,
    urgency: str,
    issue_category: str = "General Query",
    assigned_team: str = "Customer Support Team",
) -> str:
    if urgency == "Low" and GEMINI_API_KEY and genai is not None:
        try:
            return _generate_low_priority_ai_response(
                request_text=request_text,
                issue_category=issue_category,
                assigned_team=assigned_team,
            )
        except Exception:
            return _generate_template_response(request_type, urgency)

    return _generate_template_response(request_type, urgency)


def _generate_low_priority_ai_response(
    request_text: str,
    issue_category: str,
    assigned_team: str,
) -> str:
    client = genai.Client(api_key=GEMINI_API_KEY)

    prompt = f"""
You are a customer support assistant.

Write a concise, professional response for a low-priority customer request.

Rules:
- Acknowledge the customer's request.
- Mention that it has been routed to the correct team.
- Do not promise refunds, cancellations, compensation, or account changes unless confirmed.
- Keep it under 120 words.
- Tone should be helpful and calm.

Issue category: {issue_category}
Assigned team: {assigned_team}

Customer request:
{request_text}
"""

    response = client.models.generate_content(
        model=GEMINI_MODEL,
        contents=prompt,
    )

    return (response.text or "").strip() or _generate_template_response("General Enquiry", "Low")


def _generate_template_response(request_type: str, urgency: str) -> str:
    if request_type == "Complaint":
        return f"""Dear Customer,

Thank you for bringing this issue to our attention. We are sorry to hear about your experience.

Your case has been marked as {urgency} priority and escalated to the appropriate team for review. Our team will investigate the matter and follow up with you shortly.

Regards,
Customer Support Team"""

    if request_type == "General Enquiry":
        return """Dear Customer,

Thank you for reaching out. We have received your enquiry and routed it to the appropriate support team.

Please let us know if you need any additional clarification.

Regards,
Customer Support Team"""

    if request_type == "Service Request":
        return """Dear Customer,

Thank you for submitting your service request.

We have routed your request to the appropriate department. A team member will review the details and follow up according to the applicable service timeline.

Regards,
Service Operations Team"""

    return """Dear Customer,

Thank you for contacting us.

Your request has been flagged for urgent human review. A supervisor or specialist will review this case before any automated resolution is attempted.

Regards,
Escalation Support Team"""