import streamlit as st
from src.sheets_manager import SheetsManager
import pandas as pd
import logging
import traceback

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def main():
    st.title("KatoriKount - AI-Based Nutritional Intelligence")
    st.write("Welcome to KatoriKount! This app helps you track and analyze your nutritional intake.")
    
    try:
        # Initialize SheetsManager
        logger.debug("Initializing SheetsManager...")
        sheets_manager = SheetsManager()
        logger.debug("SheetsManager initialized successfully")
        
        # Get nutrition data
        logger.debug("Attempting to read data from 'Nutrition Data' sheet...")
        nutrition_data = sheets_manager.read_data("Nutrition Data")
        logger.debug(f"Data read successfully: {len(nutrition_data) if nutrition_data else 0} rows")
        
        if nutrition_data:
            # Convert to DataFrame for better display
            df = pd.DataFrame(nutrition_data)
            st.dataframe(df)
        else:
            st.warning("No nutrition data found. Please add some data first.")
            
    except Exception as e:
        logger.error(f"Error in Streamlit app: {str(e)}")
        logger.error(f"Traceback: {traceback.format_exc()}")
        st.error(f"An error occurred while loading the data: {str(e)}")
        st.error("Please check the logs for more details.")

if __name__ == "__main__":
    main() 