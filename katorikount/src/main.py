import streamlit as st
import os
import logging
import traceback
import json
import tempfile
from google.oauth2.service_account import Credentials
import gspread
import pandas as pd

# Debug prints for startup
print("Starting Streamlit app...")
print("Current working directory:", os.getcwd())
print("Files in directory:", os.listdir())

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def setup_google_sheets():
    try:
        # Log available secrets for debugging
        logger.debug(f"Available secrets: {list(st.secrets.keys())}")
        
        # Create a temporary file that works on both Windows and Unix
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
            creds_path = f.name
            try:
                # Get credentials from secrets
                creds_json = st.secrets["GOOGLE_CREDS_JSON"]
                logger.debug("Successfully retrieved GOOGLE_CREDS_JSON from secrets")
                
                # Write credentials to temp file
                f.write(creds_json)
                f.flush()  # Ensure all data is written
                logger.debug(f"Wrote credentials to temporary file: {creds_path}")
                
            except Exception as e:
                logger.error(f"Error accessing secrets: {str(e)}")
                raise
        
        # Set environment variables for use with libraries like gspread
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = creds_path
        os.environ["SPREADSHEET_ID"] = st.secrets["SPREADSHEET_ID"]
        logger.debug("Set environment variables successfully")
        
        # Initialize Google Sheets client
        creds = Credentials.from_service_account_file(creds_path)
        gc = gspread.authorize(creds)
        sheet = gc.open_by_key(os.environ["SPREADSHEET_ID"]).sheet1
        
        # Clean up the temporary file
        try:
            os.unlink(creds_path)
            logger.debug("Cleaned up temporary credentials file")
        except Exception as e:
            logger.warning(f"Failed to clean up temporary file: {str(e)}")
        
        st.sidebar.success("Successfully connected to Google Sheets!")
        return sheet
        
    except Exception as e:
        st.sidebar.error(f"Error connecting to Google Sheets: {str(e)}")
        st.sidebar.error("Please check your credentials in Streamlit secrets.")
        logger.error(f"Google Sheets connection error: {str(e)}")
        logger.error(traceback.format_exc())
        return None

def main():
    st.title("KatoriKount - AI-Based Nutritional Intelligence")
    st.write("Welcome to KatoriKount! This app helps you track and analyze your nutritional intake.")
    
    # Debug information
    st.sidebar.title("Debug Information")
    st.sidebar.write(f"Working Directory: {os.getcwd()}")
    st.sidebar.write(f"Files in directory: {os.listdir()}")
    
    # Show environment variables and secrets for debugging
    st.sidebar.write("Environment Variables:")
    st.sidebar.write(f"SPREADSHEET_ID: {os.getenv('SPREADSHEET_ID')}")
    st.sidebar.write(f"GOOGLE_APPLICATION_CREDENTIALS: {os.getenv('GOOGLE_APPLICATION_CREDENTIALS')}")
    st.sidebar.write("Available Secrets:", list(st.secrets.keys()))
    
    try:
        # Initialize Google Sheets
        sheet = setup_google_sheets()
        if not sheet:
            st.error("Failed to initialize Google Sheets. Please check the logs.")
            return
            
        # Get all records
        data = sheet.get_all_records()
        if data:
            df = pd.DataFrame(data)
            st.dataframe(df)
        else:
            st.warning("No data found in the spreadsheet")
            
    except Exception as e:
        logger.error(f"Application error: {str(e)}")
        logger.error(traceback.format_exc())
        st.error(f"Error: {str(e)}")
        st.error("Please check the logs for more details.")

if __name__ == "__main__":
    main() 