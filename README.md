# Wikipedia Simple English MCP Server

A Model Context Protocol (MCP) server that provides access to Wikipedia content, prioritizing Simple English Wikipedia with intelligent fallback to regular English Wikipedia when content is unavailable or of poor quality.

## Overview

This MCP server acts as a bridge between AI assistants and Wikipedia, specifically designed to:

- **Prioritize Simple English**: Uses Simple English Wikipedia first for clearer, more accessible content
- **Intelligent Fallback**: Automatically falls back to regular English Wikipedia when needed
- **Quality Detection**: Evaluates content quality and switches to English Wikipedia for stub articles
- **Human-Friendly**: Designed with readability and usability in mind

## Features

### 🔍 Search Tool
- Search across Wikipedia articles
- Returns ranked list of relevant page titles
- Tries Simple English first, falls back to English
- Configurable result limits

### 📖 Page Tool
- Retrieve full Wikipedia page content
- Includes page summary and full text
- Automatic disambiguation handling
- Quality-based language selection

## Installation & Setup

### Prerequisites
- Python 3.12 or higher
- `uv` package manager

### Quick Start

**Run directly with uvx:**
```bash
uvx git+https://github.com/bhubbb/mcp-se-wikipedia mcp-se-wikipedia
```

**Or install locally:**
1. **Clone or download this project**
2. **Install dependencies:**
   ```bash
   cd mcp-se-wikipedia
   uv sync
   ```

3. **Run the server:**
   ```bash
   uv run python main.py
   ```

### Integration with AI Assistants

This MCP server is designed to work with AI assistants that support the Model Context Protocol. Configure your AI assistant to connect to this server via stdio.

Example configuration for Claude Desktop:
```json
{
  "mcpServers": {
    "wikipedia-se": {
      "command": "uvx",
      "args": ["git+https://github.com/bhubbb/mcp-se-wikipedia", "mcp-se-wikipedia"]
    }
  }
}
```

Or if using a local installation:
```json
{
  "mcpServers": {
    "wikipedia-se": {
      "command": "uv",
      "args": ["run", "python", "/path/to/mcp-se-wikipedia/main.py"]
    }
  }
}
```

## Available Tools

### `search`
Search Wikipedia for articles.

**Parameters:**
- `query` (required): Search terms
- `limit` (optional): Max results to return (1-20, default: 10)

**Example:**
```json
{
  "name": "search",
  "arguments": {
    "query": "solar system",
    "limit": 5
  }
}
```

### `page`
Get the full content of a Wikipedia page.

**Parameters:**
- `title` (required): Page title to retrieve
- `auto_suggest` (optional): Auto-suggest similar titles if exact match not found (default: true)

**Example:**
```json
{
  "name": "page",
  "arguments": {
    "title": "Earth",
    "auto_suggest": true
  }
}
```

## How It Works

### Language Priority System

1. **Simple English First**: All requests start with Simple English Wikipedia
2. **Quality Check**: For page requests, checks if content is substantial (>500 characters)
3. **Automatic Fallback**: Switches to English Wikipedia if:
   - Page doesn't exist in Simple English
   - Content is too brief (likely a stub)
   - Search returns no results

### Error Handling

- **Disambiguation**: When multiple pages match, returns list of options
- **Page Not Found**: Clear error messages with suggestions
- **Network Issues**: Graceful error handling with informative messages

## Use Cases

### For Students & Learners
- Get simplified explanations of complex topics
- Access educational content in clearer language
- Research assistance with automatic complexity adjustment

### For Content Creation
- Source material for articles and explanations
- Fact-checking with reliable Wikipedia sources
- Research support with readability optimization

### For Accessibility
- Easier-to-read content for various reading levels
- Simplified language for non-native speakers
- Clear, concise information delivery

## Examples

### Basic Search
Ask your AI assistant: *"Search Wikipedia for information about photosynthesis"*

The server will:
1. Search Simple English Wikipedia for "photosynthesis"
2. Return a list of relevant articles
3. Fall back to English Wikipedia if needed

### Page Retrieval
Ask your AI assistant: *"Get the Wikipedia page about the Moon"*

The server will:
1. Try to fetch "Moon" from Simple English Wikipedia
2. Check if the content is substantial enough
3. Return Simple English version or fall back to English
4. Include full page content and summary

### Disambiguation Handling
Ask your AI assistant: *"Get information about Mercury"*

If multiple pages match (planet Mercury, element Mercury, etc.), the server will return a list of options to choose from.

## Development

### Project Structure
```
mcp-se-wikipedia/
├── main.py          # Main MCP server implementation
├── pyproject.toml   # Project dependencies and metadata
├── AGENT.md         # This documentation
└── .venv/           # Virtual environment (created by uv)
```

### Key Dependencies
- `mcp`: Model Context Protocol framework
- `wikipedia`: Python Wikipedia API wrapper
- `asyncio`: Async/await support for MCP

### Customization

The server can be easily customized by modifying `main.py`:

- **Quality Threshold**: Change the 500-character threshold for content quality
- **Search Limits**: Modify default and maximum search result limits
- **Language Settings**: Add support for other Wikipedia languages
- **Content Filtering**: Add custom content processing or filtering

### Testing the Server

Test the server directly:
```bash
uvx git+https://github.com/bhubbb/mcp-se-wikipedia mcp-se-wikipedia
```

Or with local installation:
```bash
cd mcp-se-wikipedia
uv run python main.py
```

The server communicates via JSON-RPC over stdin/stdout, so you'll need an MCP client or AI assistant to interact with it properly.

## Troubleshooting

### Common Issues

1. **Import Errors**: Make sure all dependencies are installed with `uv sync`
2. **Connection Issues**: Check network connectivity for Wikipedia API access
3. **Rate Limiting**: Wikipedia has rate limits; the server handles this gracefully

### Debugging

Enable debug logging by modifying the logging level in `main.py`:
```python
logging.basicConfig(level=logging.DEBUG)
```

## Contributing

This is a simple, single-file implementation designed for clarity and ease of modification. Feel free to:

- Add new Wikipedia language support
- Implement additional content filtering
- Add caching for better performance
- Extend with additional Wikipedia features

## License

This project uses the same license as its dependencies. The Wikipedia content accessed through this server is subject to Wikipedia's licensing terms.

---

*This MCP server makes Wikipedia more accessible by prioritizing Simple English content while maintaining access to the full breadth of Wikipedia knowledge.*