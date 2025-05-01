import streamlit as st

def main():
    st.title("KatoriKount - AI-Based Nutritional Intelligence")
    st.write("Welcome to KatoriKount! This app helps you track and analyze your nutritional intake.")
    
    # Add a simple test widget
    st.write("Basic app test - if you see this, the app is working!")
    
    if st.button("Click me!"):
        st.success("Button clicked!")

if __name__ == "__main__":
    main() 