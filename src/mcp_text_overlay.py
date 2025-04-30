import os
import sys
import requests
from typing import Any
import httpx
from mcp.server.fastmcp import FastMCP
from dotenv import load_dotenv
import logging
logger = logging.getLogger(__name__)

load_dotenv()

# Initialize FastMCP server
mcp = FastMCP("vision-mcp")

# Constants
api_key = os.getenv("x-api-key")
url = "https://api.segmind.com/v1/text-overlay"

@mcp.tool()
async def text_overlay(blend_mode='normal', image_url: str="", text=""):
    """
    Overlay text on an image using Segmind API.
    Args:
        blend_mode (str): The blend mode to use for the overlay.
        image_url (str): The URL of the image to overlay text on.
        text (str): The text to overlay on the image.
    Returns:
        Any: The response from the Segmind API.
    """
    logger.info("Getting into the function")
    data = {
        "blend_mode": blend_mode,
        "image_url": image_url,
        "text": text
    }
    headers = {'x-api-key': api_key}

    response = requests.post(url, json=data, headers=headers)
    print(response.content)
    return response.content

if __name__ == "__main__":
    # Initialize and run the server
    logging.basicConfig(filename='./mcp.log', level=logging.INFO)
    logger.info("Starting the server")
    mcp.run(transport='stdio')