# Image Generation Toolkit with Fine-Tuning, Inpainting and MCP Server

This project is part of a research effort to explore modern image generation techniques and interface them with agent-based systems using the Model Context Protocol (MCP).

We investigated workflows for:

Fine-tuning generative models (e.g., using LoRA & Dreambooth),

Leveraging inpainting and prompt-based image generation,

Exposing these capabilities to AI agents via MCP, making them usable as tools in automated reasoning systems.

## 📋 System Requirements
Minimum 24 GB of RAM: High memory usage due to model training and inference tasks.

GPU with at least 12 GB VRAM recommended for efficient model execution.

Python 3.8+ with dependencies listed in requirements.txt or pyproject.toml.


# Vision MCP: Image Generation & Text Overlay Server

This lightweight MCP (Model Context Protocol) server exposes two tools for use by LLM agents or automation pipelines:

gen_image: Generate images from text prompts using Stable Diffusion 3.5

gen_text_overlay: Overlay custom text on images using an external API (e.g., Segmind)

The tools are served using FastMCP, making them accessible in function-calling environments like OpenAI Assistants API or LlamaIndex agents.

## Set Up
1. Install uv:
```
curl -LsSf https://astral.sh/uv/install.sh | sh
```

2. Create a virtual environment:
```
uv venv
source .venv/bin/activate
```

3. Install dependencies:
```
uv add "mcp[cli]" httpx
```

or sync with the pyproject.toml:
```
uv sync
```

4. .env 

```
AWS_ACCESS_KEY_ID=
AWS_SECRET_ACCESS_KEY=
x-api-key=
```

5. Run the MCP server

```python
python src/mcp_text_overlay.py
```

