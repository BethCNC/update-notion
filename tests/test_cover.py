import requests

def check_image_accessibility(image_url):
    try:
        # Follow redirects by allowing GET request after HEAD
        response = requests.get(image_url, allow_redirects=True)
        
        if response.status_code == 200:
            print(f"The image at {image_url} is accessible.")
        else:
            print(f"Error accessing the image at {image_url}. HTTP Status: {response.status_code}")
        
        # Check content type to ensure it's an image
        if 'image' in response.headers.get('Content-Type', ''):
            print("The URL points to a valid image.")
        else:
            print("The URL does not point to an image. Check the file permissions or URL.")
    except Exception as e:
        print(f"An error occurred: {e}")

# Replace with the provided Google Drive link
image_url = "https://drive.google.com/uc?id=11fIUMlIfmVLCPqg9dlQpUKgH-xVcgDng"
check_image_accessibility(image_url)
