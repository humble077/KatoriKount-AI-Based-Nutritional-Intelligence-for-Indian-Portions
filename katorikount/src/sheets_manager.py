import streamlit as st
import logging
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

class SheetsManager:
    def __init__(self):
        try:
            # Log available secrets for debugging
            logging.debug(f"Available secrets: {list(st.secrets.keys())}")
            
            # Try to get credentials from different possible locations
            if "google_credentials" in st.secrets:
                credentials = st.secrets["google_credentials"]
            elif all(key in st.secrets for key in ["GOOGLE_PROJECT_ID", "GOOGLE_PRIVATE_KEY"]):
                # Fallback to individual secret keys
                credentials = {
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
            else:
                raise ValueError("Google credentials not found in Streamlit secrets. Please check your secrets configuration.")
                
            # Get spreadsheet ID
            if "spreadsheet_id" in st.secrets:
                self.spreadsheet_id = st.secrets["spreadsheet_id"]
            elif "SPREADSHEET_ID" in st.secrets:
                self.spreadsheet_id = st.secrets["SPREADSHEET_ID"]
            else:
                raise ValueError("Spreadsheet ID not found in Streamlit secrets")
                
            self.service = self._get_service(credentials)
            logging.info("SheetsManager initialized successfully")
            
        except Exception as e:
            logging.error(f"Error initializing SheetsManager: {str(e)}")
            logging.error(f"Available secrets: {list(st.secrets.keys())}")
            raise
            
    def _get_service(self, credentials_dict):
        """Initialize and return the Google Sheets service."""
        try:
            # Validate all required fields are present
            required_fields = [
                "type", "project_id", "private_key_id", "private_key",
                "client_email", "client_id", "auth_uri", "token_uri",
                "auth_provider_x509_cert_url", "client_x509_cert_url"
            ]
            
            for field in required_fields:
                if field not in credentials_dict:
                    raise ValueError(f"Missing required field in Google credentials: {field}")
                    
            # Ensure private key has proper newlines
            if isinstance(credentials_dict["private_key"], str):
                credentials_dict["private_key"] = credentials_dict["private_key"].replace("\\n", "\n")
            
            logging.debug("Creating credentials from service account info")
            credentials = service_account.Credentials.from_service_account_info(
                credentials_dict,
                scopes=["https://www.googleapis.com/auth/spreadsheets"]
            )
            
            logging.debug("Building Google Sheets service")
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
            logging.debug(f"Reading data from range: {range_name}")
            
            result = self.service.spreadsheets().values().get(
                spreadsheetId=self.spreadsheet_id,
                range=range_name
            ).execute()
            
            values = result.get("values", [])
            if not values:
                logging.warning(f"No data found in sheet: {sheet_name}")
                return []
                
            logging.info(f"Successfully read {len(values)} rows from {sheet_name}")
            return values
            
        except HttpError as e:
            logging.error(f"HTTP Error reading from Google Sheets: {str(e)}")
            raise
        except Exception as e:
            logging.error(f"Error reading from Google Sheets: {str(e)}")
            raise
            
    def write_data(self, sheet_name, values):
        """Write data to the specified sheet."""
        try:
            range_name = f"{sheet_name}!A:Z"
            body = {"values": values}
            
            logging.debug(f"Writing {len(values)} rows to {range_name}")
            result = self.service.spreadsheets().values().update(
                spreadsheetId=self.spreadsheet_id,
                range=range_name,
                valueInputOption="RAW",
                body=body
            ).execute()
            
            logging.info(f"Successfully wrote {len(values)} rows to {sheet_name}")
            return result
            
        except HttpError as e:
            logging.error(f"HTTP Error writing to Google Sheets: {str(e)}")
            raise
        except Exception as e:
            logging.error(f"Error writing to Google Sheets: {str(e)}")
            raise 