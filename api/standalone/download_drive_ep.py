import io
import os
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from dotenv import load_dotenv
from google_credentials import get_google_credentials  # Import the function

# Load environment variables from .env file
load_dotenv()

# Get the directory of the current script
current_script_directory = os.path.dirname(os.path.abspath(__file__))

# Set up the PDF folder path relative to the script's location
PDF_FOLDER = os.path.join(current_script_directory, "pdfs/")

# Ensure PDF folder exists
os.makedirs(PDF_FOLDER, exist_ok=True)

# Get the folder IDs from environment variables
FOLDER_ID = os.getenv('FOLDER_ID')
PROCESSED_FOLDER_ID = os.getenv('PROCESSED_FOLDER_ID')


def download_drive_ep():
    credentials = get_google_credentials()
    service = build('drive', 'v3', credentials=credentials)

    query = f"'{FOLDER_ID}' in parents and mimeType='application/pdf'"
    results = service.files().list(q=query, fields="files(id, name)").execute()
    items = results.get('files', [])

    if not items:
        return 'No PDF files found in the specified folder.'

    downloaded_files = []
    moved_files = []

    for item in items:
        request = service.files().get_media(fileId=item['id'])
        fh = io.BytesIO()
        downloader = MediaIoBaseDownload(fh, request)
        done = False

        while not done:
            _, done = downloader.next_chunk()

        pdf_file_path = os.path.join(PDF_FOLDER, item['name'])
        with open(pdf_file_path, 'wb') as f:
            fh.seek(0)
            f.write(fh.read())
        downloaded_files.append(item['name'])

        file_id = item['id']
        file = service.files().get(fileId=file_id, fields='parents').execute()
        previous_parents = ",".join(file.get('parents'))

        service.files().update(
            fileId=file_id,
            addParents=PROCESSED_FOLDER_ID,
            removeParents=previous_parents,
            fields='id, parents'
        ).execute()
        moved_files.append(item['name'])

    return {
        "downloaded_files": downloaded_files,
        "moved_files": moved_files
    }


if __name__ == "__main__":
    # Test the function or perform some standalone tasks
    result = download_drive_ep()
    print(result)
