# auth.py
"""
Auth helpers for Auth0 integration.
This module provides helper functions used by app.py.
It expects environment variables:
AUTH0_DOMAIN, AUTH0_CLIENT_ID, AUTH0_CLIENT_SECRET, REDIRECT_URI
"""
import os
from urllib.parse import urlencode
import requests
import jwt


AUTH0_DOMAIN = os.getenv("AUTH0_DOMAIN")
CLIENT_ID = os.getenv("AUTH0_CLIENT_ID")
CLIENT_SECRET = os.getenv("AUTH0_CLIENT_SECRET")
REDIRECT_URI = os.getenv("REDIRECT_URI")

AUTH0_BASE_URL = f"https://{AUTH0_DOMAIN}"
AUTH0_AUTHORIZE_URL = f"{AUTH0_BASE_URL}/authorize"
AUTH0_TOKEN_URL = f"{AUTH0_BASE_URL}/oauth/token"


import uuid

params = {
    "client_id": CLIENT_ID,
    "response_type": "code",
    "redirect_uri": REDIRECT_URI,
    "scope": "openid profile email offline_access",
    "state": str(uuid.uuid4()),
    "nonce": str(uuid.uuid4()),
    "prompt": "login"   # forces fresh login instead of using stale cached SSO
}




def exchange_code_for_tokens(code):
    payload = {
        "grant_type": "authorization_code",
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "redirect_uri": REDIRECT_URI,
        "code": code
    }
    resp = requests.post(AUTH0_TOKEN_URL, data=payload,
                         headers={"Content-Type": "application/x-www-form-urlencoded"}, timeout=10)
    resp.raise_for_status()
    return resp.json()

def decode_id_token(id_token):
    # For demo only: do not skip verification in production.
    return jwt.decode(id_token, options={"verify_signature": False})
