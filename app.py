import streamlit as st
import os
import sys
import logging
import traceback

# Configure logging to write to a file
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('app.log')
    ]
)
logger = logging.getLogger(__name__)

def main():
    try:
        logger.info("Starting application...")
        logger.info(f"Current working directory: {os.getcwd()}")
        logger.info(f"Files in directory: {os.listdir()}")
        logger.info(f"Environment variables: PORT={os.environ.get('PORT')}, RAILWAY_ENVIRONMENT={os.environ.get('RAILWAY_ENVIRONMENT')}")
        
        st.title("KatoriKount - AI-Based Nutritional Intelligence")
        st.write("Welcome to KatoriKount! This app helps you track and analyze your nutritional intake.")
        
        # Debug information in sidebar
        st.sidebar.title("Debug Information")
        st.sidebar.write(f"Port: {os.environ.get('PORT', '8501')}")
        st.sidebar.write(f"Environment: {os.environ.get('RAILWAY_ENVIRONMENT', 'unknown')}")
        st.sidebar.write(f"Working Directory: {os.getcwd()}")
        
        # Try to set up Google credentials
        try:
            creds_json = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS_JSON")
            if creds_json:
                logger.info("Found Google credentials in environment variables")
                with open("service_account.json", "w") as f:
                    f.write(creds_json)
                os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "service_account.json"
                st.sidebar.success("✅ Google credentials configured")
                logger.info("Successfully wrote Google credentials to file")
            else:
                logger.warning("No Google credentials found in environment variables")
                st.sidebar.warning("⚠️ No Google credentials found")
        except Exception as e:
            logger.error(f"Error setting up Google credentials: {str(e)}")
            logger.error(traceback.format_exc())
            st.sidebar.error("❌ Error setting up Google credentials")
        
        # Only try to import and use Google Sheets if credentials are set up
        if os.path.exists("service_account.json"):
            try:
                import pandas as pd
                from katorikount.src.sheets_manager import SheetsManager
                
                logger.info("Initializing SheetsManager...")
                sheets_manager = SheetsManager()
                logger.info("SheetsManager initialized successfully")
                
                logger.info("Attempting to read data from 'Nutrition Data' sheet...")
                nutrition_data = sheets_manager.read_data("Nutrition Data")
                logger.info(f"Data read successfully: {len(nutrition_data) if nutrition_data else 0} rows")
                
                if nutrition_data:
                    df = pd.DataFrame(nutrition_data)
                    st.dataframe(df)
                else:
                    st.warning("No nutrition data found. Please add some data first.")
                    
            except Exception as e:
                logger.error(f"Error accessing Google Sheets: {str(e)}")
                logger.error(traceback.format_exc())
                st.error(f"Error accessing Google Sheets: {str(e)}")
        else:
            st.warning("Google Sheets integration not configured. Please set up credentials first.")
            
    except Exception as e:
        logger.error(f"Application error: {str(e)}")
        logger.error(traceback.format_exc())
        st.error(f"Application error: {str(e)}")
        st.error("Please check the logs for more details.")

if __name__ == "__main__":
    main() 