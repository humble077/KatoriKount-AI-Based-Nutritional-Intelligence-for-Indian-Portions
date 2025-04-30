import streamlit as st
from sheets_manager import SheetsManager

def initialize_sheets():
    """Initialize Google Sheets with required sheets and headers."""
    try:
        sheets_manager = SheetsManager()
        
        # Define required sheets and their headers
        sheets_config = {
            "Nutrition Data": [
                "Date",
                "Category",
                "Food Item",
                "Calories",
                "Protein (g)",
                "Carbs (g)",
                "Fat (g)",
                "Fiber (g)",
                "Sodium (mg)",
                "Notes"
            ],
            "Categories": [
                "Category",
                "Description"
            ]
        }
        
        # Create or update sheets
        for sheet_name, headers in sheets_config.items():
            # Check if sheet exists
            try:
                existing_data = sheets_manager.read_data(sheet_name)
                if not existing_data:
                    # Sheet exists but is empty, add headers
                    sheets_manager.write_data(sheet_name, [headers])
                elif existing_data[0] != headers:
                    # Headers don't match, update them
                    sheets_manager.write_data(sheet_name, [headers] + existing_data[1:])
            except Exception:
                # Sheet doesn't exist, create it with headers
                sheets_manager.write_data(sheet_name, [headers])
                
        st.success("Sheets initialized successfully!")
        
    except Exception as e:
        st.error(f"Error initializing sheets: {str(e)}")
        raise

if __name__ == "__main__":
    initialize_sheets() 