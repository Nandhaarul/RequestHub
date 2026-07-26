import streamlit as st

from app.repositories.case_repository import load_review_cases


def render_review_queue_tab() -> None:
    st.subheader("Human Review Queue")

    df = load_review_cases()
    if df.empty:
        st.success("No cases currently require human review.")
        return

    display_columns = [
        "id", "created_at", "requester_name", "request_type", "urgency",
        "status", "assigned_team", "review_reason", "follow_up_at",
    ]

    st.warning(f"{len(df)} case(s) require review.")
    st.dataframe(df[display_columns], use_container_width=True)

    selected_id = st.selectbox("Inspect review case", df["id"].tolist())
    selected_case = df[df["id"] == selected_id].iloc[0]

    st.markdown("### Request")
    st.write(selected_case["request_text"])

    st.markdown("### Review Reason")
    st.info(selected_case["review_reason"] or "Review required based on workflow status.")

    st.markdown("### Current Owner")
    st.write(selected_case["assigned_team"])

    st.markdown("### Next Step")
    st.write(
        "Use the Case Logs tab to apply a manual override, update ownership, "
        "or change the case status after review."
    )