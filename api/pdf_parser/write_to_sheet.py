import pandas as pd
import os
import shutil
from google.oauth2 import service_account
from googleapiclient.discovery import build
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Service account file and Google Sheet ID
SERVICE_ACCOUNT_FILE = 'credentials.json'
SHEET_ID = os.getenv('GOOGLE_SHEETS_ID')

# Function to clean a directory


def clean_directory(directory):
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print(f'Failed to delete {file_path}. Reason: {e}')


def main():
    # Authenticate using the service account file
    credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE,
        scopes=['https://www.googleapis.com/auth/spreadsheets'])

    # Connect to the Sheets API
    service = build('sheets', 'v4', credentials=credentials)
    sheet = service.spreadsheets()

    # Get the directory of the current script
    current_script_directory = os.path.dirname(os.path.abspath(__file__))

    # Set up the path to the CSV file relative to the script's location
    csv_file_path = os.path.join(
        current_script_directory, "output/MASTER_REPORT.csv")

    # Check if the CSV file exists
    if not os.path.exists(csv_file_path):
        print("No CSV to write to Google Sheets. No CSVs to clean up.")
        return

    # Load data from CSV without headers
    dataframe = pd.read_csv(csv_file_path, header=0)

    # Insert an empty column after the 'Phone' column to match Google Sheets structure
    dataframe.insert(2, 'Empty', '')

    # Prepare values for appending (excluding headers)
    values = dataframe.values.tolist()

    # Append data to Google Sheet
    body = {
        'values': values
    }
    result = sheet.values().append(
        spreadsheetId=SHEET_ID,
        range='A1',
        valueInputOption='USER_ENTERED',
        body=body,
        insertDataOption='INSERT_ROWS').execute()

    if result:
        print(f"{result.get('updates').get('updatedCells')} cells updated.")

    # Clean up the pdfs and output directories
    pdfs_directory = os.path.join(current_script_directory, "pdfs")
    output_directory = os.path.join(current_script_directory, "output")
    clean_directory(pdfs_directory)
    clean_directory(output_directory)
    print("Cleaned up PDF and output directories.")


if __name__ == '__main__':
    main()
