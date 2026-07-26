import streamlit as st

from app.repositories.case_repository import load_manager_cases, update_manager_approval
from app.ui.workflow_stepper import render_workflow_stepper


MANAGER_STAGE_OPTIONS = {
    "Manager Review": 35,
    "Approved for Agent Action": 45,
    "Assigned": 50,
    "In Progress": 65,
    "In Review": 75,
    "Resolved": 90,
    "Closed": 100,
}


def render_manager_console() -> None:
    st.subheader("Manager Console")

    manager_name = st.selectbox(
        "Manager",
        [
            "All Managers",
            "Orders - Manager",
            "Accounts - Manager",
            "Billing - Manager",
            "Technical - Manager",
            "Service - Manager",
            "General - Manager",
        ],
    )

    selected_manager = None if manager_name == "All Managers" else manager_name
    df = load_manager_cases(selected_manager)

    if df.empty:
        st.info("No tickets available for this manager view.")
        return

    total_cases = len(df)
    pending_approval = len(df[df["manager_approval_status"] == "Pending"])
    high_priority = len(df[df["urgency"].isin(["High", "Critical"])])
    closed_cases = len(df[df["status"] == "Closed"])

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Team Tickets", total_cases)
    col2.metric("Pending Approval", pending_approval)
    col3.metric("High/Critical", high_priority)
    col4.metric("Closed", closed_cases)

    csv_data = df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="Download Manager Report CSV",
        data=csv_data,
        file_name="manager_ticket_report.csv",
        mime="text/csv",
    )

    st.markdown("### Team Ticket Queue")
    display_columns = [
        "id",
        "created_at",
        "requester_name",
        "issue_category",
        "request_type",
        "urgency",
        "status",
        "current_stage",
        "progress_percent",
        "assigned_team",
        "assigned_agent",
        "assigned_manager",
        "manager_approval_status",
    ]
    st.dataframe(df[display_columns], use_container_width=True)

    selected_id = st.selectbox("Select ticket for manager action", df["id"].tolist())
    selected_case = df[df["id"] == selected_id].iloc[0]

    st.markdown("### Ticket Review")
    st.write(f"**Customer:** {selected_case['requester_name']} ({selected_case['requester_email']})")
    st.write(f"**Classified Query:** {selected_case['issue_category']}")
    st.write(f"**Workflow Type:** {selected_case['request_type']}")
    st.write(f"**Priority:** {selected_case['urgency']}")
    st.write(f"**Assigned Agent:** {selected_case['assigned_agent']}")
    st.write(f"**Review Reason:** {selected_case['review_reason']}")
    st.write("**Request:**")
    st.write(selected_case["request_text"])

    st.markdown("### Progress")
    render_workflow_stepper(selected_case["current_stage"])
    st.write(f"Current Stage: **{selected_case['current_stage']}**")

    st.markdown("### Manager Action")
    with st.form(f"manager_action_{selected_id}"):
        approval_status = st.selectbox(
            "Approval Status",
            ["Pending", "Approved", "Rejected", "Not Required"],
            index=["Pending", "Approved", "Rejected", "Not Required"].index(
                selected_case["manager_approval_status"]
            )
            if selected_case["manager_approval_status"] in ["Pending", "Approved", "Rejected", "Not Required"]
            else 0,
        )

        current_stage = st.selectbox(
            "Stage",
            list(MANAGER_STAGE_OPTIONS.keys()),
            index=list(MANAGER_STAGE_OPTIONS.keys()).index(selected_case["current_stage"])
            if selected_case["current_stage"] in MANAGER_STAGE_OPTIONS else 0,
        )

        manager_note = st.text_area(
            "Manager Note",
            value=selected_case["manager_approval_note"] or "",
            height=100,
        )

        submitted = st.form_submit_button("Save Manager Action")

        if submitted:
            progress_percent = MANAGER_STAGE_OPTIONS[current_stage]

            if approval_status == "Approved":
                status = "Approved for Agent Action"
                review_required = False
            elif approval_status == "Rejected":
                status = "Rejected by Manager"
                review_required = True
            elif current_stage == "Closed":
                status = "Closed"
                review_required = False
            elif current_stage == "Resolved":
                status = "Resolved"
                review_required = False
            elif current_stage == "In Review":
                status = "In Review"
                review_required = True
            else:
                status = "Manager Review"
                review_required = True

            update_manager_approval(
                case_id=int(selected_id),
                approval_status=approval_status,
                manager_note=manager_note.strip(),
                status=status,
                current_stage=current_stage,
                progress_percent=progress_percent,
                review_required=review_required,
            )

            st.success("Manager action saved.")
            st.rerun()