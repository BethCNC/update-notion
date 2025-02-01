from notion_client import Client
import os
from pathlib import Path
import requests
import time

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
    test_data = test  # Store the response
    print("Successfully connected to Notion API")
    print(f"Connected as: {test_data.get('name', 'Unknown User')}")
    print(f"Bot ID: {test_data.get('bot', {}).get('owner', {}).get('workspace', True)}")
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

# Add error handling for image URLs
def verify_image_url(url):
    """Verify that an image URL is accessible"""
    try:
        response = requests.head(url)
        if response.status_code == 200:
            print(f"Successfully verified URL: {url}")
            return True
        print(f"URL not accessible (status {response.status_code}): {url}")
        return False
    except Exception as e:
        print(f"Error checking URL {url}: {e}")
        return False

def get_valid_icon_url():
    """Try both possible icon URLs and return the first valid one"""
    base_url = "https://raw.githubusercontent.com/BethCNC/update-notion/main/images"
    icon_urls = [
        f"{base_url}/icon.png",
        f"{base_url}/logo.png"
    ]
    
    print("Checking icon URLs:")
    for url in icon_urls:
        if verify_image_url(url):
            return url
    return None

# Constants
GITHUB_USER = "BethCNC"
GITHUB_REPO = "update-notion"
GITHUB_BRANCH = "main"
GITHUB_RAW_URL_BASE = f"https://raw.githubusercontent.com/{GITHUB_USER}/{GITHUB_REPO}/{GITHUB_BRANCH}/images/"
ICON_URL = get_valid_icon_url()

if not ICON_URL:
    print("\nWARNING: No valid icon URL found!")
    print("Please verify:")
    print("1. The icon.png file exists in your GitHub repository")
    print("2. The file is in the correct location: /images/icon.png")
    print("3. The repository is public and the file is accessible")
else:
    print(f"\nUsing icon URL: {ICON_URL}")

# Update the cover_photos mapping to match EXACTLY what's in your database
cover_photos = {
    # Exact matches from your database
    "wireframes": "wireframes.png",
    "website_assets": "website_assets.png",
    "user_journey_maps": "user_journey_maps.png",
    "ui_ux_inspiration": "ui_ux_inspiration.png",
    "typography": "typography.png",
    "tech_stack_documentation": "tech_stack_documentation.png",
    "target_audience": "target_audience.png",
    "social_media_templates": "social_media_templates.png",
    "sitemap": "sitemap.png",
    "seo_insights": "seo_insights.png",
    "photography_style": "photography_style.png",
    "performance_metrics": "performance_metrics.png",
    "moodboard": "moodboard.png",
    "logos": "logos.png",
    "iconography": "iconography.png",
    "hosting_details": "hosting_details.png",
    "development_roadmap": "development_roadmap.png",
    "deliverables_marketing": "marketing_assets.png",
    "competitor_analysis": "competitor_analysis.png",
    "color_palette": "color_palette.png",
    "code_snippets_components": "code_snippets_components.png",
    "brand_vision": "brand_vision.png",
    "brand_values": "brand_values.png",
    "brand_positioning_statement": "brand_positioning.png",
    "mission_statement": "mission_statement.png",
    "brand_guidelines": "brand_guidelines.png",
    "a_b_testing_notes": "a_b_testing_notes.png"
}

def verify_github_access():
    """Verify access to GitHub repository and images"""
    print("\nVerifying GitHub repository access...")
    
    # Test a few known images
    test_images = [
        "icon.png",
        "brand_guidelines.png",
        "a_b_testing_notes.png"
    ]
    
    for image in test_images:
        url = f"{GITHUB_RAW_URL_BASE}{image}"
        if verify_image_url(url):
            print(f"✓ Successfully verified access to {image}")
        else:
            print(f"✗ Failed to access {image}")
            print(f"URL attempted: {url}")
            return False
    return True

def update_page_cover_and_icon(page_name, page_id):
    """Update a single page cover and icon"""
    try:
        cover_url = f"{GITHUB_RAW_URL_BASE}{cover_photos[page_name]}"
        print(f"Attempting to update: {page_name}")
        print(f"Using cover URL: {cover_url}")
        
        # Verify URL is accessible
        if not verify_image_url(cover_url):
            print(f"Warning: Cover image URL is not accessible: {cover_url}")
            return False

        # Update the page with new cover and icon
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
        print(f"✓ Successfully updated cover and icon for page: {page_name}")
        return True
    except Exception as e:
        print(f"Error updating page '{page_name}': {e}")
        return False

def update_all_covers_and_icons():
    """Update covers and icons for all pages in the database"""
    try:
        print("\nFetching pages from Notion database...")
        response = notion.databases.query(database_id=database_id)
        pages = response.get("results", [])
        
        if not pages:
            print("No pages found in the database.")
            return

        print("\nFound pages in database:")
        for page in pages:
            page_name = page["properties"]["Name"]["title"][0]["text"]["content"]
            print(f"- {page_name}")

        success_count = 0
        fail_count = 0
        
        for page in pages:
            try:
                page_name = page["properties"]["Name"]["title"][0]["text"]["content"]
                print(f"\nProcessing page: {page_name}")
                if update_page_cover_and_icon(page_name, page["id"]):
                    success_count += 1
                else:
                    fail_count += 1
            except Exception as e:
                print(f"Error processing page: {e}")
                fail_count += 1
        
        print(f"\nUpdate complete:")
        print(f"✓ Successfully updated: {success_count} pages")
        print(f"✗ Failed to update: {fail_count} pages")
        
    except Exception as e:
        print(f"Error fetching pages: {e}")

if __name__ == "__main__":
    print("\nStarting bulk update of all pages...")
    update_all_covers_and_icons()
