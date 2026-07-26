from datetime import datetime, timedelta

from app.models.case import WorkflowResult


TEAM_ROUTING = {
    "Orders & Returns": {
        "team": "Orders & Returns Team",
        "agent": "Orders - Support Agent",
        "manager": "Orders - Manager",
    },
    "Account Related": {
        "team": "Account Management Team",
        "agent": "Accounts - Support Agent",
        "manager": "Accounts - Manager",
    },
    "Billing & Payments": {
        "team": "Billing & Payments Team",
        "agent": "Billing - Support Agent",
        "manager": "Billing - Manager",
    },
    "Technical Support": {
        "team": "Technical Support Team",
        "agent": "Technical - Support Agent",
        "manager": "Technical - Manager",
    },
    "Service Appointment": {
        "team": "Service Operations Team",
        "agent": "Service - Support Agent",
        "manager": "Service - Manager",
    },
    "General Query": {
        "team": "Customer Support Team",
        "agent": "General - Support Agent",
        "manager": "General - Manager",
    },
}


def execute_workflow(request_type: str, urgency: str, issue_category: str = "General Query") -> WorkflowResult:
    now = datetime.now()
    routing = TEAM_ROUTING.get(issue_category, TEAM_ROUTING["General Query"])

    if urgency in ["High", "Critical"] or request_type in ["Complaint", "Urgent Escalation"]:
        return WorkflowResult(
            status="Escalated to Manager",
            assigned_team=routing["team"],
            assigned_agent=routing["agent"],
            assigned_manager=routing["manager"],
            follow_up_at=now + timedelta(hours=2),
            actions=[
                "Created new customer ticket",
                "Classified request category and priority",
                "Assigned ticket to responsible team",
                "Escalated ticket to manager approval queue",
            ],
            review_required=True,
            review_reason="High or critical priority requires manager approval before agent action.",
            current_stage="Manager Review",
            progress_percent=35,
        )

    if urgency == "Medium":
        return WorkflowResult(
            status="Assigned to Agent",
            assigned_team=routing["team"],
            assigned_agent=routing["agent"],
            assigned_manager=routing["manager"],
            follow_up_at=now + timedelta(hours=24),
            actions=[
                "Created new customer ticket",
                "Classified request category and priority",
                "Assigned ticket to agent queue",
                "Set SLA follow-up timer",
            ],
            review_required=False,
            review_reason="Medium priority request can be handled by assigned agent.",
            current_stage="Assigned",
            progress_percent=25,
        )

    return WorkflowResult(
        status="Assigned to Agent",
        assigned_team=routing["team"],
        assigned_agent=routing["agent"],
        assigned_manager=routing["manager"],
        follow_up_at=None,
        actions=[
            "Created new customer ticket",
            "Classified request category and priority",
            "Assigned ticket to agent queue",
            "Prepared standard customer response",
        ],
        review_required=False,
        review_reason="Low priority request can be handled by assigned agent.",
        current_stage="Assigned",
        progress_percent=25,
    )