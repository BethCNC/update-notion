from notion_client import Client
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Initialize Notion client
notion = Client(auth=os.getenv('NOTION_API_KEY'))

# Function to update database properties
def update_database_properties(database_id, properties):
    try:
        response = notion.databases.update(
            database_id=database_id,
            properties=properties
        )
        print(f"Updated database {database_id} with properties.")
    except Exception as e:
        print(f"Error updating database {database_id}: {e}")

# Define properties for Client Projects
client_projects_properties = {
    "Project Name": {"title": {}},  # Ensure this is the only title property
    "Client": {
        "relation": {
            "database_id": "f35dd79078dd4a1e99a8ae538047976c",
            "single_property": {}
        }
    },  # Relation to Client Database
    "Start Date": {"date": {}},
    "End Date": {"date": {}},
    "Status": {
        "select": {
            "options": [
                {"name": "Planned", "color": "blue"},
                {"name": "In Progress", "color": "yellow"},
                {"name": "Completed", "color": "green"},
                {"name": "On Hold", "color": "red"}
            ]
        }
    },
    "Budget": {"number": {"format": "dollar"}},  # Fixed format
    "Notes": {"rich_text": {}}
}

# Define properties for Client Tasks
client_tasks_properties = {
    # Removed "Task Name" if it already exists
    "Assigned To": {"people": {}},
    "Due Date": {"date": {}},
    "Status": {
        "select": {
            "options": [
                {"name": "Pending", "color": "yellow"},
                {"name": "In Progress", "color": "blue"},
                {"name": "Completed", "color": "green"}
            ]
        }
    },
    "Priority": {
        "select": {
            "options": [
                {"name": "Low", "color": "gray"},
                {"name": "Medium", "color": "orange"},
                {"name": "High", "color": "red"}
            ]
        }
    },
    "Related Project": {
        "relation": {
            "database_id": "18a86edcae2c8096882fe1ccad1c4ad4",
            "single_property": {}
        }
    },  # Relation to Client Projects
    "Related Client": {
        "relation": {
            "database_id": "f35dd79078dd4a1e99a8ae538047976c",
            "single_property": {}
        }
    },  # Relation to Clients
    "Notes": {"rich_text": {}}
}

# Database IDs
CLIENT_PROJECTS_DATABASE_ID = "18a86edcae2c8096882fe1ccad1c4ad4"
CLIENT_TASKS_DATABASE_ID = "18a86edcae2c8062b4d1f91202b5d925"

# Update properties for each database
update_database_properties(CLIENT_PROJECTS_DATABASE_ID, client_projects_properties)
update_database_properties(CLIENT_TASKS_DATABASE_ID, client_tasks_properties)
