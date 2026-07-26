import streamlit as st

from app.models.case import IncomingRequest
from app.repositories.case_repository import load_customer_cases, save_case
from app.services.classifier import classify_request
from app.services.response_generator import generate_response
from app.services.workflow_engine import execute_workflow
from app.ui.workflow_stepper import render_workflow_stepper


def render_customer_portal() -> None:
    st.subheader("Customer Portal")

    st.markdown("### Submit New Request")

    col_name, col_email = st.columns(2)
    requester_name = col_name.text_input("Customer Name", value="")
    requester_email = col_email.text_input("Customer Email", value="")

    request_text = st.text_area(
        "Describe Your Issue",
        height=180,
        placeholder="Tell us what happened, what support you need, and any relevant details.",
    )

    if st.button("Submit Request", type="primary"):
        if not requester_name.strip() or not requester_email.strip() or not request_text.strip():
            st.error("Please enter your name, email address, and issue details.")
            return

        with st.spinner("Classifying your request and routing it to the right team..."):
            classification = classify_request(request_text.strip())
            issue_category = classify_issue_category(request_text.strip())

            incoming_request = IncomingRequest(
                requester_name=requester_name.strip(),
                requester_email=requester_email.strip(),
                source="Customer Portal",
                issue_category=issue_category,
                request_text=request_text.strip(),
            )

            workflow = execute_workflow(
                classification.request_type,
                classification.urgency,
                incoming_request.issue_category,
            )

            draft_response = generate_response(
                request_text=incoming_request.request_text,
                request_type=classification.request_type,
                urgency=classification.urgency,
                issue_category=incoming_request.issue_category,
                assigned_team=workflow.assigned_team,
            )

            save_case(incoming_request, classification, workflow, draft_response)

        st.success("Your request has been submitted and routed to the appropriate team.")

        col1, col2, col3 = st.columns(3)
        col1.metric("Classified Query", issue_category)
        col2.metric("Priority", classification.urgency)
        col3.metric("Assigned Team", workflow.assigned_team)

        st.markdown("### Routing Summary")
        if workflow.review_required:
            st.warning(
                f"Your request was classified as **{issue_category}** and sent to "
                f"**{workflow.assigned_manager}** under **{workflow.assigned_team}** for review."
            )
        else:
            st.info(
                f"Your request was classified as **{issue_category}** and assigned to "
                f"**{workflow.assigned_agent}** in **{workflow.assigned_team}**."
            )

        if classification.urgency == "Low":
            st.markdown("### Initial Response")
            st.success(draft_response)

        st.markdown("### Request Progress")
        render_workflow_stepper(workflow.current_stage)
        st.write(f"Current Stage: **{workflow.current_stage}**")

    st.divider()

    st.markdown("### Track Existing Requests")
    lookup_email = st.text_input("Enter your email to view request status", key="customer_lookup_email")

    if st.button("View My Requests"):
        if not lookup_email.strip():
            st.error("Please enter an email address.")
            return

        df = load_customer_cases(lookup_email.strip())

        if df.empty:
            st.info("No requests found for this email.")
            return

        for _, row in df.iterrows():
            classified_query = row["issue_category"] or row["request_type"]

            with st.expander(f"Ticket #{row['id']} - {classified_query} - {row['status']}", expanded=False):
                st.write(f"**Classified Query:** {classified_query}")
                st.write(f"**Workflow Type:** {row['request_type']}")
                st.write(f"**Priority:** {row['urgency']}")
                st.write(f"**Assigned Team:** {row['assigned_team']}")
                st.write(f"**Current Stage:** {row['current_stage']}")
                render_workflow_stepper(row["current_stage"])
                st.write(f"**Submitted:** {row['created_at']}")
                if row["follow_up_at"]:
                    st.write(f"**SLA / Follow-up:** {row['follow_up_at']}")
                st.write("**Issue Details:**")
                st.write(row["request_text"])
                if row["urgency"] == "Low":
                    st.write("**Initial Response:**")
                    st.success(row["draft_response"])


def classify_issue_category(request_text: str) -> str:
    text = request_text.lower()

    orders_returns_terms = [
        "order",
        "ordered",
        "cancel",
        "cancelling",
        "cancellation",
        "refund",
        "return",
        "replacement",
        "wrong product",
        "damaged product",
        "delivery",
        "shipment",
        "shipping",
    ]

    account_terms = [
        "login",
        "log in",
        "password",
        "account",
        "locked",
        "access",
        "sign in",
        "signin",
        "reset",
        "otp",
        "verification",
        "profile",
        "phone number",
        "registered phone",
        "mobile number",
        "registered mobile",
        "update my phone",
        "update phone",
        "change phone",
        "change mobile",
        "contact number",
    ]

    billing_terms = [
        "bill",
        "billing",
        "invoice",
        "charged",
        "payment",
        "transaction",
        "subscription",
        "price",
    ]

    technical_terms = [
        "network",
        "internet",
        "connection",
        "speed",
        "slow",
        "outage",
        "not working",
        "error",
        "bug",
        "app crash",
        "website",
        "technical",
    ]

    appointment_terms = [
        "appointment",
        "technician",
        "install",
        "installation",
        "repair",
        "schedule",
        "visit",
        "service request",
    ]

    if _contains_any(text, orders_returns_terms):
        return "Orders & Returns"

    if _contains_any(text, account_terms):
        return "Account Related"

    if _contains_any(text, billing_terms):
        return "Billing & Payments"

    if _contains_any(text, technical_terms):
        return "Technical Support"

    if _contains_any(text, appointment_terms):
        return "Service Appointment"

    return "General Query"


def _contains_any(text: str, terms: list[str]) -> bool:
    return any(term in text for term in terms)