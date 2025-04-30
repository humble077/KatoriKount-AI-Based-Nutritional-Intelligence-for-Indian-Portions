import streamlit as st
import logging
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class SheetsManager:
    def __init__(self):
        try:
            # Log all available secrets for debugging
            logger.debug("=== SECRETS DEBUG INFO ===")
            logger.debug(f"All available secrets: {dict(st.secrets)}")
            logger.debug(f"Secrets keys: {list(st.secrets.keys())}")
            
            # Check for google_credentials section
            if "google_credentials" in st.secrets:
                logger.debug("Found google_credentials section")
                logger.debug(f"google_credentials keys: {list(st.secrets['google_credentials'].keys())}")
                credentials = st.secrets["google_credentials"]
            else:
                logger.debug("No google_credentials section found")
            
            # Check for individual credential fields
            if all(key in st.secrets for key in ["type", "project_id", "private_key"]):
                logger.debug("Found individual credential fields")
                credentials = {
                    "type": st.secrets["type"],
                    "project_id": st.secrets["project_id"],
                    "private_key_id": st.secrets["private_key_id"],
                    "private_key": st.secrets["private_key"],
                    "client_email": st.secrets["client_email"],
                    "client_id": st.secrets["client_id"],
                    "auth_uri": st.secrets.get("auth_uri", "https://accounts.google.com/o/oauth2/auth"),
                    "token_uri": st.secrets.get("token_uri", "https://oauth2.googleapis.com/token"),
                    "auth_provider_x509_cert_url": st.secrets.get("auth_provider_x509_cert_url", "https://www.googleapis.com/oauth2/v1/certs"),
                    "client_x509_cert_url": st.secrets["client_x509_cert_url"]
                }
            else:
                logger.debug("Individual credential fields not found")
            
            if not credentials:
                raise ValueError("Google credentials not found in Streamlit secrets. Please check your secrets configuration.")
            
            logger.debug("=== CREDENTIALS DEBUG INFO ===")
            logger.debug(f"Credentials type: {credentials.get('type')}")
            logger.debug(f"Project ID: {credentials.get('project_id')}")
            logger.debug(f"Client email: {credentials.get('client_email')}")
            logger.debug(f"Private key present: {'private_key' in credentials}")
            
            # Get spreadsheet ID
            if "spreadsheet_id" in st.secrets:
                self.spreadsheet_id = st.secrets["spreadsheet_id"]
            elif "SPREADSHEET_ID" in st.secrets:
                self.spreadsheet_id = st.secrets["SPREADSHEET_ID"]
            else:
                raise ValueError("Spreadsheet ID not found in Streamlit secrets")
                
            logger.debug(f"Using spreadsheet ID: {self.spreadsheet_id}")
            self.service = self._get_service(credentials)
            logger.info("SheetsManager initialized successfully")
            
        except Exception as e:
            logger.error(f"Error initializing SheetsManager: {str(e)}")
            logger.error(f"Available secrets: {dict(st.secrets)}")
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
            
            missing_fields = [field for field in required_fields if field not in credentials_dict]
            if missing_fields:
                raise ValueError(f"Missing required fields in Google credentials: {missing_fields}")
                    
            # Ensure private key has proper newlines
            if isinstance(credentials_dict["private_key"], str):
                credentials_dict["private_key"] = credentials_dict["private_key"].replace("\\n", "\n")
            
            logger.debug("Creating credentials from service account info")
            credentials = service_account.Credentials.from_service_account_info(
                credentials_dict,
                scopes=["https://www.googleapis.com/auth/spreadsheets"]
            )
            
            logger.debug("Building Google Sheets service")
            service = build("sheets", "v4", credentials=credentials)
            logger.info("Successfully connected to Google Sheets")
            return service
            
        except Exception as e:
            logger.error(f"Error initializing Google Sheets service: {str(e)}")
            raise
            
    def read_data(self, sheet_name):
        """Read data from the specified sheet."""
        try:
            range_name = f"{sheet_name}!A:Z"
            logger.debug(f"Reading data from range: {range_name}")
            
            result = self.service.spreadsheets().values().get(
                spreadsheetId=self.spreadsheet_id,
                range=range_name
            ).execute()
            
            values = result.get("values", [])
            if not values:
                logger.warning(f"No data found in sheet: {sheet_name}")
                return []
                
            logger.info(f"Successfully read {len(values)} rows from {sheet_name}")
            return values
            
        except HttpError as e:
            logger.error(f"HTTP Error reading from Google Sheets: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Error reading from Google Sheets: {str(e)}")
            raise
            
    def write_data(self, sheet_name, values):
        """Write data to the specified sheet."""
        try:
            range_name = f"{sheet_name}!A:Z"
            body = {"values": values}
            
            logger.debug(f"Writing {len(values)} rows to {range_name}")
            result = self.service.spreadsheets().values().update(
                spreadsheetId=self.spreadsheet_id,
                range=range_name,
                valueInputOption="RAW",
                body=body
            ).execute()
            
            logger.info(f"Successfully wrote {len(values)} rows to {sheet_name}")
            return result
            
        except HttpError as e:
            logger.error(f"HTTP Error writing to Google Sheets: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Error writing to Google Sheets: {str(e)}")
            raise 