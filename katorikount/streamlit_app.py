import streamlit as st
from src.sheets_manager import SheetsManager
import pandas as pd
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    st.title("KatoriKount - AI-Based Nutritional Intelligence")
    st.write("Welcome to KatoriKount! This app helps you track and analyze your nutritional intake.")
    
    try:
        # Initialize SheetsManager
        sheets_manager = SheetsManager()
        
        # Get nutrition data
        nutrition_data = sheets_manager.read_data("Nutrition Data")
        
        if nutrition_data:
            # Convert to DataFrame for better display
            df = pd.DataFrame(nutrition_data)
            st.dataframe(df)
        else:
            st.warning("No nutrition data found. Please add some data first.")
            
    except Exception as e:
        logger.error(f"Error in Streamlit app: {str(e)}")
        st.error("An error occurred while loading the data. Please check the logs for details.")

if __name__ == "__main__":
    main() 