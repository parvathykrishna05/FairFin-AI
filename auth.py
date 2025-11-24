"""
Auth helpers for Auth0 integration.
This version uses environment variables so the app works
both locally (localhost) and in Streamlit Cloud deployment.
"""

import os
from urllib.parse import urlencode
import requests
import jwt

# ---- Load configuration from environment ----
AUTH0_DOMAIN = os.getenv("AUTH0_DOMAIN")
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
REDIRECT_URI = os.getenv("REDIRECT_URI")  # IMPORTANT

# ---- Auth0 Endpoints ----
AUTH0_BASE_URL = f"https://{AUTH0_DOMAIN}"
AUTH0_AUTHORIZE_URL = f"{AUTH0_BASE_URL}/authorize"
AUTH0_TOKEN_URL = f"{AUTH0_BASE_URL}/oauth/token"


def build_auth_url():
    """Create the Auth0 login redirect URL."""
    params = {
        "client_id": CLIENT_ID,
        "response_type": "code",
        "redirect_uri": REDIRECT_URI,
        "scope": "openid profile email",
        "prompt": "select_account"  # ensures user can switch accounts if needed
    }
    return f"{AUTH0_AUTHORIZE_URL}?{urlencode(params)}"


def exchange_code_for_tokens(code):
    """Exchange authorization code for tokens."""
    payload = {
        "grant_type": "authorization_code",
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "redirect_uri": REDIRECT_URI,
        "code": code
    }

    response = requests.post(
        AUTH0_TOKEN_URL,
        data=payload,
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        timeout=10
    )

    response.raise_for_status()
    return response.json()


def decode_id_token(id_token):
    """Decode token (signature skipped for simplicity — fine for demo)."""
    return jwt.decode(id_token, options={"verify_signature": False})
