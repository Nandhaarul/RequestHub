import streamlit as st


WORKFLOW_STEPS = [
    "Request Submitted",
    "Classified",
    "Assigned",
    "In Progress",
    "In Review",
    "Closed",
]


STAGE_TO_STEP_INDEX = {
    "New": 0,
    "Request Submitted": 0,
    "Classified": 1,
    "Assigned": 2,
    "Approved for Agent Action": 2,
    "In Progress": 3,
    "Pending Customer Response": 3,
    "In Review": 4,
    "Awaiting Manager Approval": 4,
    "Manager Review": 4,
    "Resolved": 4,
    "Closed": 5,
}


def render_workflow_stepper(current_stage: str) -> None:
    current_index = STAGE_TO_STEP_INDEX.get(current_stage, 0)

    st.markdown(
        """
        <style>
        .workflow-stepper {
            display: flex;
            align-items: center;
            width: 100%;
            margin: 16px 0 24px 0;
            overflow-x: auto;
            padding-bottom: 8px;
        }

        .workflow-step {
            min-width: 140px;
            text-align: center;
            color: #9ca3af;
            font-size: 13px;
            font-weight: 600;
        }

        .workflow-circle {
            width: 34px;
            height: 34px;
            border-radius: 50%;
            margin: 0 auto 8px auto;
            display: flex;
            align-items: center;
            justify-content: center;
            border: 2px solid #4b5563;
            background: #111827;
            color: #9ca3af;
        }

        .workflow-step.completed .workflow-circle {
            background: #16a34a;
            border-color: #16a34a;
            color: white;
        }

        .workflow-step.active .workflow-circle {
            background: #2563eb;
            border-color: #60a5fa;
            color: white;
            box-shadow: 0 0 0 4px rgba(37, 99, 235, 0.25);
        }

        .workflow-step.completed,
        .workflow-step.active {
            color: white;
        }

        .workflow-line {
            flex: 1;
            height: 3px;
            min-width: 28px;
            background: #374151;
            margin: 0 -18px 28px -18px;
        }

        .workflow-line.completed {
            background: #16a34a;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    html = '<div class="workflow-stepper">'

    for index, step in enumerate(WORKFLOW_STEPS):
        if index < current_index:
            state = "completed"
            symbol = "✓"
        elif index == current_index:
            state = "active"
            symbol = str(index + 1)
        else:
            state = ""
            symbol = str(index + 1)

        html += f"""
        <div class="workflow-step {state}">
            <div class="workflow-circle">{symbol}</div>
            <div>{step}</div>
        </div>
        """

        if index < len(WORKFLOW_STEPS) - 1:
            line_class = "completed" if index < current_index else ""
            html += f'<div class="workflow-line {line_class}"></div>'

    html += "</div>"
    st.markdown(html, unsafe_allow_html=True)