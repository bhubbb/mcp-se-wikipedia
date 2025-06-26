#!/usr/bin/env python3
"""
Wikipedia Simple English MCP Server

A Model Context Protocol server that provides access to Wikipedia content,
prioritizing Simple English Wikipedia with fallback to regular English.
"""

import asyncio
import logging
from typing import Any, Sequence
import wikipedia

from mcp.server.models import InitializationOptions
from mcp.server import NotificationOptions, Server
from mcp.types import (
    Tool,
    TextContent,
    LoggingLevel
)
import mcp.types as types

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("wikipedia-mcp")

# Initialize the MCP server
server = Server("wikipedia-se")

@server.list_tools()
async def handle_list_tools() -> list[Tool]:
    """
    List available tools.
    Each tool specifies its arguments using JSON Schema validation.
    """
    return [
        Tool(
            name="search",
            description="Search Wikipedia for articles. Uses Simple English Wikipedia first, falls back to English.",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Search query for Wikipedia articles"
                    },
                    "limit": {
                        "type": "integer",
                        "description": "Maximum number of search results to return (default: 10)",
                        "default": 10,
                        "minimum": 1,
                        "maximum": 20
                    }
                },
                "required": ["query"]
            }
        ),
        Tool(
            name="page",
            description="Get the content of a specific Wikipedia page. Tries Simple English first, falls back to English.",
            inputSchema={
                "type": "object",
                "properties": {
                    "title": {
                        "type": "string",
                        "description": "Title of the Wikipedia page to retrieve"
                    },
                    "auto_suggest": {
                        "type": "boolean",
                        "description": "Whether to automatically suggest similar titles if exact match not found (default: true)",
                        "default": True
                    }
                },
                "required": ["title"]
            }
        )
    ]

@server.call_tool()
async def handle_call_tool(name: str, arguments: dict[str, Any]) -> list[types.TextContent]:
    """
    Handle tool execution requests.
    Tools can modify server state and notify clients of changes.
    """

    if name == "search":
        return await handle_search(arguments)
    elif name == "page":
        return await handle_page(arguments)
    else:
        raise ValueError(f"Unknown tool: {name}")

async def handle_search(arguments: dict[str, Any]) -> list[types.TextContent]:
    """Handle Wikipedia search requests."""
    query = arguments.get("query")
    limit = arguments.get("limit", 10)

    if not query:
        raise ValueError("Query parameter is required")

    results = []

    # Try Simple English Wikipedia first
    try:
        wikipedia.set_lang("simple")
        search_results = wikipedia.search(query, results=limit)

        if search_results:
            results.append(types.TextContent(
                type="text",
                text=f"# Wikipedia Search Results (Simple English)\n\n**Query:** {query}\n\n**Results:**\n" +
                     "\n".join([f"- {result}" for result in search_results])
            ))
        else:
            # Fallback to English Wikipedia
            wikipedia.set_lang("en")
            search_results = wikipedia.search(query, results=limit)

            if search_results:
                results.append(types.TextContent(
                    type="text",
                    text=f"# Wikipedia Search Results (English - Simple English not available)\n\n**Query:** {query}\n\n**Results:**\n" +
                         "\n".join([f"- {result}" for result in search_results])
                ))
            else:
                results.append(types.TextContent(
                    type="text",
                    text=f"# Wikipedia Search Results\n\n**Query:** {query}\n\n**Results:** No results found in Simple English or English Wikipedia."
                ))

    except Exception as e:
        logger.error(f"Search error: {e}")
        results.append(types.TextContent(
            type="text",
            text=f"# Wikipedia Search Error\n\n**Query:** {query}\n\n**Error:** {str(e)}"
        ))

    return results

async def handle_page(arguments: dict[str, Any]) -> list[types.TextContent]:
    """Handle Wikipedia page content requests."""
    title = arguments.get("title")
    auto_suggest = arguments.get("auto_suggest", True)

    if not title:
        raise ValueError("Title parameter is required")

    results = []

    # Try Simple English Wikipedia first
    try:
        wikipedia.set_lang("simple")

        try:
            page = wikipedia.page(title, auto_suggest=auto_suggest)

            # Check if the page has reasonable content (not just a stub)
            if len(page.content) > 500:  # Arbitrary threshold for "good quality"
                results.append(types.TextContent(
                    type="text",
                    text=f"# {page.title} (Simple English Wikipedia)\n\n**URL:** {page.url}\n\n**Summary:**\n{page.summary}\n\n**Full Content:**\n{page.content}"
                ))
                return results
        except wikipedia.exceptions.DisambiguationError as e:
            # Handle disambiguation by showing options
            results.append(types.TextContent(
                type="text",
                text=f"# Disambiguation Required (Simple English)\n\n**Title:** {title}\n\n**Did you mean:**\n" +
                     "\n".join([f"- {option}" for option in e.options[:10]])
            ))
            return results
        except wikipedia.exceptions.PageError:
            # Page doesn't exist in Simple English, will try regular English
            pass
    except Exception as e:
        logger.warning(f"Simple English lookup failed: {e}")

    # Fallback to English Wikipedia
    try:
        wikipedia.set_lang("en")

        try:
            page = wikipedia.page(title, auto_suggest=auto_suggest)
            results.append(types.TextContent(
                type="text",
                text=f"# {page.title} (English Wikipedia - Simple English not available)\n\n**URL:** {page.url}\n\n**Summary:**\n{page.summary}\n\n**Full Content:**\n{page.content}"
            ))
        except wikipedia.exceptions.DisambiguationError as e:
            results.append(types.TextContent(
                type="text",
                text=f"# Disambiguation Required (English)\n\n**Title:** {title}\n\n**Did you mean:**\n" +
                     "\n".join([f"- {option}" for option in e.options[:10]])
            ))
        except wikipedia.exceptions.PageError:
            results.append(types.TextContent(
                type="text",
                text=f"# Page Not Found\n\n**Title:** {title}\n\n**Error:** Page does not exist in Simple English or English Wikipedia."
            ))

    except Exception as e:
        logger.error(f"Page retrieval error: {e}")
        results.append(types.TextContent(
            type="text",
            text=f"# Wikipedia Page Error\n\n**Title:** {title}\n\n**Error:** {str(e)}"
        ))

    return results

async def main():
    # Run the server using stdin/stdout streams
    from mcp.server.stdio import stdio_server

    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="wikipedia-se",
                server_version="0.1.0",
                capabilities=server.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={},
                ),
            ),
        )

def cli():
    """Entry point for the mcp-se-wikipedia command."""
    asyncio.run(main())

if __name__ == "__main__":
    cli()
