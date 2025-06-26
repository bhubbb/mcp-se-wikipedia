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
- Returns structured metadata and ranked list of relevant page titles
- Tries Simple English first, falls back to English
- Configurable result limits

### 📄 Summary Tool
- Retrieve Wikipedia page summaries/excerpts
- Lightweight, fast responses for quick overviews
- Structured metadata with content length and language indicators
- Automatic disambiguation handling

### 📖 Content Tool
- Retrieve full Wikipedia page content
- Complete article text for detailed research
- Structured output with separate metadata and content blocks
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
Search Wikipedia for articles with structured results.

**Parameters:**
- `query` (required): Search terms
- `limit` (optional): Max results to return (1-20, default: 10)

**Returns:**
- Search metadata (Wikipedia version, query, results count, language code)
- List of matching article titles

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

### `summary`
Get the summary/excerpt of a Wikipedia page.

**Parameters:**
- `title` (required): Page title to retrieve summary for
- `auto_suggest` (optional): Auto-suggest similar titles if exact match not found (default: true)

**Returns:**
- Summary metadata (title, Wikipedia version, language code, URL, content length)
- Page summary text

**Example:**
```json
{
  "name": "summary",
  "arguments": {
    "title": "Earth",
    "auto_suggest": true
  }
}
```

### `content`
Get the full content of a Wikipedia page.

**Parameters:**
- `title` (required): Page title to retrieve full content for
- `auto_suggest` (optional): Auto-suggest similar titles if exact match not found (default: true)

**Returns:**
- Content metadata (title, Wikipedia version, language code, URL, content length)
- Complete article content

**Example:**
```json
{
  "name": "content",
  "arguments": {
    "title": "Earth",
    "auto_suggest": true
  }
}
```

## How It Works

### Language Priority System

1. **Simple English First**: All requests start with Simple English Wikipedia
2. **Quality Check**: For content/summary requests, checks if content is substantial (>500 characters)
3. **Automatic Fallback**: Switches to English Wikipedia if:
   - Page doesn't exist in Simple English
   - Content is too brief (likely a stub)
   - Search returns no results

### Structured Output Format

All tools return structured responses with separate blocks for:
- **Metadata**: Wikipedia version, language codes, URLs, content statistics
- **Content**: Search results, summaries, or full article content
- **Options**: Disambiguation choices when multiple pages match

This structure makes responses both human-readable and machine-parseable.

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
2. Return structured metadata (version, language code, result count)
3. Provide a list of relevant articles
4. Fall back to English Wikipedia if needed

### Summary Retrieval
Ask your AI assistant: *"Get a summary of the Moon from Wikipedia"*

The server will:
1. Try to fetch "Moon" summary from Simple English Wikipedia
2. Return structured metadata (title, version, URL, content length)
3. Provide the page summary
4. Fall back to English Wikipedia if Simple English unavailable

### Full Content Retrieval
Ask your AI assistant: *"Get the full Wikipedia article about the Moon"*

The server will:
1. Try to fetch complete "Moon" article from Simple English Wikipedia
2. Check if the content is substantial enough
3. Return structured metadata and full article content
4. Fall back to English Wikipedia if needed

### Disambiguation Handling
Ask your AI assistant: *"Get information about Mercury"*

If multiple pages match (planet Mercury, element Mercury, etc.), the server will return:
- Structured disambiguation metadata
- A list of options to choose from

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