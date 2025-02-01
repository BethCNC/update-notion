import os

def list_github_image_urls(github_username="BethCNC", repo_name="update-notion"):
    """Generate GitHub raw URLs for all images in the images folder"""
    
    # Get list of files in the images directory
    image_dir = "/Users/bethcartrette/Library/Mobile Documents/com~apple~CloudDocs/REPOS/Chat_GPT_Access_to_Notion/images"
    
    try:
        image_files = [f for f in os.listdir(image_dir) if f.endswith(('.png', '.jpg', '.jpeg', '.gif'))]
        
        print("GitHub Raw URLs for images:")
        print("-" * 50)
        
        for image_file in sorted(image_files):
            # Using the correct repository name and main branch
            raw_url = f"https://raw.githubusercontent.com/{github_username}/{repo_name}/main/images/{image_file}"
            print(f"{image_file}: {raw_url}")
            
            # Also print the alternative URL format in case main branch doesn't work
            alt_url = f"https://raw.githubusercontent.com/{github_username}/{repo_name}/master/images/{image_file}"
            print(f"Alternative URL: {alt_url}\n")
            
    except Exception as e:
        print(f"Error listing images: {e}")

if __name__ == "__main__":
    list_github_image_urls()
