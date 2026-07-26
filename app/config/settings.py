from pathlib import Path
import os

from dotenv import load_dotenv


BASE_DIR = Path(__file__).resolve().parents[2]
DATA_DIR = BASE_DIR / "data"
DB_PATH = DATA_DIR / "request_workflow.db"

REQUEST_TYPES = [
    "Complaint",
    "General Enquiry",
    "Service Request",
    "Urgent Escalation",
]

URGENCY_LEVELS = ["Low", "Medium", "High", "Critical"]

STATUS_OPTIONS = [
    "Assigned to Agent",
    "In Progress",
    "In Review",
    "Escalated to Manager",
    "Approved for Agent Action",
    "Awaiting Manager Approval",
    "Resolved",
    "Closed",
]

load_dotenv(BASE_DIR / ".env")

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "").strip()
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.0-flash").strip() or "gemini-2.0-flash"

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "").strip()
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4.1-mini").strip() or "gpt-4.1-mini"