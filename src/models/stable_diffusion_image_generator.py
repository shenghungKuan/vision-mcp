import torch
from diffusers import StableDiffusion3Pipeline
from src.services.s3.s3_service import upload_image_from_memory
import io

def image_to_bytes(image, format="JPEG") -> bytes:
    """
    Convert a PIL image to raw image bytes.

    :param image: A PIL image object
    :param format: Image format (e.g., 'JPEG', 'PNG')
    :return: Image bytes
    """
    buffer = io.BytesIO()
    image.save(buffer, format=format)
    return buffer.getvalue()

def generate_image(prompt, steps = 10):
    pipe = StableDiffusion3Pipeline.from_pretrained(
        "stabilityai/stable-diffusion-3.5-medium",
        torch_dtype=torch.float16
    )
    pipe = pipe.to("mps")

    image = pipe(prompt, num_inference_steps=steps, guidance_scale=8).images[0]
    return upload_image_from_memory("emptorix-images", image_to_bytes(image), "test")

if __name__ == '__main__':
    print(generate_image("Anime Astronaut in space"))