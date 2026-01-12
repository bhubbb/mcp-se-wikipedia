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
