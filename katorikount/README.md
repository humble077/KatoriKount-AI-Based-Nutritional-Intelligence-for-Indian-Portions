# KatoriKount - AI-Based Nutritional Intelligence

A Streamlit application for tracking and analyzing nutritional data from Google Sheets.

## Setup

1. Install the required dependencies:
```bash
pip install -r requirements.txt
```

2. Set up Streamlit secrets:
   - Create a `.streamlit/secrets.toml` file in your project directory
   - Add your Google Sheets credentials in the following format:
```toml
[google_credentials]
type = "service_account"
project_id = "your-project-id"
private_key_id = "your-private-key-id"
private_key = "your-private-key"
client_email = "your-service-account-email"
client_id = "your-client-id"
auth_uri = "https://accounts.google.com/o/oauth2/auth"
token_uri = "https://oauth2.googleapis.com/token"
auth_provider_x509_cert_url = "https://www.googleapis.com/oauth2/v1/certs"
client_x509_cert_url = "your-cert-url"
```

## Running the Application

To run the application locally:

```bash
streamlit run streamlit_app.py
```

The application will be available at `http://localhost:8501` by default.

## Features

- Connects to Google Sheets to fetch nutritional data
- Displays data in an interactive table format
- Real-time updates from the connected Google Sheet 