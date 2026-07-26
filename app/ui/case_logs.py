import json

import streamlit as st

from app.config.settings import REQUEST_TYPES, URGENCY_LEVELS, STATUS_OPTIONS
from app.repositories.case_repository import load_cases, update_case_override


def render_case_logs_tab() -> None:
    st.subheader("Case Audit Logs")

    df = load_cases()
    if df.empty:
        st.info("No case logs available yet.")
        return

    csv_data = df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="Download Full Audit Log CSV",
        data=csv_data,
        file_name="case_audit_log.csv",
        mime="text/csv",
    )

    display_columns = [
        "id", "created_at", "requester_name", "source", "request_type",
        "urgency", "status", "assigned_team", "review_required",
        "override_applied", "follow_up_at",
    ]
    st.dataframe(df[display_columns], use_container_width=True)

    selected_id = st.selectbox("View case details", df["id"].tolist())
    selected_case = df[df["id"] == selected_id].iloc[0]

    st.markdown("### Original Request")
    st.write(selected_case["request_text"])

    st.markdown("### Classification Reasoning")
    st.info(selected_case["reasoning"])

    st.markdown("### Action Summary")
    for action in json.loads(selected_case["action_summary"]):
        st.write(f"- {action}")

    st.markdown("### Manual Override")
    with st.form(f"override_form_{selected_id}"):
        request_type = st.selectbox(
            "Request Type",
            REQUEST_TYPES,
            index=REQUEST_TYPES.index(selected_case["request_type"]),
        )
        urgency = st.selectbox(
            "Urgency",
            URGENCY_LEVELS,
            index=URGENCY_LEVELS.index(selected_case["urgency"]),
        )
        status = st.selectbox(
            "Status",
            STATUS_OPTIONS,
            index=STATUS_OPTIONS.index(selected_case["status"])
            if selected_case["status"] in STATUS_OPTIONS else 0,
        )
        assigned_team = st.text_input("Assigned Team", value=selected_case["assigned_team"])
        review_required = st.checkbox(
            "Review Required",
            value=bool(selected_case["review_required"]),
        )
        override_note = st.text_area(
            "Override Note",
            value=selected_case["override_note"] or "",
            height=100,
        )

        submitted = st.form_submit_button("Save Override")
        if submitted:
            update_case_override(
                case_id=int(selected_id),
                request_type=request_type,
                urgency=urgency,
                status=status,
                assigned_team=assigned_team,
                review_required=review_required,
                override_note=override_note.strip(),
            )
            st.success("Manual override saved. Refreshing view...")
            st.rerun()

    st.markdown("### Draft Response")
    st.text_area("Saved draft response", value=selected_case["draft_response"], height=220)