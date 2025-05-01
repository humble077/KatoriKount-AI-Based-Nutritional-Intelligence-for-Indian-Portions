import os
import streamlit as st
from typing import Dict

def get_google_credentials() -> Dict:
    """Get Google credentials from environment or Streamlit secrets"""
    try:
        # Try to get credentials from Streamlit secrets first (production)
        return {
            "type": "service_account",
            "project_id": st.secrets["GOOGLE_PROJECT_ID"],
            "private_key_id": st.secrets["GOOGLE_PRIVATE_KEY_ID"],
            "private_key": st.secrets["GOOGLE_PRIVATE_KEY"],
            "client_email": st.secrets["GOOGLE_CLIENT_EMAIL"],
            "client_id": st.secrets["GOOGLE_CLIENT_ID"],
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
            "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
            "client_x509_cert_url": st.secrets["GOOGLE_CLIENT_CERT_URL"]
        }
    except Exception:
        # Fall back to environment variables (local development)
        return {
            "type": "service_account",
            "project_id": os.getenv("GOOGLE_PROJECT_ID"),
            "private_key_id": os.getenv("GOOGLE_PRIVATE_KEY_ID"),
            "private_key": os.getenv("GOOGLE_PRIVATE_KEY"),
            "client_email": os.getenv("GOOGLE_CLIENT_EMAIL"),
            "client_id": os.getenv("GOOGLE_CLIENT_ID"),
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
            "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
            "client_x509_cert_url": os.getenv("GOOGLE_CLIENT_CERT_URL")
        } 