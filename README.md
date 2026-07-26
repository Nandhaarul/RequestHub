# Incoming Request Processing Workflow

A modular Streamlit prototype that accepts incoming requests, classifies them by type and urgency, runs a branch-specific remediation workflow, generates a draft response, and stores an audit log in SQLite.

## Features

- Request intake form with demo samples
- Optional OpenAI classification
- Local fallback classifier when no API key is configured
- Four remediation branches:
  - Complaint
  - General Enquiry
  - Service Request
  - Urgent Escalation
- SQLite audit log
- Dashboard with request counts by type and urgency
- Case detail view with action summary and generated response

## Setup

Create a virtual environment:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Install dependencies:

```powershell
pip install -r requirements.txt
```

Optional: create `.env` from `.env.example` and add an OpenAI API key:

```txt
OPENAI_API_KEY=your_key_here
OPENAI_MODEL=gpt-4.1-mini
```

Run the app:

```powershell
streamlit run run_app.py
```

## Demo Flow

1. Open the Process Request tab.
2. Create a request.
3. Click Process Request.
4. Review the classification, urgency, confidence, triggered remediation steps, assigned team, follow-up timer, and draft response.
5. Repeat for at least three request types.
6. Open Dashboard and Case Logs to show the audit trail.

## Notes

The app is designed for a proof of concept. It does not send real emails, create real tickets, or notify real teams. Those actions are simulated as workflow outputs and audit log entries.
