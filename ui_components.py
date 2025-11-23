import streamlit as st
import pandas as pd
from datetime import datetime
import urllib.parse

# Import only values needed for logout (in a try block for safety)
try:
    from auth import AUTH0_DOMAIN, REDIRECT_URI
except ImportError:
    AUTH0_DOMAIN = None
    REDIRECT_URI = None


def page_header(title, subtitle=None):
    st.markdown(f"## {title}")
    if subtitle:
        st.caption(subtitle)


def info_card(title, body):
    with st.container():
        st.markdown(f"**{title}**")
        st.write(body)


def display_loans_table(loans):
    """Displays a clean and readable loan history table."""
    rows = []
    for l in loans:
        rows.append({
            "ID": l.id,
            "Submitted": l.created_at.strftime("%Y-%m-%d %H:%M"),
            "Status": l.status.value if hasattr(l.status, "value") else l.status,
            "Decision": l.decision or "-",
            "Explanation": l.explanation or "-"
        })

    if rows:
        df = pd.DataFrame(rows)
        st.dataframe(df, use_container_width=True)
    else:
        st.info("No records to display.")


def logout_button():
    """Provides a consistent logout experience using Auth0."""
    if st.sidebar.button("Logout"):
        st.session_state.clear()
        st.query_params = {}

        if AUTH0_DOMAIN and REDIRECT_URI:
            return_url = urllib.parse.quote(REDIRECT_URI)
            logout_url = f"https://{AUTH0_DOMAIN}/v2/logout?federated&returnTo={return_url}"

            st.write(
                f'<meta http-equiv="refresh" content="0; url={logout_url}" />',
                unsafe_allow_html=True
            )
        else:
            st.warning("Logout config missing — user session cleared locally.")
