import streamlit as st
from services import session_scope, list_pending_loans, log_action
from ui_components import page_header
from analysis import (
    load_model,
    load_explainer,
    load_feature_names,
    predict_proba_and_class,
    shap_bar_plot,
    generate_simple_shap_explanation
)
import matplotlib.pyplot as plt


def analyst_dashboard(user):
    page_header("Analyst Dashboard", "Review pending applications and run model analysis.")

    model = load_model()
    explainer = load_explainer()
    feature_names = load_feature_names()

    with session_scope() as s:
        pending = list_pending_loans(s)

    if not pending:
        st.info("No pending loan applications.")
        return

    for loan in pending:
        st.markdown(f"### Application {loan.id} — submitted {loan.created_at}")
        st.json(loan.application_data)

        cols = st.columns([1, 1, 1])

        # --------------------------
        # Column 1 — Model Prediction
        # --------------------------
        with cols[0]:
            if model is not None:
                try:
                    proba, pred = predict_proba_and_class(model, loan.application_data)
                    st.metric("Approval Probability", f"{proba:.2f}")
                    st.write("Predicted Decision:", "Approved ✔" if pred == 1 else "Denied ❌")
                except Exception as e:
                    st.warning(f"Prediction unavailable: {e}")
            else:
                st.info("No ML model available.")

        # --------------------------
        # Column 2 — SHAP Plot
        # --------------------------
        with cols[1]:
            if explainer is not None and model is not None:
                try:
                    fig = shap_bar_plot(explainer, model, loan.application_data, feature_names=feature_names, topn=6)
                    st.pyplot(fig)
                except Exception as e:
                    st.warning(f"Unable to generate SHAP explanation: {e}")
            else:
                st.info("SHAP explainer not available.")

        # --------------------------
        # Column 3 — Decision + Explanation
        # --------------------------
        with cols[2]:

            auto_explanation = ""

            # Generate SHAP-based plain language bullet points
            if explainer and model:
                try:
                    raw_text = generate_simple_shap_explanation(
                        explainer,
                        model,
                        loan.application_data,
                        feature_names=feature_names,
                        topn=3
                    )

                    # Convert explanation into clean bullet point lines
                    auto_explanation = "\n" + "\n".join([line for line in raw_text.split("\n") if line.startswith("-")])

                except Exception:
                    auto_explanation = ""

            decision = st.selectbox(
                f"Decision for Loan {loan.id}",
                ["leave pending", "approve", "deny"],
                key=f"decision_{loan.id}"
            )

            explanation = st.text_area(
                "Explanation shown to the user (auto-generated, editable):",
                key=f"explain_{loan.id}",
                value=auto_explanation
            )

            if st.button(f"Apply Decision for {loan.id}", key=f"apply_{loan.id}"):
                with session_scope() as s:
                    db_loan = s.query(type(loan)).get(loan.id)

                    if decision == "approve":
                        db_loan.status = "approved"
                        db_loan.decision = "approved"
                        db_loan.explanation = explanation

                    elif decision == "deny":
                        db_loan.status = "denied"
                        db_loan.decision = "denied"
                        db_loan.explanation = explanation

                    # leave pending → no changes

                    log_action(s, user.id, f"Analyst updated loan {loan.id} with decision: {decision}")

                st.success("Decision saved successfully.")
                st.rerun()
