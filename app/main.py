import streamlit as st

from app.database.schema import init_db
from app.ui.agent_workspace import render_agent_workspace
from app.ui.customer_portal import render_customer_portal
from app.ui.dashboard import render_dashboard_tab
from app.ui.manager_console import render_manager_console


def main() -> None:
    st.set_page_config(
        page_title="RequestHub",
        layout="wide",
    )

    init_db()

    st.title("RequestHub")
    st.caption("Drop your queries here!")

    portal, agent, dashboard, manager = st.tabs(
        [
            "Customer Portal",
            "Agent Workspace",
            "Dashboard",
            "Manager Console",
        ]
    )

    with portal:
        render_customer_portal()

    with agent:
        render_agent_workspace()

    with dashboard:
        render_dashboard_tab()

    with manager:
        render_manager_console()


if __name__ == "__main__":
    main()