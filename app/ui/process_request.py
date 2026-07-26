import streamlit as st

from app.models.case import IncomingRequest
from app.repositories.case_repository import save_case
from app.services.classifier import classify_request
from app.services.response_generator import generate_response
from app.services.workflow_engine import execute_workflow
from app.utils.sample_data import get_sample_requests


ISSUE_CATEGORIES = [
    "Billing",
    "Technical Support",
    "Account Access",
    "Service Appointment",
    "General Query",
]


def render_process_request_tab() -> None:
    st.subheader("Customer Request Intake")

    samples = get_sample_requests()
    selected_sample = st.selectbox("Use a sample request", ["Custom"] + list(samples.keys()))
    default_text = "" if selected_sample == "Custom" else samples[selected_sample]

    col_left, col_right = st.columns(2)
    requester_name = col_left.text_input("Customer Name", value="Demo Customer")
    requester_email = col_right.text_input("Customer Email", value="customer@example.com")

    col_issue, col_source = st.columns(2)
    issue_category = col_issue.selectbox("Issue Category", ISSUE_CATEGORIES)
    source = col_source.selectbox("Source", ["Web Form", "Email", "Shared Inbox", "Manual Entry"])

    request_text = st.text_area(
        "Issue Details / Specifications",
        value=default_text,
        height=180,
    )

    if st.button("Submit Request", type="primary"):
        if not request_text.strip():
            st.error("Please enter issue details before submitting.")
            return

        incoming_request = IncomingRequest(
            requester_name=requester_name.strip(),
            requester_email=requester_email.strip(),
            source=source,
            issue_category=issue_category,
            request_text=request_text.strip(),
        )

        with st.spinner("Submitting request and creating workflow ticket..."):
            classification = classify_request(incoming_request.request_text)
            workflow = execute_workflow(
                classification.request_type,
                classification.urgency,
                incoming_request.issue_category,
            )
            draft_response = generate_response(
                incoming_request.request_text,
                classification.request_type,
                classification.urgency,
            )
            save_case(incoming_request, classification, workflow, draft_response)

        st.success("Request submitted successfully.")

        col1, col2, col3, col4, col5 = st.columns(5)
        col1.metric("Request Type", classification.request_type)
        col2.metric("Priority", classification.urgency)
        col3.metric("Status", workflow.status)
        col4.metric("Assigned Team", workflow.assigned_team)
        col5.metric("Review Required", "Yes" if workflow.review_required else "No")

        st.markdown("### Request Progress")
        st.progress(workflow.progress_percent)
        st.write(f"Current Stage: **{workflow.current_stage}**")

        st.markdown("### Assigned Owner")
        if workflow.review_required:
            st.warning(f"Escalated to manager: {workflow.assigned_manager}")
        else:
            st.success(f"Assigned to agent: {workflow.assigned_agent}")

        st.markdown("### Workflow Reasoning")
        st.info(classification.reasoning)

        st.markdown("### Triggered Workflow Steps")
        for action in workflow.actions:
            st.write(f"- {action}")

        if workflow.follow_up_at:
            st.markdown("### SLA / Follow-Up")
            st.write(workflow.follow_up_at.strftime("%Y-%m-%d %H:%M"))

        st.markdown("### Customer Acknowledgement Draft")
        st.text_area("Draft message", value=draft_response, height=220)