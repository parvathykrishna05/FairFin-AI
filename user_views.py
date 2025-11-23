import streamlit as st
from services import session_scope, save_loan, list_user_loans, create_edit_request, log_action
from ui_components import page_header, display_loans_table
from datetime import datetime


def is_pending(loan):
    """Safe check for pending status regardless of enum/string."""
    return (str(getattr(loan.status, "value", loan.status)) == "pending")


def user_dashboard(user):
    page_header("User dashboard", "Submit loan applications and track them.")

    # -----------------------------
    # New Loan Application Form
    # -----------------------------
    st.subheader("New application")

    with st.form("new_app"):
        loan_amount = st.number_input("Loan amount (INR)", min_value=1000, value=50000, step=1000)
        loan_tenure = st.selectbox("Tenure (months)", [12, 24, 36, 48, 60], index=2)
        employment = st.selectbox("Employment type", ["Salaried", "Self-Employed", "Freelancer"])
        annual_income = st.number_input("Annual income (INR)", min_value=0, value=500000, step=10000)
        credit_score = st.slider("Credit score", 300, 850, 650)
        existing_loans = st.number_input("Existing loans", min_value=0, value=0)
        monthly_expenses = st.number_input("Monthly expenses", min_value=0, value=20000)
        gender = st.radio("Gender", ["Male", "Female"])
        region = st.selectbox("Region", ["Urban", "Rural", "Semi-Urban"])
        submitted = st.form_submit_button("Submit")

    if submitted:
        application = {
            "Loan_Amount": float(loan_amount),
            "Loan_Tenure_Months": int(loan_tenure),
            "Employment_Type": employment,
            "Annual_Income": float(annual_income),
            "Credit_Score": int(credit_score),
            "Existing_Loans": int(existing_loans),
            "Monthly_Expenses": float(monthly_expenses),
            "Gender": gender,
            "Region": region,
            "submitted_at": datetime.utcnow().isoformat()
        }

        with session_scope() as s:
            loan = save_loan(s, user.id, application)
            log_action(s, user.id, f"Submitted application {loan.id}")

        st.success(f"Submitted application ID: {loan.id}")
        st.rerun()

    # -----------------------------
    # My Loan Applications Section
    # -----------------------------
    st.subheader("My applications")

    with session_scope() as s:
        loans = list_user_loans(s, user.id)

    display_loans_table(loans)

    # -----------------------------
    # Edit or Withdraw Requests
    # -----------------------------
    st.subheader("Request edit or withdrawal (pending only)")

    pending_loans = [l for l in loans if is_pending(l)]

    if not pending_loans:
        st.info("No pending applications.")
        return

    for loan in pending_loans:
        st.write(f"Application ID: {loan.id}")

        # Separate UI for stability
        with st.form(f"edit_form_{loan.id}"):
            monthly_expenses = st.number_input(
                "Monthly Expenses",
                value=float(loan.application_data.get("Monthly_Expenses", 0))
            )
            existing_loans = st.number_input(
                "Existing Loans",
                value=int(loan.application_data.get("Existing_Loans", 0))
            )
            loan_tenure = st.number_input(
                "Loan Tenure (Months)",
                value=int(loan.application_data.get("Loan_Tenure_Months", 1))
            )

            edit = st.form_submit_button("Request Edit")

        if edit:
            with session_scope() as s:
                req = create_edit_request(
                    s,
                    user_id=user.id,
                    loan_application_id=loan.id,
                    new_monthly_expenses=float(monthly_expenses),
                    new_existing_loans=int(existing_loans),
                    new_loan_tenure=int(loan_tenure),
                    withdraw_requested=False,
                    status="pending"
                )
                log_action(s, user.id, f"Requested edit {req.id} for loan {loan.id}")
            st.success(f"Edit request sent for Application {loan.id}")
            st.rerun()

        with st.form(f"withdraw_form_{loan.id}"):
            withdraw = st.form_submit_button("Request Withdrawal")

        if withdraw:
            with session_scope() as s:
                req = create_edit_request(
                    s,
                    user_id=user.id,
                    loan_application_id=loan.id,
                    withdraw_requested=True,
                    status="pending"
                )
                log_action(s, user.id, f"Requested withdraw {req.id} for loan {loan.id}")
            st.success(f"Withdrawal request sent for Application {loan.id}")
            st.rerun()
