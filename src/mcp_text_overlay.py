from mcp.server.fastmcp import FastMCP
from dotenv import load_dotenv
from models.stable_diffusion_image_generator import generate_image
from services.overlay.overlay import text_overlay

load_dotenv()

# Initialize FastMCP server
mcp = FastMCP("vision-mcp")

@mcp.tool()
async def gen_text_overlay(blend_mode='normal', image_url: str="", text="", out_dir="data/output.jpg") -> str:
    """
    Overlay text on an image using Segmind API.
    Args:
        blend_mode (str): The blend mode to use for the overlay.
        image_url (str): The URL of the image to overlay text on.
        text (str): The text to overlay on the image.
        out_dir (str): The output directory for the processed image.
    Returns:
        str: The message from the text_overlay function.
    """
    return text_overlay(blend_mode=blend_mode, image_url=image_url, text=text, out_dir=out_dir)

@mcp.tool()
async def gen_image(prompt: str, steps: int) -> str:
    """
    Generates an image from a prompt using Stable Diffusion 3.5 and returns pre-signed URL

    Args:
        prompt (str): The prompt for the image generation.
        steps (int): Number of inference steps (default: 10)

    Returns:
        str: Returns image_url to the generated image.
    """

    return generate_image(prompt, steps)


if __name__ == "__main__":
    # Initialize and run the server
    mcp.run(transport='stdio')