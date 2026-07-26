import re

import streamlit as st
from streamlit_sortables import sort_items

from app.repositories.case_repository import load_agent_cases, update_agent_progress
from app.ui.workflow_stepper import render_workflow_stepper


BOARD_COLUMNS = {
    "Ready": {
        "stages": ["Assigned", "Approved for Agent Action"],
        "target_stage": "Assigned",
        "status": "Assigned to Agent",
        "progress": 25,
    },
    "In Progress": {
        "stages": ["In Progress", "Pending Customer Response"],
        "target_stage": "In Progress",
        "status": "In Progress",
        "progress": 50,
    },
    "In Review": {
        "stages": ["In Review", "Awaiting Manager Approval", "Manager Review", "Resolved"],
        "target_stage": "In Review",
        "status": "In Review",
        "progress": 75,
    },
    "Closed / Done": {
        "stages": ["Closed"],
        "target_stage": "Closed",
        "status": "Closed",
        "progress": 100,
    },
}


CARD_STYLE = """
.sortable-component {
    display: grid;
    grid-template-columns: repeat(4, minmax(220px, 1fr));
    gap: 12px;
    align-items: start;
}
.sortable-container {
    background: #111827;
    border: 1px solid #374151;
    border-radius: 8px;
    min-height: 320px;
}
.sortable-container-header {
    background: #1f2937;
    color: #f9fafb;
    font-weight: 700;
    padding: 12px;
    border-bottom: 1px solid #374151;
}
.sortable-container-body {
    padding: 10px;
}
.sortable-item {
    background: #0f172a;
    color: #f9fafb;
    border: 1px solid #334155;
    border-radius: 8px;
    padding: 12px;
    margin-bottom: 10px;
    cursor: grab;
    white-space: pre-wrap;
    line-height: 1.35;
}
.sortable-item:hover {
    border-color: #60a5fa;
    background: #172554;
}
"""


def render_agent_workspace() -> None:
    st.subheader("Agent Workspace")

    agent_name = st.selectbox(
        "Support Agent",
        [
            "Orders - Support Agent",
            "Accounts - Support Agent",
            "Billing - Support Agent",
            "Technical - Support Agent",
            "Service - Support Agent",
            "General - Support Agent",
            "All Agents",
        ],
    )

    selected_agent = None if agent_name == "All Agents" else agent_name
    df = load_agent_cases(selected_agent)

    if df.empty:
        st.info("No tickets assigned to this agent.")
        return

    st.markdown("### My Ticket Board")
    st.caption(
        "Drag a ticket to Ready, In Progress, In Review, or Closed / Done. "
        "Click Save Board Changes to update the customer progress tracker."
    )

    containers, card_to_id = _build_board(df)

    sorted_containers = sort_items(
        containers,
        multi_containers=True,
        custom_style=CARD_STYLE,
        key=f"agent_board_{agent_name}",
    )

    if st.button("Save Board Changes", type="primary"):
        updated_count = _save_board_changes(sorted_containers, card_to_id)
        st.success(f"Board updated. {updated_count} ticket(s) synced to customer progress.")
        st.rerun()

    st.divider()

    st.markdown("### Ticket Details")
    selected_id = st.selectbox("Inspect ticket", df["id"].tolist())
    selected_case = df[df["id"] == selected_id].iloc[0]

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Ticket", f"#{selected_case['id']}")
    col2.metric("Priority", selected_case["urgency"])
    col3.metric("Status", selected_case["status"])
    col4.metric("Progress Stage", selected_case["current_stage"])

    st.write(f"**Customer:** {selected_case['requester_name']} ({selected_case['requester_email']})")
    st.write(f"**Classified Query:** {selected_case['issue_category']}")
    st.write(f"**Assigned Team:** {selected_case['assigned_team']}")
    st.write("**Request:**")
    st.write(selected_case["request_text"])

    st.markdown("### Customer-Facing Workflow Progress")
    render_workflow_stepper(selected_case["current_stage"])
    st.write(f"Current Stage: **{selected_case['current_stage']}**")


def _build_board(df):
    card_to_id = {}
    containers = [{"header": column, "items": []} for column in BOARD_COLUMNS.keys()]

    for _, row in df.iterrows():
        column_name = _column_for_stage(row["current_stage"])
        card = _format_card(row)
        card_to_id[card] = int(row["id"])

        for container in containers:
            if container["header"] == column_name:
                container["items"].append(card)
                break

    return containers, card_to_id


def _column_for_stage(stage: str) -> str:
    for column, config in BOARD_COLUMNS.items():
        if stage in config["stages"]:
            return column

    return "Ready"


def _format_card(row) -> str:
    return (
        f"TICKET-{row['id']}\n"
        f"{row['requester_name']} | {row['issue_category']}\n"
        f"Priority: {row['urgency']}\n"
        f"Stage: {row['current_stage']}\n"
        f"{_shorten(row['request_text'], 90)}"
    )


def _shorten(text: str, limit: int) -> str:
    if not text:
        return ""

    return text if len(text) <= limit else text[: limit - 3] + "..."


def _save_board_changes(sorted_containers, card_to_id) -> int:
    updated_count = 0

    for container in sorted_containers:
        column_name = container["header"]
        config = BOARD_COLUMNS[column_name]

        for card in container["items"]:
            case_id = card_to_id.get(card) or _extract_ticket_id(card)

            if not case_id:
                continue

            update_agent_progress(
                case_id=case_id,
                current_stage=config["target_stage"],
                progress_percent=config["progress"],
                status=config["status"],
                note=f"Moved to {column_name} from agent board.",
            )
            updated_count += 1

    return updated_count


def _extract_ticket_id(card: str) -> int | None:
    match = re.search(r"TICKET-(\d+)", card)

    if not match:
        return None

    return int(match.group(1))