# Rules
- Keep It Simple Stupid
- Use `uv` for everything, deps and running
- Keep it as a single file
- Make it easy to understand for humans
- Don't add unnecessary dependencies

# Environment Variables
- `WIKIPEDIA_MODE`: Set to `full` to use full English Wikipedia only (bypasses Simple English)
  - Default: `simple` (prioritizes Simple English with fallback to full English)
  - Example: `WIKIPEDIA_MODE=full uv run python main.py`

# Testing

## Manual Test Commands

### Run the server
```bash
# Default mode (Simple English priority)
uv run python main.py

# Full Wikipedia mode
WIKIPEDIA_MODE=full uv run python main.py
```

### Test with MCP Inspector
```bash
# Install MCP Inspector if not already installed
npm install -g @modelcontextprotocol/inspector

# Run the inspector
npx @modelcontextprotocol/inspector uv run python main.py
```

## Test Cases

### Search Tool
1. Search for "solar system" - should return list of related articles
2. Search for "photosynthesis" - should return biology-related articles
3. Search for nonexistent term like "asdfghjkl" - should handle gracefully

### Summary Tool
1. Get summary of "Earth" - should return page summary
2. Get summary of "Mercury" - should handle disambiguation
3. Get summary of nonexistent page - should show error

### Content Tool
1. Get full content of "Moon" - should return complete article
2. Get content of ambiguous term - should show disambiguation options
3. Get content of stub article - should fallback to English Wikipedia

## Common Issues

### Import Errors
- Ensure all dependencies installed: `uv sync`

### Connection Issues
- Check network connectivity
- Wikipedia API may be temporarily unavailable

### Linting
- Run `uvx ruff check main.py` to check for issues
- Run `uvx ruff check main.py --fix` to auto-fix
- Run `uvx ruff format main.py` to format code