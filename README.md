<div align="center">

# 💰 FairFin — AI-Assisted Loan Evaluation System

A responsible, explainable and role-based loan decisioning application powered by machine learning, Auth0 authentication, and SHAP explainability.

---

### 🔒 Authentication • 🤖 Machine Learning • 📊 SHAP Explainability • 🏦 Loan Workflow Automation

---

</div>

<br>

## 🏷️ Badges

![Python](https://img.shields.io/badge/Python-3.9+-blue?logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-Framework-red?logo=streamlit)
![Status](https://img.shields.io/badge/Project-Working-success)
![License](https://img.shields.io/badge/License-Open%20Use-green)
![Auth0](https://img.shields.io/badge/Auth0-Authentication-orange?logo=auth0)

---

## 📌 Overview

FairFin demonstrates how AI-powered decision systems can be transparent, fair, and auditable.  
It simulates a realistic loan processing environment with multiple user roles and explainable ML predictions.

---

## 👥 User Roles

| Role | Can Submit Loan | View SHAP ML Decision | Approve/Deny | Approve Edit/Withdraw | Manage System |
|------|----------------|------------------------|--------------|------------------------|---------------|
| **User** | ✔ | ✖ | ✖ | Request only | ✖ |
| **Analyst** | ✖ | ✔ | ✔ | ✖ | ✖ |
| **Admin** | ✖ | ✔ | ✔ | ✔ | ✔ |

---

✨ Key Features

Fair AI-Driven Loan Decisions
Logistic Regression model with standardized preprocessing.

Explainable AI with SHAP
Analysts can view feature-level impact through SHAP waterfall plots.

Role-Based Access

Customer: Submit loan applications

Admin: Approve or reject applications

Analyst: View ML explanations and insights

Secure Authentication
Auth0 OAuth 2.0 login + JWT role validation.

Full Loan Lifecycle Management
Submit → Score → Review → Approve/Reject → Log activity.

Audit Logging for Compliance
Every action recorded to meet FCRA/ECOA expectations.

📐 System Architecture

FairFin follows a modular monolithic structure with clear separation of concerns:

Client Layer: Streamlit UI with role-based dashboard navigation

Authentication Layer: Auth0 (OAuth 2.0 + JWT)

Business Logic Layer: Loan CRUD, scoring, audit logging (services.py)

Data Layer: SQLAlchemy ORM models (User, LoanApplication, AuditLog, EditRequest)

AI Layer: On-demand ML prediction + SHAP explainability

High-Level Flow:
Login → Identify role → Submit/view loans → ML prediction → Admin decision → Analyst SHAP view → Audit logs.

🧠 AI / ML Components

Model: Logistic Regression (scikit-learn)

Dataset: Synthetic 1,000-record dataset with numerical + categorical features

Preprocessing: StandardScaler + OneHotEncoder

Output: Approval probability + risk category

Explainability: SHAP LinearExplainer + Waterfall and importance plots

Model Artifacts: Stored as .joblib files

🗄️ Database & Storage
Core Entities

User: Role-based access (customer, admin, analyst)

LoanApplication: JSON-formatted application data + ML output

AuditLog: Detailed activity tracking

EditRequest: Mechanism for users to request corrections

Storage Options

Development: SQLite (fairfin.db)

Production Ready: PostgreSQL with indexing & JSON support

🔒 Security & Compliance

Authenticated sessions via Auth0

Strict role-based authorization

No plain-text passwords (Auth0-managed identity)

SQL injection protection via SQLAlchemy

FCRA/ECOA compliance using ML explainability

GDPR-oriented features:

Data minimization

User correction requests

Consent-based form usage

📈 Scalability & Performance

FairFin is designed to scale with minimal friction:

Stateless Streamlit frontend → easy horizontal scaling

ML model loads once per session → fast inference

PostgreSQL with proper indexing for production workloads

Future:

Redis caching

Celery-based async tasks

NGINX reverse proxy + AWS EC2 deployment

🧩 Technology Stack
Layer	Technologies
Frontend	Streamlit, HTML/CSS
Backend	Python, SQLAlchemy
Authentication	Auth0 (OAuth 2.0, JWT)
Database	SQLite (dev), PostgreSQL (prod)
ML	scikit-learn, SHAP, joblib
Deployment	Streamlit Cloud, GitHub Actions, Docker
📦 Project Structure
FairFin-AI/
│
├── app.py                     # Main Streamlit app
├── services.py                # Business logic (CRUD, scoring, logs)
├── models.py                  # SQLAlchemy models
├── database.py                # DB setup and session logic
├── utils.py                   # Helper functions
├── ml/
│   ├── model_training.py      # Training script
│   ├── model.joblib           # Trained ML model
│   ├── explainer.joblib       # SHAP explainer
│   └── feature_names.joblib   # Preprocessing feature names
├── assets/                    # CSS, images, diagrams
└── README.md

▶️ Running Locally
1. Clone the Repository
git clone https://github.com/parvathykrishna05/FairFin-AI
cd FairFin-AI

2. Install Dependencies
pip install -r requirements.txt

3. Create .env File
AUTH0_DOMAIN=your-domain
AUTH0_CLIENT_ID=your-client-id
AUTH0_CLIENT_SECRET=your-secret
AUTH0_API_AUDIENCE=your-api
DATABASE_URL=sqlite:///fairfin.db

4. Run the App
streamlit run app.py

📹 Demo

Live App:
https://fairfin-ai-7ufnb4rxfnwhwbs2xaygzr.streamlit.app/

YouTube/Drive Video:
(Add your link here)

🤝 Team ZENFIN

Ann Lia Sunil

Parvathy Krishna M

Grace Maria Reji

📄 License

MIT License. You are free to use, modify, and distribute this project.
