import io
import os
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

SERVICE_ACCOUNT_FILE = 'credentials.json'

# Get the directory of the current script
current_script_directory = os.path.dirname(os.path.abspath(__file__))

# Set up the PDF folder path relative to the script's location
PDF_FOLDER = os.path.join(current_script_directory, "pdfs/")

# Ensure PDF folder exists
os.makedirs(PDF_FOLDER, exist_ok=True)

# Get the folder IDs from environment variables
FOLDER_ID = os.getenv('FOLDER_ID')
PROCESSED_FOLDER_ID = os.getenv('PROCESSED_FOLDER_ID')


def main():
    # Authenticate using the service account file
    credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=['https://www.googleapis.com/auth/drive'])

    # Connect to the Drive API
    service = build('drive', 'v3', credentials=credentials)

    # Query for PDF files in the specified folder
    query = f"'{FOLDER_ID}' in parents and mimeType='application/pdf'"
    results = service.files().list(q=query, fields="files(id, name)").execute()
    items = results.get('files', [])

    # Check if there are any PDF files in the folder
    if not items:
        print('No PDF files found in the specified folder.')
        return  # Exit the function if no files are found

    # If there are files, proceed with the download
    print('PDF files found:')
    for item in items:
        print(f"Downloading: {item['name']}...")
        request = service.files().get_media(fileId=item['id'])
        fh = io.BytesIO()
        downloader = MediaIoBaseDownload(fh, request)
        done = False
        while not done:
            _, done = downloader.next_chunk()

        # Write the PDF to a file
        with open(os.path.join(PDF_FOLDER, item['name']), 'wb') as f:
            fh.seek(0)
            f.write(fh.read())
        print(f"Downloaded: {item['name']}")

        # Move the file to the processed folder
        file_id = item['id']
        # Retrieve the existing parents to remove
        file = service.files().get(fileId=file_id, fields='parents').execute()
        previous_parents = ",".join(file.get('parents'))
        # Move the file to the new folder
        file = service.files().update(
            fileId=file_id,
            addParents=PROCESSED_FOLDER_ID,
            removeParents=previous_parents,
            fields='id, parents'
        ).execute()
        print(f"Moved {item['name']} to the processed folder.")


if __name__ == '__main__':
    main()
