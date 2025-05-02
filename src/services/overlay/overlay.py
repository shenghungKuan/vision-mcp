import os
import requests
from mcp.server.fastmcp import FastMCP
from dotenv import load_dotenv

from src.models.stable_diffusion_image_generator import generate_image
from src.services.s3.s3_service import upload_image_from_memory

load_dotenv()

# Initialize FastMCP server
mcp = FastMCP("vision-mcp")

# Constants
api_key = os.getenv("x-api-key")
url = "https://api.segmind.com/v1/text-overlay"


def text_overlay(blend_mode='normal', image_url: str = "", text=""):
    """
    Overlay text on an image using Segmind API and upload it to S3.

    Args:
        blend_mode (str): The blend mode to use for the overlay.
        image_url (str): The URL of the image to overlay text on.
        text (str): The text to overlay on the image.
        api_key (str): Your API key for Segmind API.
        url (str): The URL for the Segmind API.
    Returns:
        Any: The binary of the processed image or None if there was an error.
    """
    print(image_url)
    # Request payload
    data = {
        "align": "right",
        "base64": False,
        "blend_mode": blend_mode,
        "color": "#FFF",
        "font": "JosefinSans-Bold",
        "font_size": 150,
        "graphspace": 0,
        "image": image_url,
        "image_format": "jpeg",
        "image_quality": 90,
        "linespace": 10,
        "margin_x": 97,
        "margin_y": 300,
        "outline_color": "#11ff00",
        "outline_size": 0,
        "text": text,
        "text_underlay": False,
        "wrap": 50
    }
    headers = {'x-api-key': api_key}

    try:
        # Make a synchronous POST request to Segmind API
        response = requests.post(url, json=data, headers=headers)

        # Check if the request was successful
        if response.status_code == 200:
            response_content = response.content
            # Assuming upload_image_from_memory accepts bytes (if not, modify accordingly)
            return upload_image_from_memory("emptorix-images", image=response_content, object_key="test")
        else:
            print(f"❌ Error: {response.status_code}, {response.text}")
            return None

    except requests.exceptions.RequestException as e:
        print(f"❌ Error during the request: {e}")
        return None

    except Exception as e:
        print(f"❌ Error during image processing: {e}")
        return None

if __name__ == '__main__':
    print(text_overlay(image_url=generate_image("Anime Astronaut in space"), text="Viva Las Vegas"))