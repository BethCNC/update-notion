from googleapiclient.discovery import build
from google.oauth2.service_account import Credentials

# Path to your service account credentials JSON file
SERVICE_ACCOUNT_FILE = "/Users/bethcartrette/Library/Mobile Documents/com~apple~CloudDocs/REPOS/Chat_GPT_Access_to_Notion/gpt-access-to-notion-b89a720d560e.json"

# The scope to access Google Drive
SCOPES = ["https://www.googleapis.com/auth/drive"]

# Folder ID from Google Drive (replace this with the correct folder ID)
FOLDER_ID = "1Qczf_AJzSMTtM8KH8NzGHQYFf1s2QPIt"

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
