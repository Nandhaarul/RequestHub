import pandas as pd
import streamlit as st
import altair as alt
from typing import Optional

from app.repositories.case_repository import load_cases


def _render_categorical_chart(
    title: str,
    series: pd.Series,
    color_map: Optional[dict] = None,
    legend_text: Optional[str] = None,
) -> None:
    chart_data = (
        series.fillna("Unknown")
        .astype(str)
        .value_counts()
        .rename_axis("category")
        .reset_index(name="count")
    )
    chart_data = chart_data.sort_values("count", ascending=False).reset_index(drop=True)

    if color_map is None:
        color_map = {"default": "#2563eb"}

    normalized_color_map = {
        str(key).strip().lower(): value for key, value in color_map.items()
    }

    def resolve_color(value: str) -> str:
        return normalized_color_map.get(
            str(value).strip().lower(),
            normalized_color_map.get("default", "#2563eb"),
        )

    chart_data["color"] = chart_data["category"].apply(resolve_color)

    chart = (
        alt.Chart(chart_data)
        .mark_bar(size=34)
        .encode(
            x=alt.X("category:N", sort="-y", title=""),
            y=alt.Y("count:Q", title="Number of Tickets"),
            color=alt.Color("color:N", legend=None),
            tooltip=[
                alt.Tooltip("category:N", title="Category"),
                alt.Tooltip("count:Q", title="Count"),
            ],
        )
        .properties(height=260, title=title)
        .configure_axis(labelFontSize=12, titleFontSize=12)
        .configure_title(fontSize=16)
    )

    st.altair_chart(chart, use_container_width=True)

    if legend_text:
        st.caption(legend_text)


def render_dashboard_tab() -> None:
    st.subheader("Manager Dashboard")
    st.caption("A clearer, color-coded view of ticket volume and priority.")

    df = load_cases()
    if df.empty:
        st.info("No cases processed yet.")
        return

    csv_data = df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="Download Audit Report CSV",
        data=csv_data,
        file_name="workflow_audit_report.csv",
        mime="text/csv",
    )

    total_cases = len(df)
    review_cases = int((df["review_required"] == 1).sum())
    high_priority = int(
        df["urgency"].isin(["High", "Critical", "Very High", "Urgent"]).sum()
    )
    closed_cases = int((df["status"] == "Closed").sum())

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Tickets", total_cases)
    col2.metric("Needs Review", review_cases)
    col3.metric("High / Critical", high_priority)
    col4.metric("Closed", closed_cases)

    col_left, col_right = st.columns(2)

    with col_left:
        _render_categorical_chart(
            "Tickets by Classified Query",
            df["issue_category"],
            color_map={"default": "#3b82f6"},
        )

    with col_right:
        _render_categorical_chart(
            "Tickets by Priority",
            df["urgency"],
            color_map={
                "critical": "#dc2626",
                "high": "#dc2626",
                "urgent": "#dc2626",
                "very high": "#dc2626",
                "medium": "#f59e0b",
                "moderate": "#f59e0b",
                "low": "#16a34a",
                "minor": "#16a34a",
                "default": "#6b7280",
            },
        )

    col_left, col_right = st.columns(2)

    with col_left:
        _render_categorical_chart(
            "Tickets by Stage",
            df["current_stage"],
            color_map={"default": "#8b5cf6"},
        )

    with col_right:
        _render_categorical_chart(
            "Tickets by Assigned Team",
            df["assigned_team"],
            color_map={"default": "#14b8a6"},
        )

    st.markdown("### Recent Tickets")
    recent_columns = [
        "id",
        "created_at",
        "requester_name",
        "issue_category",
        "urgency",
        "status",
        "current_stage",
        "assigned_team",
        "assigned_agent",
        "assigned_manager",
    ]

    st.dataframe(df[recent_columns].head(10), use_container_width=True)