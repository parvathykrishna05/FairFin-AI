import streamlit as st
from auth import build_auth_url, exchange_code_for_tokens, decode_id_token
from models import init_db, User
from services import session_scope
import user_views, analyst_views, admin_views
import os

# ------------------------------
# PAGE CONFIG
# ------------------------------
st.set_page_config(page_title="FairFin - Loan Application Portal", layout="wide")
st.title("FairFin — Loan Application Portal")

# ------------------------------
# INIT DATABASE
# ------------------------------
init_db()

# ------------------------------
# HANDLE AUTH CODE CALLBACK
# ------------------------------
query_params = st.query_params

if "code" in query_params:
    code = query_params.get("code")
    if isinstance(code, list):
        code = code[0]

    try:
        token_data = exchange_code_for_tokens(code)
        st.session_state["id_token"] = token_data.get("id_token")
        st.session_state["access_token"] = token_data.get("access_token")

        # Remove the code from URL to prevent looping
        st.query_params={}
        st.rerun()
    except Exception as e:
        st.error(f"Authentication failed: {e}")
        st.stop()


# ------------------------------
# CHECK LOGIN STATE
# ------------------------------
if "id_token" in st.session_state and st.session_state["id_token"]:

    try:
        info = decode_id_token(st.session_state["id_token"])
    except Exception:
        st.error("Session expired. Please sign in again.")
        st.stop()

    auth0_sub = info.get("sub")
    email = info.get("email") or info.get("preferred_username")
    name = info.get("name") or info.get("nickname") or "User"

    if not email:
        st.error("No email returned from Auth0 — login cannot continue.")
        st.stop()

    st.sidebar.success(f"Logged in as: {name}")

    # ------------------------------
    # LOAD OR CREATE USER
    # ------------------------------
    with session_scope() as s:
        user = s.query(User).filter(User.email == email).first()

        if not user:
            user = User(auth0_id=auth0_sub, name=name, email=email, role=None)
            s.add(user)
            s.commit()
            s.refresh(user)
        else:
            # Ensure auth0_id stays synced
            if user.auth0_id != auth0_sub:
                user.auth0_id = auth0_sub
                s.commit()

    # ------------------------------
    # ROLE SELECTION (FIRST TIME ONLY)
    # ------------------------------
    if user.role not in ["user", "analyst", "admin"]:
        st.info("Please select your role before proceeding:")

        selected_role = st.radio(
            "Select role",
            ["user", "analyst", "admin"],
            key=f"role_select_{email}"
        )

        if st.button("Save Role", key=f"save_role_{email}"):
            with session_scope() as s:
                db_user = s.query(User).filter(User.email == email).first()
                db_user.role = selected_role
                s.commit()

            st.success("Role saved successfully! Reloading...")
            st.rerun()

        st.stop()

    # ------------------------------
    # ROLE ROUTING
    # ------------------------------
    if user.role == "user":
        user_views.user_dashboard(user)

    elif user.role == "analyst":
        analyst_views.analyst_dashboard(user)

    elif user.role == "admin":
        admin_views.admin_dashboard(user)

    else:
        st.error("Unexpected role stored. Contact support.")
        st.stop()

# ------------------------------
# LOGIN SCREEN
# ------------------------------
else:
    st.header("Please log in to continue")
    login_url = build_auth_url()
    st.markdown(f"[👉 Sign in with Auth0]({login_url})")
