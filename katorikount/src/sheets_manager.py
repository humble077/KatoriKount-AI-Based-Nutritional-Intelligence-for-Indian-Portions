import streamlit as st
import logging
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def mask_sensitive_data(secrets_dict):
    """Mask sensitive data in secrets for logging."""
    masked = secrets_dict.copy()
    sensitive_keys = ['private_key', 'GOOGLE_PRIVATE_KEY']
    for key in sensitive_keys:
        if key in masked:
            masked[key] = '***MASKED***'
    return masked

def get_nested_secrets(secrets_dict, key):
    """Get secrets from nested structure."""
    if 'secrets' in secrets_dict:
        return secrets_dict['secrets'].get(key)
    return secrets_dict.get(key)

class SheetsManager:
    def __init__(self):
        try:
            # Log all available secrets for debugging
            logger.debug("=== SECRETS DEBUG INFO ===")
            logger.debug(f"All available secrets (masked): {mask_sensitive_data(dict(st.secrets))}")
            logger.debug(f"Secrets keys: {list(st.secrets.keys())}")
            
            # Get the nested secrets
            secrets = st.secrets.get('secrets', {})
            logger.debug(f"Nested secrets keys: {list(secrets.keys())}")
            
            # Try to get credentials from different possible locations
            credentials = None
            
            # Method 1: Check for google_credentials section
            if "google_credentials" in secrets:
                logger.debug("Method 1: Found google_credentials section")
                logger.debug(f"google_credentials keys: {list(secrets['google_credentials'].keys())}")
                logger.debug(f"google_credentials content (masked): {mask_sensitive_data(dict(secrets['google_credentials']))}")
                credentials = secrets["google_credentials"]
            
            # Method 2: Check for individual fields at root level
            elif all(key in secrets for key in ["type", "project_id", "private_key"]):
                logger.debug("Method 2: Found individual credential fields at root level")
                logger.debug(f"Root level credentials (masked): {mask_sensitive_data({k: secrets[k] for k in ['type', 'project_id', 'private_key_id', 'private_key', 'client_email', 'client_id']})}")
                credentials = {
                    "type": secrets["type"],
                    "project_id": secrets["project_id"],
                    "private_key_id": secrets["private_key_id"],
                    "private_key": secrets["private_key"],
                    "client_email": secrets["client_email"],
                    "client_id": secrets["client_id"],
                    "auth_uri": secrets.get("auth_uri", "https://accounts.google.com/o/oauth2/auth"),
                    "token_uri": secrets.get("token_uri", "https://oauth2.googleapis.com/token"),
                    "auth_provider_x509_cert_url": secrets.get("auth_provider_x509_cert_url", "https://www.googleapis.com/oauth2/v1/certs"),
                    "client_x509_cert_url": secrets["client_x509_cert_url"]
                }
            
            # Method 3: Check for individual fields with GOOGLE_ prefix
            elif all(key in secrets for key in ["GOOGLE_TYPE", "GOOGLE_PROJECT_ID", "GOOGLE_PRIVATE_KEY"]):
                logger.debug("Method 3: Found GOOGLE_ prefixed fields")
                logger.debug(f"GOOGLE_ prefixed credentials (masked): {mask_sensitive_data({k: secrets[k] for k in ['GOOGLE_TYPE', 'GOOGLE_PROJECT_ID', 'GOOGLE_PRIVATE_KEY_ID', 'GOOGLE_PRIVATE_KEY', 'GOOGLE_CLIENT_EMAIL', 'GOOGLE_CLIENT_ID']})}")
                credentials = {
                    "type": secrets["GOOGLE_TYPE"],
                    "project_id": secrets["GOOGLE_PROJECT_ID"],
                    "private_key_id": secrets["GOOGLE_PRIVATE_KEY_ID"],
                    "private_key": secrets["GOOGLE_PRIVATE_KEY"],
                    "client_email": secrets["GOOGLE_CLIENT_EMAIL"],
                    "client_id": secrets["GOOGLE_CLIENT_ID"],
                    "auth_uri": secrets.get("GOOGLE_AUTH_URI", "https://accounts.google.com/o/oauth2/auth"),
                    "token_uri": secrets.get("GOOGLE_TOKEN_URI", "https://oauth2.googleapis.com/token"),
                    "auth_provider_x509_cert_url": secrets.get("GOOGLE_AUTH_PROVIDER_X509_CERT_URL", "https://www.googleapis.com/oauth2/v1/certs"),
                    "client_x509_cert_url": secrets["GOOGLE_CLIENT_X509_CERT_URL"]
                }
            
            if not credentials:
                logger.error("No valid credentials found in any format")
                logger.error("Available secrets keys: " + ", ".join(secrets.keys()))
                raise ValueError("Google credentials not found in Streamlit secrets. Please check your secrets configuration.")
            
            logger.debug("=== CREDENTIALS DEBUG INFO ===")
            logger.debug(f"Credentials type: {credentials.get('type')}")
            logger.debug(f"Project ID: {credentials.get('project_id')}")
            logger.debug(f"Client email: {credentials.get('client_email')}")
            logger.debug(f"Private key present: {'private_key' in credentials}")
            
            # Get spreadsheet ID
            spreadsheet_id = None
            for key in ["spreadsheet_id", "SPREADSHEET_ID", "GOOGLE_SPREADSHEET_ID"]:
                if key in secrets:
                    spreadsheet_id = secrets[key]
                    logger.debug(f"Found spreadsheet ID in {key}: {spreadsheet_id}")
                    break
            
            if not spreadsheet_id:
                logger.error("No spreadsheet ID found in any format")
                raise ValueError("Spreadsheet ID not found in Streamlit secrets")
            
            self.spreadsheet_id = spreadsheet_id
            logger.debug(f"Using spreadsheet ID: {self.spreadsheet_id}")
            
            self.service = self._get_service(credentials)
            logger.info("SheetsManager initialized successfully")
            
        except Exception as e:
            logger.error(f"Error initializing SheetsManager: {str(e)}")
            logger.error(f"Available secrets (masked): {mask_sensitive_data(dict(st.secrets))}")
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