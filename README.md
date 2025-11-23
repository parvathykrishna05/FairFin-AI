# FairFin — AI-Assisted Loan Evaluation System

FairFin is a transparent and role-based loan processing platform designed to simulate a real-world loan workflow.  
It includes multi-role authentication, ML-based credit decisioning, SHAP-driven model explainability, edit request handling, and a full audit trail.

---

## 🚀 Features

### 🔐 Authentication & User Roles
- Auth0 secure login
- Automatic first-time user registration
- Role-based dashboards:
  - **User** – Submit and track loan requests
  - **Analyst** – Evaluate applications using ML predictions + SHAP
  - **Admin** – Approve edit/withdrawal requests and manage workflow

---

### 📊 ML Decision Support
- Logistic Regression model trained on synthetic financial data
- Automatic feature preprocessing via Sklearn Pipeline
- Probability-based outcome prediction (`approve` vs `deny`)
- Fair and transparent SHAP explainability to justify decisions

---

### 🧾 User Loan Management
- Submit new loan applications
- View status history
- Request:
  - Loan detail corrections
  - Withdrawal before analyst decision
- Edit requests processed by analyst or admin

---

### ✔ Analyst Workflow
- View pending applications
- View ML prediction and SHAP explanation
- Decide: `approve`, `deny`, or `leave pending`

---

### 🛠 Admin Controls
- Approve or reject edit/withdrawal requests
- View activity log trail

---

## 🧩 System Architecture

Auth0 Login → Role Router → User/Admin/Analyst Dashboards
↳ ML Model (predict)
↳ SHAP Explainer (interpret)
↳ SQLite DB (SQLAlchemy ORM)


---

## 📦 Technology Stack

| Component | Technology |
|----------|------------|
| UI Framework | Streamlit |
| Backend / Logic | Python |
| Database | SQLite (SQLAlchemy ORM) |
| Authentication | Auth0 |
| Machine Learning | Scikit-Learn + SHAP |
| State/Session | Streamlit Session State |

---

## 📁 Project Structure

├── app.py # Main entry point

├── analysis.py # ML prediction and SHAP utilities

├── model_training.py # Model training script

├── models.py # SQLAlchemy ORM definitions

├── services.py # Business logic layer

├── user_views.py # User dashboard UI

├── analyst_views.py # Analyst dashboard UI

├── admin_views.py # Admin dashboard UI

├── ui_components.py # Styled UI widgets

└── models/ # Saved ML model + metadata


---

## 🧪 Training the Model

Run the following command once to generate:

- `model.joblib`
- `explainer.joblib`
- `feature_names.joblib`

```sh
python model_training.py


▶ Running the Application
1️⃣ Install dependencies:
pip install -r requirements.txt
