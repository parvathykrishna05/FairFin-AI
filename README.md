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

## 🚀 Core Features

- 🔐 **Auth0 secure login with automatic role onboarding**
- 🤖 **Machine learning approval prediction using logistic regression**
- 📈 **SHAP interpretability to justify AI decisions**
- 🏦 **Full loan lifecycle management: submit → edit → analyst → admin**
- 🧾 **Audit logging for every decision**
- 🗃️ **SQLite + SQLAlchemy ORM for clean persistence**

---

## 🧪 Training the Model

Run the command below once to generate:

- `model.joblib`
- `explainer.joblib`
- `feature_names.joblib`

```sh
python model_training.py
