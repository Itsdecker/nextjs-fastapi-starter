import os
from google.oauth2 import service_account
from dotenv import load_dotenv

# Load environment variables from .env file (useful in local development)
load_dotenv()


def get_google_credentials():
    # Create a dictionary to hold your service account info
    service_account_info = {
        "type": os.getenv("TYPE"),
        "project_id": os.getenv("PROJECT_ID"),
        "private_key_id": os.getenv("PRIVATE_KEY_ID"),
        "private_key": os.getenv("PRIVATE_KEY").replace('\\n', '\n'),
        "client_email": os.getenv("CLIENT_EMAIL"),
        "client_id": os.getenv("CLIENT_ID"),
        "auth_uri": os.getenv("AUTH_URI"),
        "token_uri": os.getenv("TOKEN_URI"),
        "auth_provider_x509_cert_url": os.getenv("AUTH_PROVIDER_X509_CERT_URL"),
        "client_x509_cert_url": os.getenv("CLIENT_X509_CERT_URL")
    }

    # Create credentials object from the service account info
    credentials = service_account.Credentials.from_service_account_info(
        service_account_info)
    return credentials
