import json
from datetime import datetime

import pandas as pd

from app.database.connection import get_connection
from app.models.case import ClassificationResult, IncomingRequest, WorkflowResult


def save_case(
    incoming_request: IncomingRequest,
    classification: ClassificationResult,
    workflow: WorkflowResult,
    draft_response: str,
) -> None:
    follow_up_at = workflow.follow_up_at.isoformat(timespec="minutes") if workflow.follow_up_at else None
    approval_status = "Pending" if workflow.review_required else "Not Required"

    with get_connection() as conn:
        conn.execute(
            """
            INSERT INTO cases (
                created_at, requester_name, requester_email, source, issue_category,
                request_text, request_type, urgency, confidence, reasoning, status,
                assigned_team, assigned_agent, assigned_manager, follow_up_at,
                draft_response, action_summary, review_required, review_reason,
                current_stage, progress_percent, manager_approval_status,
                manager_approval_note, override_applied, override_note
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                datetime.now().isoformat(timespec="minutes"),
                incoming_request.requester_name,
                incoming_request.requester_email,
                incoming_request.source,
                incoming_request.issue_category,
                incoming_request.request_text,
                classification.request_type,
                classification.urgency,
                classification.confidence,
                classification.reasoning,
                workflow.status,
                workflow.assigned_team,
                workflow.assigned_agent,
                workflow.assigned_manager,
                follow_up_at,
                draft_response,
                json.dumps(workflow.actions),
                1 if workflow.review_required else 0,
                workflow.review_reason,
                workflow.current_stage,
                workflow.progress_percent,
                approval_status,
                None,
                0,
                None,
            ),
        )
        conn.commit()


def load_cases() -> pd.DataFrame:
    with get_connection() as conn:
        return pd.read_sql_query("SELECT * FROM cases ORDER BY id DESC", conn)


def load_customer_cases(requester_email: str) -> pd.DataFrame:
    with get_connection() as conn:
        return pd.read_sql_query(
            """
            SELECT * FROM cases
            WHERE LOWER(requester_email) = LOWER(?)
            ORDER BY id DESC
            """,
            conn,
            params=(requester_email,),
        )


def load_agent_cases(agent_name: str | None = None) -> pd.DataFrame:
    with get_connection() as conn:
        if agent_name:
            return pd.read_sql_query(
                """
                SELECT * FROM cases
                WHERE assigned_agent = ?
                  AND review_required = 0
                ORDER BY id DESC
                """,
                conn,
                params=(agent_name,),
            )

        return pd.read_sql_query(
            """
            SELECT * FROM cases
            WHERE assigned_agent IS NOT NULL
              AND review_required = 0
            ORDER BY id DESC
            """,
            conn,
        )


def load_manager_cases(manager_name: str | None = None) -> pd.DataFrame:
    with get_connection() as conn:
        if manager_name:
            return pd.read_sql_query(
                """
                SELECT * FROM cases
                WHERE assigned_manager = ?
                ORDER BY id DESC
                """,
                conn,
                params=(manager_name,),
            )

        return pd.read_sql_query(
            """
            SELECT * FROM cases
            WHERE assigned_manager IS NOT NULL
            ORDER BY id DESC
            """,
            conn,
        )


def load_review_cases() -> pd.DataFrame:
    with get_connection() as conn:
        return pd.read_sql_query(
            """
            SELECT * FROM cases
            WHERE review_required = 1
               OR status IN ('Escalated to Manager', 'Manager Review')
               OR manager_approval_status = 'Pending'
            ORDER BY id DESC
            """,
            conn,
        )


def update_agent_progress(
    case_id: int,
    current_stage: str,
    progress_percent: int,
    status: str,
    note: str,
) -> None:
    with get_connection() as conn:
        conn.execute(
            """
            UPDATE cases
            SET current_stage = ?,
                progress_percent = ?,
                status = ?,
                override_note = ?
            WHERE id = ?
            """,
            (
                current_stage,
                progress_percent,
                status,
                note,
                case_id,
            ),
        )
        conn.commit()


def update_manager_approval(
    case_id: int,
    approval_status: str,
    manager_note: str,
    status: str,
    current_stage: str,
    progress_percent: int,
    review_required: bool,
) -> None:
    with get_connection() as conn:
        conn.execute(
            """
            UPDATE cases
            SET manager_approval_status = ?,
                manager_approval_note = ?,
                status = ?,
                current_stage = ?,
                progress_percent = ?,
                review_required = ?
            WHERE id = ?
            """,
            (
                approval_status,
                manager_note,
                status,
                current_stage,
                progress_percent,
                1 if review_required else 0,
                case_id,
            ),
        )
        conn.commit()


def update_case_override(
    case_id: int,
    request_type: str,
    urgency: str,
    status: str,
    assigned_team: str,
    review_required: bool,
    override_note: str,
) -> None:
    with get_connection() as conn:
        conn.execute(
            """
            UPDATE cases
            SET request_type = ?,
                urgency = ?,
                status = ?,
                assigned_team = ?,
                review_required = ?,
                override_applied = 1,
                override_note = ?
            WHERE id = ?
            """,
            (
                request_type,
                urgency,
                status,
                assigned_team,
                1 if review_required else 0,
                override_note,
                case_id,
            ),
        )
        conn.commit()