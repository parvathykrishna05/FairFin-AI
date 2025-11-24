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


**🔗 Live Demo:** https://drive.google.com/file/d/1-bcbFzS6Ryq0hiBW2gYuRNqNpvE9NwOQ/view?usp=sharing
**📁 Website:** https://fairfin-ai-7ufnb4rxfnwhwbs2xaygzr.streamlit.app/

---

## ✨ Key Features

- AI-driven loan approval scoring  
- SHAP explainable AI for transparent decisions  
- Secure role-based authentication (User, Admin, Analyst)  
- End-to-end loan lifecycle management  
- Full audit logging for compliance  
- Modern Streamlit UI with custom CSS  
- Modular backend built for future scalability  

---

## 🧩 Tech Stack

| Layer | Technologies |
|------|--------------|
| Frontend | Streamlit, CSS |
| Backend | Python, SQLAlchemy |
| Authentication | Auth0 (OAuth 2.0, JWT) |
| Database | SQLite (dev), PostgreSQL (prod) |
| ML/AI | scikit-learn, SHAP, joblib |
| DevOps | Streamlit Cloud, GitHub Actions, Docker |

---

## 🏗️ System Architecture

**Flow:**  
Login → Role Identified → Loan Submission → ML Scoring → Pending Queue → Admin Decision → Analyst SHAP Review → Audit Logging

**Architecture Layers**
- UI Layer (Streamlit)  
- Auth Layer (Auth0, JWT)  
- Service Layer (Loan CRUD, audit logging, scoring)  
- Data Layer (SQLAlchemy ORM)  
- AI Layer (ML model + SHAP insights)  

---

## 🗃️ Data Model

### Core Tables
- **User** – role, email, auth0 id  
- **LoanApplication** – input data, ML score, status, timestamps  
- **AuditLog** – tracking user activity  
- **EditRequest** – user-requested corrections  

### Storage
- SQLite during development  
- PostgreSQL recommended for production  
- JSON fields for raw loan input flexibility  

---

## 🤖 AI / ML Pipeline

### Model
- Logistic Regression with preprocessing  
- Trained on 1,000 synthetic samples  
- Numerical + categorical features  
- Approval threshold: > 40% probability  

### Explainability
- SHAP LinearExplainer  
- Waterfall plots for per-feature impact  
- Analyst dashboard for interpretation  

### Artifacts
- `model.joblib`  
- `explainer.joblib`  
- `feature_names.joblib`  

---

## 🔐 Security & Compliance

### Security Features
- Auth0 OAuth 2.0 authentication  
- JWT-based role validation  
- SQL injection prevention through SQLAlchemy  
- HTTPS enforcement recommended  
- No credential storage in-app  

### Compliance
- **FCRA/ECOA:** ML decisions include explainability  
- **GDPR:** Correction rights through EditRequest  
- **Audit Logging:** Long-term tracking of all critical actions  

---

## 📈 Scalability

- Stateless frontend → supports horizontal scaling  
- ML model loaded once per session  
- PostgreSQL with indexing for production  
- Future enhancements:
  - Redis caching  
  - Celery asynchronous workers  
  - AWS EC2 + NGINX  
  - Potential microservices split  

---

## 📁 Project Structure

```
FairFin-AI/
│
├── app.py                 # Streamlit application
├── services.py            # Business logic
├── models.py              # ORM models
├── database.py            # DB initialization
├── utils.py               # Helper functions
│
├── ml/
│   ├── model_training.py
│   ├── model.joblib
│   ├── explainer.joblib
│   └── feature_names.joblib
│
├── assets/                # CSS and images
└── README.md
```

## ▶️ Running Locally

### 1. Clone the repository
```bash
git clone https://github.com/parvathykrishna05/FairFin-AI
cd FairFin-AI
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Create `.env`
```
AUTH0_DOMAIN
AUTH0_CLIENT_ID
AUTH0_CLIENT_SECRET
AUTH0_API_AUDIENCE
DATABASE_URL
```

### 4. Start the application
```bash
streamlit run app.py
```

## 👥 Team ZENFIN

Ann Lia Sunil

Parvathy Krishna M

Grace Maria Reji

