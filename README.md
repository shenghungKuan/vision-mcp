# vision-mcp

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
