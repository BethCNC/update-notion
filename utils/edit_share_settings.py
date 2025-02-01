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

# Function to list all files in the folder
def list_files_in_folder(folder_id):
    try:
        query = f"'{folder_id}' in parents and trashed = false"
        results = drive_service.files().list(
            q=query,
            fields="files(id, name)"
        ).execute()
        files = results.get("files", [])
        return files
    except Exception as e:
        print(f"An error occurred while listing files: {e}")
        return []

# Function to update sharing settings for a file
def update_sharing_settings(file_id):
    try:
        # Create a permission that allows anyone with the link to view
        permission = {
            "type": "anyone",
            "role": "reader"
        }
        drive_service.permissions().create(
            fileId=file_id,
            body=permission
        ).execute()
        print(f"Updated sharing settings for file ID: {file_id}")
    except Exception as e:
        print(f"An error occurred while updating sharing settings for file ID {file_id}: {e}")

# Main function to process all files in the folder
def update_folder_sharing_settings(folder_id):
    files = list_files_in_folder(folder_id)
    if not files:
        print("No files found in the folder.")
        return
    for file in files:
        file_id = file["id"]
        file_name = file["name"]
        print(f"Updating sharing settings for file: {file_name} (ID: {file_id})")
        update_sharing_settings(file_id)

# Run the script
update_folder_sharing_settings(FOLDER_ID)
