import base64
import os
import requests
from PIL import Image
import io
import logging

from dotenv import load_dotenv

from services.s3.s3_service import upload_image_from_memory
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("mcp.log"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

api_key = os.getenv("x-api-key")
url = "https://api.segmind.com/v1/text-overlay"
print(api_key)

image_url = "https://segmind-sd-models.s3.amazonaws.com/display_images/txt_overlay_in.png.jpeg"

# Request payload
data = {
  "align": "center",
  "base64": False,
  "blend_mode": "normal",
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
  "text": "Hello World",
  "text_underlay": False,
  "wrap": 50
}

headers = {'x-api-key': "SG_1a0272c31cc94a02"}

response = requests.post(url, json=data, headers=headers)
# print(response.content)  # The response is the generated image

print("Response status code:", response.status_code)
image_data = response.content
image = Image.open(io.BytesIO(image_data))
image.show()
image.save("data/output_1.jpg")
print(upload_image_from_memory('emptorix-images', image_data, "test"))