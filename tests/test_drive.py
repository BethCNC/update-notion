from googleapiclient.discovery import build
from google.oauth2.service_account import Credentials
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Get credentials file path from environment
SERVICE_ACCOUNT_FILE = os.getenv('GOOGLE_SERVICE_ACCOUNT_FILE')

# The scope to access Google Drive
SCOPES = ["https://www.googleapis.com/auth/drive"]

# Folder ID from Google Drive
FOLDER_ID = os.getenv('GOOGLE_DRIVE_FOLDER_ID')

# Authenticate and build the Google Drive API service
credentials = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
drive_service = build("drive", "v3", credentials=credentials)

def list_files_in_folder(folder_id):
    try:
        query = f"'{folder_id}' in parents and trashed = false"
        results = drive_service.files().list(
            q=query,
            fields="files(id, name)"
        ).execute()
        files = results.get("files", [])
        if not files:
            print("No files found in the folder.")
        else:
            print("Files in the folder:")
            for file in files:
                print(f"File name: {file['name']}, File ID: {file['id']}")
    except Exception as e:
        print(f"An error occurred: {e}")

# Run the function to list files in the specified folder
list_files_in_folder(FOLDER_ID)
