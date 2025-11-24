import streamlit as st
import os
from auth import build_auth_url, exchange_code_for_tokens, decode_id_token
from models import init_db, User
from services import session_scope
import user_views, analyst_views, admin_views

import streamlit as st

st.set_page_config(page_title="FairFin - Loan Application Portal", layout="wide")

# Allow Auth0 callback parameters without breaking UI
if st.query_params:
    pass


import os
st.sidebar.write("🔍 DEBUG:")
st.sidebar.write("AUTH0_DOMAIN =", os.getenv("AUTH0_DOMAIN"))
st.sidebar.write("CLIENT_ID =", os.getenv("CLIENT_ID"))
st.sidebar.write("REDIRECT_URI =", os.getenv("REDIRECT_URI"))


# Initialize database
init_db()

st.set_page_config(page_title="FairFin - Loan Portal", layout="wide")
st.title("FairFin — Loan Application Portal")

# Extract query params
query_params = st.query_params

# ------------------------------
# 1. AUTH0 CALLBACK HANDLING
# ------------------------------
if "code" in query_params:
    code = query_params.get("code")
    if isinstance(code, list):
        code = code[0]

    try:
        token_data = exchange_code_for_tokens(code)
        st.session_state["id_token"] = token_data.get("id_token")
        st.session_state["access_token"] = token_data.get("access_token")
    except Exception:
        st.error("Authentication failed. Please try again.")

    # Fix infinite loop — fully reset URL parameters
    st.experimental_set_query_params()
    st.rerun()



# ------------------------------
# 2. CHECK IF USER IS LOGGED IN
# ------------------------------
if "id_token" in st.session_state and st.session_state["id_token"]:
    try:
        info = decode_id_token(st.session_state["id_token"])
    except Exception:
        st.error("Invalid login session. Please sign in again.")
        st.stop()

    auth0_sub = info.get("sub")
    email = info.get("email") or info.get("preferred_username") or None
    name = info.get("name") or info.get("nickname") or "User"

    if not email:
        st.error("No email was returned by Auth0. Cannot proceed.")
        st.stop()

    st.sidebar.info(f"Logged in as: {name}")

    # ------------------------------
    # 3. SAFE USER CREATE / LOAD LOGIC
    # ------------------------------
    with session_scope() as s:
        user = s.query(User).filter(User.email == email).first()

        if user:
            if user.auth0_id != auth0_sub:
                user.auth0_id = auth0_sub
                s.commit()
        else:
            user = User(auth0_id=auth0_sub, name=name, email=email, role=None)
            s.add(user)
            s.commit()
            s.refresh(user)

    # ------------------------------
    # 4. ROLE SELECTION (first login only)
    # ------------------------------
    if not user.role or user.role.strip() == "":
        st.info("Please select your role to continue.")

        selected_role = st.radio(
            "Select role",
            ["user", "analyst", "admin"],
            key=f"role_select_{email}"
        )

        if st.button("Save Role", key=f"save_role_{email}"):
            with session_scope() as s:
                db_user = s.query(User).filter(User.auth0_id == auth0_sub).first()
                db_user.role = selected_role
                s.commit()

            st.success("Role saved. Reloading...")
            st.rerun()

        st.stop()

    # ------------------------------
    # 5. ROLE-BASED VIEW ROUTING
    # ------------------------------
    if user.role == "user":
        user_views.user_dashboard(user)

    elif user.role == "analyst":
        analyst_views.analyst_dashboard(user)

    elif user.role == "admin":
        admin_views.admin_dashboard(user)

    else:
        st.error("Unexpected role. Contact the administrator.")
        st.stop()

else:
    # ------------------------------
    # 6. LOGIN PAGE
    # ------------------------------
    st.header("Please log in to continue")
    login_url = build_auth_url()
    st.markdown(f"[**Sign in with Auth0**]({login_url})")
