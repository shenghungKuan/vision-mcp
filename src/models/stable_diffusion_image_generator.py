import torch
from diffusers import StableDiffusion3Pipeline
from services.s3.s3_service import upload_image_from_memory


def generate_image(prompt, steps = 10):
    pipe = StableDiffusion3Pipeline.from_pretrained(
        "stabilityai/stable-diffusion-3.5-medium",
        torch_dtype=torch.float16
    )
    pipe = pipe.to("mps")
    return upload_image_from_memory('emptorix-images', pipe(prompt, num_inference_steps=steps, guidance_scale=8).images[0], "test")
