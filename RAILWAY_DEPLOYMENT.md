# Deploying KatoriKount on Railway

This guide will walk you through deploying KatoriKount on Railway, a modern platform that makes deployment simple and straightforward.

## Prerequisites

- A GitHub account
- A Railway account (sign up at [railway.app](https://railway.app))
- Your Google Cloud service account credentials
- Your OpenAI API key

## Step 1: Prepare Google Credentials

1. Locate your `service_account.json` file
2. Convert it to a single line using Python:
```python
import json
with open("service_account.json") as f:
    print(json.dumps(json.load(f)))
```
3. Copy the output - you'll need it for Railway environment variables

## Step 2: Deploy on Railway

1. Sign in to your Railway account
2. Click "New Project" and select "Deploy from GitHub Repo"
3. Choose your KatoriKount repository
4. Configure the following environment variables:
   - `OPENAI_API_KEY`: Your OpenAI API key
   - `GOOGLE_CREDENTIALS`: The minified service account JSON from Step 1
   - `SPREADSHEET_ID`: Your Google Sheets spreadsheet ID

5. Set the start command:
```
streamlit run katorikount/src/main.py
```

6. Railway will automatically detect and use port 8501 for Streamlit

## Step 3: Verify Deployment

1. Once deployment is complete, Railway will provide you with a URL
2. Visit the URL to verify your application is running correctly
3. Test the Google Sheets integration and other features

## Troubleshooting

If you encounter any issues:

1. Check the Railway logs for error messages
2. Verify that all environment variables are set correctly
3. Ensure your Google Sheets spreadsheet is shared with the service account email
4. Make sure your OpenAI API key is valid

## Additional Configuration

- You can set up custom domains in Railway's project settings
- Railway provides automatic HTTPS
- You can scale your application resources as needed

## Support

For deployment-related issues, please:
1. Check the Railway documentation at [docs.railway.app](https://docs.railway.app)
2. Open an issue in the GitHub repository
3. Contact Railway support through their platform 