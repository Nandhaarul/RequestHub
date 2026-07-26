# RequestHub

> **Intelligent Request Management Platform with AI-Powered Classification & Multi-Role Workflows**

An enterprise-ready Streamlit application that automates incoming customer request management through intelligent classification, dynamic routing, real-time tracking, and comprehensive analytics. Built with scalable architecture supporting multiple user roles, complete audit trails, and data-driven decision making.

![Python](https://img.shields.io/badge/Python-3.9+-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.0+-red)
![SQLite](https://img.shields.io/badge/Database-SQLite/PostgreSQL-green)
![License](https://img.shields.io/badge/License-MIT-yellow)

---

## 📋 Table of Contents

- [Features](#-features)
- [Quick Start](#-quick-start)
- [Project Structure](#-project-structure)
- [Architecture](#-architecture)
- [Usage Guide](#-usage-guide)
- [Technology Stack](#-technology-stack)
- [Module Overview](#-module-overview)
- [Demo Walkthrough](#-demo-walkthrough)
- [Roadmap](#-roadmap)
- [Contributing](#-contributing)

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

### Technical Features
- ✓ Modular service-oriented architecture
- ✓ Repository pattern for database abstraction
- ✓ 40+ tracked attributes per case
- ✓ CSV export for audit reports
- ✓ Color-coded priority visualization
- ✓ Real-time KPI metrics
- ✓ Responsive UI for desktop and mobile

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

Design Patterns
Repository Pattern — Abstract database operations for testability and flexibility
Service Layer — Encapsulate business logic in dedicated services
Model Layer — Structured data models for type safety and validation
Configuration Management — Centralized settings for environment-specific configurations


📖 Usage Guide
Customer Portal
Navigate to Customer Portal tab
Fill in the request form:
Requester name
Issue category
Urgency level
Detailed description
Click Submit Request
Receive confirmation with ticket ID
Track status in real-time
Agent Workspace
Navigate to Agent Workspace tab
View assigned tickets with:
Full case context
Customer details
Classification results
Previous decision history
Take action:
Add notes/decisions
Update case status
Move to next workflow stage
Generate and send response
Manager Dashboard
Navigate to Dashboard tab
View KPI metrics:
Total tickets
Tickets needing review
High/Critical priority count
Closed cases
Analyze interactive charts:
Tickets by category (Blue)
Priority distribution (Red/Orange/Green)
Stage breakdown (Purple)
Team workload (Teal)
Export audit report as CSV
Manager Console
Navigate to Manager Console tab
Monitor team performance:
Agent workload and capacity
SLA compliance metrics
Average resolution times
Priority distributions by team
Access detailed analytics and trends
💻 Technology Stack
Layer	Technology	Purpose
Frontend	Streamlit 1.0+	Interactive web interface
Backend	Python 3.9+	Business logic & services
Database	SQLite/PostgreSQL	Data persistence
Data Processing	Pandas, NumPy	Analytics & transformations
Visualization	Altair (Vega-Lite)	Interactive charts & dashboards
Classification	Custom ML Service	Request categorization
Configuration	Python-dotenv	Environment management
Layer	Technology	Purpose
Frontend	Streamlit 1.0+	Interactive web interface
Backend	Python 3.9+	Business logic & services
Database	SQLite/PostgreSQL	Data persistence
Data Processing	Pandas, NumPy	Analytics & transformations
Visualization	Altair (Vega-Lite)	Interactive charts & dashboards
Classification	Custom ML Service	Request categorization
Configuration	Python-dotenv	Environment management


🔧 Module Overview
Database Module (database)
connection.py — Database connection pooling and management
schema.py — Schema initialization, migrations, and DDL operations
Services Module (services)
classifier.py — Request classification engine with priority assignment logic
workflow_engine.py — Orchestrates case progression through workflow stages (Submitted → Assigned → In Progress → Resolved → Closed)
response_generator.py — Generates contextual responses based on case type and classification
Repositories Module (repositories)
case_repository.py — CRUD operations and complex queries for case management
UI Module (ui)
customer_portal.py — Request submission and tracking interface for customers
agent_workspace.py — Ticket processing and management interface for support agents
dashboard.py — Real-time analytics and KPI visualization for management
manager_console.py — Team metrics and performance monitoring for managers
process_request.py — Request processing workflow UI component
review_queue.py — Cases pending review or escalation
case_logs.py — Case history and audit trail viewer


🎬 Demo Walkthrough
Step 1: Submit Request (Customer Portal)
1. Navigate to "Customer Portal" tab
2. Enter requester details and issue description
3. Select issue category and urgency level
4. Click "Submit Request"
5. Note the generated ticket ID and tracking number

Step 2: View in Dashboard

1. Navigate to "Dashboard" tab
2. Observe new ticket in KPI metrics
3. Verify color-coding on Priority chart:
   - Red = Critical/Urgent
   - Orange = Medium
   - Green = Low/Minor
4. Download audit report if needed

Step 3: Process Ticket (Agent Workspace)

1. Navigate to "Agent Workspace" tab
2. Select your assigned ticket from the queue
3. Review classification, urgency, and full context
4. Take action and update case status
5. Add decision notes for audit trail
6. Move case to next workflow stage

Step 4: Monitor Analytics

1. Return to "Dashboard" tab
2. Verify ticket status update reflected in all charts
3. Check metrics update in real-time
4. Export comprehensive audit report as CSV

Step 5: Team Metrics (Manager Console)

1. Navigate to "Manager Console" tab
2. Review team workload distribution
3. Monitor SLA compliance
4. Identify bottlenecks and optimize routing
5. Generate performance reports