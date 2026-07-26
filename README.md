# RequestHub

> **Intelligent Request Management Platform with AI-Powered Classification & Multi-Role Workflows**

An enterprise-ready Streamlit application that automates incoming customer request management through intelligent classification, dynamic routing, real-time tracking, and comprehensive analytics. Built with scalable architecture supporting multiple user roles, complete audit trails, and data-driven decision making.

---

## ✨ Features

### Core Functionality
- **🤖 AI-Powered Classification** — Automatic categorization of incoming requests with intelligent priority assignment
- **📊 Real-Time Dashboard** — Interactive analytics with color-coded priority visualization (Red=Critical, Orange=Medium, Green=Low)
- **👥 Multi-Role Interface** — Distinct workflows for Customers, Agents, Managers, and Administrators
- **🔄 Dynamic Workflow Engine** — Automatic case progression through stages with full decision history
- **📝 Complete Audit Trail** — Comprehensive logging of all case modifications for compliance and accountability
- **📥 Request Intake** — Streamlined customer portal for request submission and status tracking
- **⚡ Agent Workspace** — Focused ticket management interface with full case context
- **📈 Manager Console** — Team performance metrics, workload distribution, and SLA monitoring
---

## 🚀 Quick Start

### Prerequisites
- Python 3.9 or higher
- pip (Python package manager)
- SQLite3 (included with Python)

### Installation

1. **Clone the repository:**
```bash
git clone https://github.com/YOUR_USERNAME/RequestHub.git
cd RequestHub

Create virtual environment:

# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate

Install dependencies:

pip install -r requirements.txt

Initialize database:

python -c "from app.database.schema import init_db; init_db()"

Run the application:

streamlit run run_app.py

📁 Project Structure

RequestHub/
├── app/
│   ├── __init__.py
│   ├── main.py                 # Streamlit entry point
│   ├── config/
│   │   ├── __init__.py
│   │   └── settings.py         # Configuration management
│   ├── database/
│   │   ├── __init__.py
│   │   ├── connection.py       # Database connectivity
│   │   └── schema.py           # Schema initialization & management
│   ├── models/
│   │   ├── __init__.py
│   │   └── case.py             # Case data model
│   ├── repositories/
│   │   ├── __init__.py
│   │   └── case_repository.py  # Data access layer
│   ├── services/
│   │   ├── __init__.py
│   │   ├── classifier.py       # AI classification logic
│   │   ├── workflow_engine.py  # Workflow orchestration
│   │   └── response_generator.py # Response generation
│   └── ui/
│       ├── __init__.py
│       ├── agent_workspace.py  # Agent interface
│       ├── customer_portal.py  # Customer interface
│       ├── dashboard.py        # Analytics dashboard
│       ├── manager_console.py  # Manager interface
│       ├── process_request.py  # Request processing UI
│       ├── review_queue.py     # Review queue management
│       ├── case_logs.py        # Case history view
│       └── workflow_stepper.py # Workflow visualization
├── data/                        # Sample data & fixtures
├── docs/
│   └── architecture.md         # Architecture documentation
├── requirements.txt            # Python dependencies
├── run_app.py                  # Application launcher
├── .env.example                # Environment template
├── README.md                   # This file
└── .gitignore                  # Git ignore rules

🏗️ Architecture

┌─────────────────────────────────────────────────────────┐
│                    User Interface Layer                  │
│  ┌──────────────┬──────────────┬──────────────┐         │
│  │   Customer   │    Agent     │   Manager    │         │
│  │    Portal    │   Workspace  │   Console    │         │
│  └──────────────┴──────────────┴──────────────┘         │
└─────────────────────────────────────────────────────────┘
                           ▼
┌─────────────────────────────────────────────────────────┐
│              Application Service Layer                   │
│  ┌──────────────┬──────────────┬──────────────┐         │
│  │  Classifier  │   Workflow   │   Response   │         │
│  │   Service    │    Engine    │  Generator   │         │
│  └──────────────┴──────────────┴──────────────┘         │
└─────────────────────────────────────────────────────────┘
                           ▼
┌─────────────────────────────────────────────────────────┐
│               Data Access Layer (Repository)             │
│          Case Repository → Database Abstraction          │
└─────────────────────────────────────────────────────────┘
                           ▼
┌─────────────────────────────────────────────────────────┐
│                    Data Layer                            │
│        SQLite / PostgreSQL Database + Schema             │
└─────────────────────────────────────────────────────────┘