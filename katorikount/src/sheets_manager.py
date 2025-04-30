import streamlit as st
import logging
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

class SheetsManager:
    def __init__(self):
        self.service = self._get_service()
        self.spreadsheet_id = st.secrets["spreadsheet_id"]
        
    def _get_service(self):
        """Initialize and return the Google Sheets service."""
        try:
            credentials_dict = {
                "type": st.secrets["google_credentials"]["type"],
                "project_id": st.secrets["google_credentials"]["project_id"],
                "private_key_id": st.secrets["google_credentials"]["private_key_id"],
                "private_key": st.secrets["google_credentials"]["private_key"].replace("\\n", "\n"),
                "client_email": st.secrets["google_credentials"]["client_email"],
                "client_id": st.secrets["google_credentials"]["client_id"],
                "auth_uri": st.secrets["google_credentials"]["auth_uri"],
                "token_uri": st.secrets["google_credentials"]["token_uri"],
                "auth_provider_x509_cert_url": st.secrets["google_credentials"]["auth_provider_x509_cert_url"],
                "client_x509_cert_url": st.secrets["google_credentials"]["client_x509_cert_url"]
            }
            
            credentials = service_account.Credentials.from_service_account_info(
                credentials_dict,
                scopes=["https://www.googleapis.com/auth/spreadsheets"]
            )
            
            service = build("sheets", "v4", credentials=credentials)
            logging.info("Successfully connected to Google Sheets")
            return service
            
        except Exception as e:
            logging.error(f"Error initializing Google Sheets service: {str(e)}")
            raise
            
    def read_data(self, sheet_name):
        """Read data from the specified sheet."""
        try:
            range_name = f"{sheet_name}!A:Z"
            result = self.service.spreadsheets().values().get(
                spreadsheetId=self.spreadsheet_id,
                range=range_name
            ).execute()
            
            values = result.get("values", [])
            if not values:
                logging.warning(f"No data found in sheet: {sheet_name}")
                return []
                
            return values
            
        except HttpError as e:
            logging.error(f"Error reading from Google Sheets: {str(e)}")
            raise
            
    def write_data(self, sheet_name, values):
        """Write data to the specified sheet."""
        try:
            range_name = f"{sheet_name}!A:Z"
            body = {"values": values}
            
            result = self.service.spreadsheets().values().update(
                spreadsheetId=self.spreadsheet_id,
                range=range_name,
                valueInputOption="RAW",
                body=body
            ).execute()
            
            logging.info(f"Successfully wrote {len(values)} rows to {sheet_name}")
            return result
            
        except HttpError as e:
            logging.error(f"Error writing to Google Sheets: {str(e)}")
            raise 