# analyst_views.py
import streamlit as st
from services import session_scope, list_pending_loans, log_action
from ui_components import page_header
from analysis import load_model, load_explainer, load_feature_names, predict_proba_and_class, shap_bar_plot
import matplotlib.pyplot as plt


def analyst_dashboard(user):
    page_header("Analyst dashboard", "Review pending applications and run model analysis.")

    model = load_model()
    explainer = load_explainer()
    feature_names = load_feature_names()

    with session_scope() as s:
        pending = list_pending_loans(s)

    if not pending:
        st.info("No pending applications.")
        return

    for loan in pending:
        st.markdown(f"### Application {loan.id} — submitted {loan.created_at}")
        st.json(loan.application_data)

        cols = st.columns([1, 1, 1])

        # ----------------------
        # Prediction Section
        # ----------------------
        with cols[0]:
            if model:
                try:
                    proba, pred = predict_proba_and_class(model, loan.application_data)
                    st.metric("Approval probability", f"{proba:.2%}")
                    st.write("Predicted Decision:", "✔ Approved" if pred == 1 else "✖ Denied")
                except Exception:
                    st.warning("Prediction unavailable for this record.")
            else:
                st.info("Model missing. Add model.joblib to /models folder.")

        # ----------------------
        # SHAP Explanation Section
        # ----------------------
        with cols[1]:
            if explainer and model:
                try:
                    fig = shap_bar_plot(
                        explainer,
                        model,
                        loan.application_data,
                        feature_names=feature_names,
                        topn=8
                    )
                    st.pyplot(fig)
                except Exception:
                    st.warning("Unable to generate SHAP explanation.")
            else:
                st.info("SHAP explainer unavailable.")

        # ----------------------
        # Decision Panel
        # ----------------------
        with cols[2]:
            decision = st.selectbox(
                f"Decision for {loan.id}",
                ["leave pending", "approve", "deny"],
                key=f"dec_{loan.id}"
            )

            explanation = st.text_area("Explanation", key=f"exp_{loan.id}")

            if st.button(f"Apply decision for {loan.id}", key=f"apply_{loan.id}"):
                with session_scope() as s:
                    l = s.query(type(loan)).get(loan.id)

                    if decision == "approve":
                        l.status = "approved"
                        l.decision = "approved"
                        l.explanation = explanation

                    elif decision == "deny":
                        l.status = "denied"
                        l.decision = "denied"
                        l.explanation = explanation

                    log_action(s, user.id, f"Analyst marked loan {loan.id} as {decision}")

                st.success("Decision saved.")
                st.rerun()
