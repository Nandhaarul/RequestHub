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