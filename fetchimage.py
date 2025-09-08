import os
import requests
from urllib.parse import urlparse
import uuid

def fetch_image():
    # Prompt the user for an image URL
    url = input("Enter the image URL: ").strip()

    # Create directory "Fetched_Images" if it doesn’t exist
    save_dir = "Fetched_Images"
    os.makedirs(save_dir, exist_ok=True)

    try:
        # Fetch the image
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # Raise error for bad status codes (4xx, 5xx)

        # Extract filename from the URL
        parsed_url = urlparse(url)
        filename = os.path.basename(parsed_url.path)

        # If no filename found, generate one
        if not filename or "." not in filename:
            filename = f"image_{uuid.uuid4().hex}.jpg"

        save_path = os.path.join(save_dir, filename)

        # Save image in binary mode
        with open(save_path, "wb") as f:
            f.write(response.content)

        print(f"✅ Image successfully downloaded and saved as {save_path}")

    except requests.exceptions.MissingSchema:
        print("❌ Invalid URL format. Please include http:// or https://")
    except requests.exceptions.ConnectionError:
        print("❌ Failed to connect. Please check your internet connection or the URL.")
    except requests.exceptions.Timeout:
        print("❌ The request timed out. Please try again.")
    except requests.exceptions.HTTPError as e:
        print(f"❌ HTTP Error: {e}")
    except Exception as e:
        print(f"❌ An unexpected error occurred: {e}")

if __name__ == "__main__":
    fetch_image()
