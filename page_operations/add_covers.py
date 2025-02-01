from notion_client import Client
import os
from pathlib import Path

# Get absolute path to .env file
root_dir = Path(__file__).parent.parent
env_path = root_dir / '.env'

print(f"Loading .env from: {env_path.absolute()}")

# Initialize variables
api_key = None
database_id = None

# Read both values in a single file read
try:
    with open(env_path, 'r') as f:
        env_contents = f.read()
        # Split into lines and process each line
        for line in env_contents.splitlines():
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            if '=' not in line:
                continue
            
            key, value = line.split('=', 1)
            key = key.strip()
            value = value.strip()
            
            if key == 'NOTION_API_KEY':
                api_key = value
            elif key == 'BRAND_IDENTITY_DATABASE_ID':
                database_id = value

except Exception as e:
    print(f"Error reading .env file: {e}")
    raise

# Validate API key
if not api_key:
    raise ValueError("NOTION_API_KEY not found in .env file")
if not api_key.startswith('ntn_'):
    raise ValueError(f"Invalid API key format. Expected 'ntn_' prefix, got: {api_key[:4]}...")

print(f"API Key loaded (first 10 chars): {api_key[:10]}...")
print(f"API Key length: {len(api_key)}")
print(f"API Key starts with 'ntn_': {api_key.startswith('ntn_')}")

# Validate database ID
if not database_id:
    raise ValueError("BRAND_IDENTITY_DATABASE_ID not found in .env file")
if not database_id.strip():
    raise ValueError("BRAND_IDENTITY_DATABASE_ID is empty")

print(f"Database ID: {database_id}")

# Initialize Notion client
try:
    notion = Client(auth=api_key)
    # Test the connection
    test = notion.users.me()
    print("Successfully connected to Notion API")
    print(f"Connected as: {test.get('name', 'Unknown User')}")
    print(f"Bot ID: {test.get('bot', {}).get('owner', {}).get('workspace', True)}")
except Exception as e:
    print("\nConnection failed!")
    print(f"Error: {str(e)}")
    print("\nDebug information:")
    print(f"API key length: {len(api_key)}")
    print(f"API key format: {api_key[:4]}...")
    print(f"Database ID: {database_id}")
    print("\nPlease verify:")
    print("1. The integration is still active in Notion")
    print("2. The integration has access to the database")
    print("3. The API key hasn't been regenerated")
    raise

GITHUB_RAW_URL_BASE = "https://raw.githubusercontent.com/BethCNC/update-notion/main/images/"
ICON_URL = "https://raw.githubusercontent.com/BethCNC/update-notion/main/images/icon.png"

# Cover photo mapping (page name -> image filename)
cover_photos = {
    "a_b_testing_notes": "a_b_testing_notes.png",
    "brand_guidelines": "brand_guidelines.png",
    "mission_statement": "mission statement.png",
    "moodboard": "moodboard.png",
    "brand_positioning": "brand_positioning.png",
    "brand_values": "brand_values.png",
    "brand_vision": "brand_vision.png",
    "code_snippets_components": "code_snippets_components.png",
    "color_palette": "color_palette.png",
    "competitor_analysis": "competitor_analysis.png",
    "development_roadmap": "development_roadmap.png",
    "hosting_details": "hosting_details.png",
    "iconography": "iconography.png",
    "logos": "logos.png",
    "marketing_assets": "marketing_assets.png",
    "performance_metrics": "performance_metrics.png",
    "photography_style": "photography_style.png",
    "seo_insights": "seo_insights.png",
    "sitemap": "sitemap.png",
    "social_media_templates": "social_media_templates.png",
    "target_audience": "target_audience.png",
    "tech_stack_documentation": "tech_stack_documentation.png",
    "typography": "typography.png",
    "ui_ux_inspiration": "ui_ux_inspiration.png",
    "user_journey_maps": "user_journey_maps.png",
    "website_assets": "website_assets.png",
    "wireframes": "wireframes.png"
}

def update_page_cover_and_icon(page_name):
    """Update a single page cover and icon based on its name"""
    try:
        print(f"Updating page: {page_name}")
        response = notion.databases.query(
            database_id=database_id,
            filter={
                "property": "Name",
                "title": {
                    "equals": page_name
                }
            }
        )

        if not response.get("results"):
            print(f"Page '{page_name}' not found in database.")
            return

        page = response["results"][0]
        page_id = page["id"]

        if page_name in cover_photos:
            cover_url = f"{GITHUB_RAW_URL_BASE}{cover_photos[page_name]}"
            print(f"Using cover URL: {cover_url}")

            notion.pages.update(
                page_id=page_id,
                cover={
                    "type": "external",
                    "external": {
                        "url": cover_url
                    }
                },
                icon={
                    "type": "external",
                    "external": {
                        "url": ICON_URL
                    }
                }
            )
            print(f"Successfully updated cover and icon for page: {page_name}")
        else:
            print(f"No cover photo mapping found for page: {page_name}")
    except Exception as e:
        print(f"Error updating page '{page_name}': {e}")

def update_all_covers_and_icons():
    """Update covers and icons for all pages in the database"""
    try:
        pages = notion.databases.query(database_id=database_id).get("results", [])

        if not pages:
            print("No pages found in the database.")
            return

        for page in pages:
            try:
                page_name = page["properties"]["Name"]["title"][0]["text"]["content"].lower()
                if page_name in cover_photos:
                    print(f"Updating cover and icon for page: {page_name}")
                    update_page_cover_and_icon(page_name)
                else:
                    print(f"No cover photo mapping found for page: {page_name}")
            except Exception as e:
                print(f"Error processing page: {e}")
    except Exception as e:
        print(f"Error fetching pages: {e}")

if __name__ == "__main__":
    # Test updating a single page
    test_page = "a_b_testing_notes"
    print(f"Testing single page update for: {test_page}")
    update_page_cover_and_icon(test_page)

    update_all_covers_and_icons()
