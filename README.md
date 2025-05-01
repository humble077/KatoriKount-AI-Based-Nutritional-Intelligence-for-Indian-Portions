# KatoriKount - AI-Based Nutritional Intelligence

A Streamlit application for tracking and analyzing nutritional data from Google Sheets, specifically designed for Indian food portions.

## Features

- Real-time nutritional data tracking
- Google Sheets integration for data storage
- Interactive data visualization
- Support for Indian food portions and measurements
- Nutritional analysis and insights

## Setup

1. Clone the repository:
```bash
git clone https://github.com/humble077/KatoriKount-AI-Based-Nutritional-Intelligence-for-Indian-Portions.git
cd KatoriKount-AI-Based-Nutritional-Intelligence-for-Indian-Portions
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up Google Sheets credentials:
   - Create a Google Cloud project
   - Enable Google Sheets API
   - Create a service account and download credentials
   - Share your Google Sheet with the service account email

4. Configure Streamlit secrets:
   - Create a `.streamlit/secrets.toml` file
   - Add your Google credentials in the following format:
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

spreadsheet_id = "your-spreadsheet-id"
```

## Running the Application

### Local Development
```bash
streamlit run katorikount/streamlit_app.py
```

### Deployment Options

#### Railway Deployment (Recommended)
For a simple and straightforward deployment, follow the instructions in [RAILWAY_DEPLOYMENT.md](RAILWAY_DEPLOYMENT.md).

#### Streamlit Cloud Deployment
1. Fork this repository
2. Go to [Streamlit Cloud](https://share.streamlit.io/)
3. Connect your GitHub account
4. Select your forked repository
5. Set the main file path to `katorikount/streamlit_app.py`
6. Add your Google credentials in the Streamlit Cloud secrets management
7. Deploy!

## Project Structure

```
katorikount/
├── src/
│   ├── __init__.py
│   ├── sheets_manager.py
│   ├── nutrition_data.py
│   ├── init_sheets.py
│   └── config.template.py
├── streamlit_app.py
├── requirements.txt
└── README.md
```

## Contributing

1. Fork the repository
2. Create a new branch
3. Make your changes
4. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support, please open an issue in the GitHub repository. 