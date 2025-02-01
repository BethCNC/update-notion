from notion_client import Client

# Initialize Notion client
notion = Client(auth="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")

# Database ID
database_id = "18c86edcae2c80d4852cfd7e132b780b"

# List of page names
page_names = [
    "a_b_testing_notes",
    "brand_guidelines",
    "brand_mission_statement",
    "brand_positioning_statement",
    "brand_values",
    "brand_vision",
    "code_snippets_components",
    "color_palette",
    "competitor_analysis",
    "deliverables_marketing",
    "development_roadmap",
    "hosting_details",
    "iconography",
    "logos",
    "moodboard",
    "performance_metrics",
    "photography_style",
    "reports_archive",
    "seo_insights",
    "sitemap",
    "social_media_templates",
    "target_audience_overview",
    "tech_stack_documentation",
    "tracking_setup_google_analytics",
    "typography",
    "ui_Ux_inspiration",
    "user_journey_maps",
    "website_assets",
    "wireframes",
]

# Google Drive file URLs mapped to page names
cover_photos = {
    "a_b_testing_notes": "https://drive.google.com/uc?id=1a_b_testing_notes",
    "brand_guidelines": "https://drive.google.com/uc?id=1brand_guidelines",
    "brand_mission_statement": "https://drive.google.com/uc?id=1brand_mission_statement",
    "brand_positioning_statement": "https://drive.google.com/uc?id=1brand_positioning_statement",
    "brand_values": "https://drive.google.com/uc?id=1brand_values",
    "brand_vision": "https://drive.google.com/uc?id=1brand_vision",
    "code_snippets_components": "https://drive.google.com/uc?id=1code_snippets_components",
    "color_palette": "https://drive.google.com/uc?id=1color_palette",
    "competitor_analysis": "https://drive.google.com/uc?id=1competitor_analysis",
    "deliverables_marketing": "https://drive.google.com/uc?id=1deliverables_marketing",
    "development_roadmap": "https://drive.google.com/uc?id=1development_roadmap",
    "hosting_details": "https://drive.google.com/uc?id=1hosting_details",
    "iconography": "https://drive.google.com/uc?id=1iconography",
    "logos": "https://drive.google.com/uc?id=1logos",
    "moodboard": "https://drive.google.com/uc?id=1moodboard",
    "performance_metrics": "https://drive.google.com/uc?id=1performance_metrics",
    "photography_style": "https://drive.google.com/uc?id=1photography_style",
    "reports_archive": "https://drive.google.com/uc?id=1reports_archive",
    "seo_insights": "https://drive.google.com/uc?id=1seo_insights",
    "sitemap": "https://drive.google.com/uc?id=1sitemap",
    "social_media_templates": "https://drive.google.com/uc?id=1social_media_templates",
    "target_audience_overview": "https://drive.google.com/uc?id=1target_audience_overview",
    "tech_stack_documentation": "https://drive.google.com/uc?id=1tech_stack_documentation",
    "tracking_setup_google_analytics": "https://drive.google.com/uc?id=1tracking_setup_google_analytics",
    "typography": "https://drive.google.com/uc?id=1typography",
    "ui_Ux_inspiration": "https://drive.google.com/uc?id=1ui_Ux_inspiration",
    "user_journey_maps": "https://drive.google.com/uc?id=1user_journey_maps",
    "website_assets": "https://drive.google.com/uc?id=1website_assets",
    "wireframes": "https://drive.google.com/uc?id=1wireframes",
}

# Icon URL
icon_url = "https://drive.google.com/uc?id=1YPNw-KC8-4q6Vulc7MCMP_4B42ymaz8X"

# Function to create a page in the database
def create_page_in_database(page_name, cover_url, icon_url):
    try:
        response = notion.pages.create(
            parent={"database_id": database_id},
            properties={
                "Name": {
                    "title": [{"type": "text", "text": {"content": page_name}}]
                },
            },
            cover={"type": "external", "external": {"url": cover_url}},
            icon={"type": "external", "external": {"url": icon_url}},
        )
        print(f"Page '{page_name}' created successfully.")
    except Exception as e:
        print(f"Error creating page '{page_name}': {e}")

# Iterate through the page list and create pages
for page_name in page_names:
    if page_name in cover_photos:
        cover_url = cover_photos[page_name]
        create_page_in_database(page_name, cover_url, icon_url)
    else:
        print(f"No cover photo found for page: {page_name}")
