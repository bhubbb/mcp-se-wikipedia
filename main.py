#!/usr/bin/env python3
"""
Wikipedia Simple English MCP Server

A Model Context Protocol server that provides access to Wikipedia content,
prioritizing Simple English Wikipedia with fallback to regular English.
"""

import asyncio
import logging
import os
from typing import Any

import mcp.types as types
import wikipedia
from mcp.server import NotificationOptions, Server
from mcp.server.models import InitializationOptions
from mcp.types import Tool

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("wikipedia-mcp")

# Initialize the MCP server
server = Server("wikipedia-se")

# Check environment variable for Wikipedia mode
# Set WIKIPEDIA_MODE=full to use full Wikipedia only (skip Simple English)
WIKIPEDIA_MODE = os.environ.get("WIKIPEDIA_MODE", "simple").lower()
USE_SIMPLE_FIRST = WIKIPEDIA_MODE != "full"


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
                        "description": "Search query for Wikipedia articles",
                    },
                    "limit": {
                        "type": "integer",
                        "description": "Maximum number of search results to return (default: 10)",
                        "default": 10,
                        "minimum": 1,
                        "maximum": 20,
                    },
                },
                "required": ["query"],
            },
        ),
        Tool(
            name="summary",
            description="Get the summary of a specific Wikipedia page. Tries Simple English first, falls back to English.",
            inputSchema={
                "type": "object",
                "properties": {
                    "title": {
                        "type": "string",
                        "description": "Title of the Wikipedia page to get summary for",
                    },
                    "auto_suggest": {
                        "type": "boolean",
                        "description": "Whether to automatically suggest similar titles if exact match not found (default: false)",
                        "default": False,
                    },
                },
                "required": ["title"],
            },
        ),
        Tool(
            name="content",
            description="Get the full content of a specific Wikipedia page. Tries Simple English first, falls back to English.",
            inputSchema={
                "type": "object",
                "properties": {
                    "title": {
                        "type": "string",
                        "description": "Title of the Wikipedia page to retrieve full content for",
                    },
                    "auto_suggest": {
                        "type": "boolean",
                        "description": "Whether to automatically suggest similar titles if exact match not found (default: false)",
                        "default": False,
                    },
                },
                "required": ["title"],
            },
        ),
    ]


@server.call_tool()
async def handle_call_tool(
    name: str, arguments: dict[str, Any]
) -> list[types.TextContent]:
    """
    Handle tool execution requests.
    Tools can modify server state and notify clients of changes.
    """

    if name == "search":
        return await handle_search(arguments)
    elif name == "summary":
        return await handle_summary(arguments)
    elif name == "content":
        return await handle_content(arguments)
    else:
        raise ValueError(f"Unknown tool: {name}")


async def handle_search(arguments: dict[str, Any]) -> list[types.TextContent]:
    """Handle Wikipedia search requests."""
    query = arguments.get("query")
    limit = arguments.get("limit", 10)

    if not query:
        raise ValueError("Query parameter is required")

    results = []

    # Try Simple English Wikipedia first (unless WIKIPEDIA_MODE=full)
    if USE_SIMPLE_FIRST:
        try:
            wikipedia.set_lang("simple")
            search_results = wikipedia.search(query, results=limit)

            if search_results:
                # Metadata
                results.append(
                    types.TextContent(
                        type="text",
                        text=f"# Search Metadata\n\n**Wikipedia Version:** Simple English\n**Query:** {query}\n**Results Count:** {len(search_results)}\n**Language Code:** simple",
                    )
                )
                # Search Results
                results.append(
                    types.TextContent(
                        type="text",
                        text="# Search Results\n\n"
                        + "\n".join([f"- {result}" for result in search_results]),
                    )
                )
            else:
                # Fallback to English Wikipedia
                wikipedia.set_lang("en")
                search_results = wikipedia.search(query, results=limit)

                if search_results:
                    # Metadata
                    results.append(
                        types.TextContent(
                            type="text",
                            text=f"# Search Metadata\n\n**Wikipedia Version:** English\n**Query:** {query}\n**Results Count:** {len(search_results)}\n**Language Code:** en\n**Note:** Simple English results not available",
                        )
                    )
                    # Search Results
                    results.append(
                        types.TextContent(
                            type="text",
                            text="# Search Results\n\n"
                            + "\n".join([f"- {result}" for result in search_results]),
                        )
                    )
                else:
                    results.append(
                        types.TextContent(
                            type="text",
                            text=f"# Search Metadata\n\n**Wikipedia Version:** None (not found)\n**Query:** {query}\n**Results Count:** 0\n**Language Code:** N/A\n**Error:** No results found in Simple English or English Wikipedia",
                        )
                    )

        except Exception as e:
            logger.error(f"Search error: {e}")
            results.append(
                types.TextContent(
                    type="text",
                    text=f"# Search Error\n\n**Wikipedia Version:** Error\n**Query:** {query}\n**Language Code:** N/A\n**Error:** {str(e)}",
                )
            )
    else:
        # Direct English Wikipedia mode
        try:
            wikipedia.set_lang("en")
            search_results = wikipedia.search(query, results=limit)

            if search_results:
                # Metadata
                results.append(
                    types.TextContent(
                        type="text",
                        text=f"# Search Metadata\n\n**Wikipedia Version:** English\n**Query:** {query}\n**Results Count:** {len(search_results)}\n**Language Code:** en\n**Note:** Simple English results not available",
                    )
                )
                # Search Results
                results.append(
                    types.TextContent(
                        type="text",
                        text="# Search Results\n\n"
                        + "\n".join([f"- {result}" for result in search_results]),
                    )
                )
            else:
                results.append(
                    types.TextContent(
                        type="text",
                        text=f"# Search Metadata\n\n**Wikipedia Version:** None (not found)\n**Query:** {query}\n**Results Count:** 0\n**Language Code:** N/A\n**Error:** No results found in Simple English or English Wikipedia",
                    )
                )

        except Exception as e:
            logger.error(f"Search error: {e}")
            results.append(
                types.TextContent(
                    type="text",
                    text=f"# Search Error\n\n**Wikipedia Version:** Error\n**Query:** {query}\n**Language Code:** N/A\n**Error:** {str(e)}",
                )
            )

    return results


async def handle_summary(arguments: dict[str, Any]) -> list[types.TextContent]:
    """Handle Wikipedia page summary requests."""
    title = arguments.get("title")
    auto_suggest = arguments.get("auto_suggest", False)

    if not title:
        raise ValueError("Title parameter is required")

    results = []

    # Try Simple English Wikipedia first (unless WIKIPEDIA_MODE=full)
    if USE_SIMPLE_FIRST:
        try:
            wikipedia.set_lang("simple")

            try:
                page = wikipedia.page(title, auto_suggest=auto_suggest)

                # Check if the page has reasonable content (not just a stub)
                if len(page.content) > 500:  # Arbitrary threshold for "good quality"
                    # Metadata
                    results.append(
                        types.TextContent(
                            type="text",
                            text=f"# Summary Metadata\n\n**Title:** {page.title}\n**Wikipedia Version:** Simple English\n**Language Code:** simple\n**URL:** {page.url}\n**Content Length:** {len(page.content)} characters",
                        )
                    )
                    # Summary
                    results.append(
                        types.TextContent(
                            type="text", text=f"# Page Summary\n\n{page.summary}"
                        )
                    )
                    return results
            except wikipedia.exceptions.DisambiguationError as e:
                # Handle disambiguation by showing options
                # Metadata
                results.append(
                    types.TextContent(
                        type="text",
                        text=f"# Disambiguation Metadata\n\n**Wikipedia Version:** Simple English\n**Language Code:** simple\n**Requested Title:** {title}\n**Options Count:** {len(e.options[:10])}",
                    )
                )
                # Disambiguation Options
                results.append(
                    types.TextContent(
                        type="text",
                        text="# Disambiguation Options\n\n**Did you mean:**\n"
                        + "\n".join([f"- {option}" for option in e.options[:10]]),
                    )
                )
                return results
            except wikipedia.exceptions.PageError:
                # If auto_suggest is False, try with True before giving up
                if not auto_suggest:
                    try:
                        page = wikipedia.page(title, auto_suggest=True)
                        if len(page.content) > 500:
                            results.append(
                                types.TextContent(
                                    type="text",
                                    text=f"# Summary Metadata\n\n**Title:** {page.title}\n**Wikipedia Version:** Simple English\n**Language Code:** simple\n**URL:** {page.url}\n**Content Length:** {len(page.content)} characters\n**Note:** Auto-suggested from '{title}'",
                                )
                            )
                            results.append(
                                types.TextContent(
                                    type="text",
                                    text=f"# Page Summary\n\n{page.summary}",
                                )
                            )
                            return results
                    except Exception:
                        pass
                # Page doesn't exist in Simple English, will try regular English
                pass
        except Exception as e:
            logger.warning(f"Simple English lookup failed: {e}")

    # Fallback to English Wikipedia (or direct if WIKIPEDIA_MODE=full)
    if not results or not USE_SIMPLE_FIRST:
        try:
            wikipedia.set_lang("en")

            try:
                page = wikipedia.page(title, auto_suggest=auto_suggest)
                # Metadata
                results.append(
                    types.TextContent(
                        type="text",
                        text=f"# Summary Metadata\n\n**Title:** {page.title}\n**Wikipedia Version:** English\n**Language Code:** en\n**URL:** {page.url}\n**Content Length:** {len(page.content)} characters\n**Note:** Simple English version not available",
                    )
                )
                # Summary
                results.append(
                    types.TextContent(
                        type="text", text=f"# Page Summary\n\n{page.summary}"
                    )
                )
            except wikipedia.exceptions.DisambiguationError as e:
                # Metadata
                results.append(
                    types.TextContent(
                        type="text",
                        text=f"# Disambiguation Metadata\n\n**Wikipedia Version:** English\n**Language Code:** en\n**Requested Title:** {title}\n**Options Count:** {len(e.options[:10])}\n**Note:** Simple English version not available",
                    )
                )
                # Disambiguation Options
                results.append(
                    types.TextContent(
                        type="text",
                        text="# Disambiguation Options\n\n**Did you mean:**\n"
                        + "\n".join([f"- {option}" for option in e.options[:10]]),
                    )
                )
            except wikipedia.exceptions.PageError:
                # If auto_suggest is False, try with True before giving up
                if not auto_suggest:
                    try:
                        page = wikipedia.page(title, auto_suggest=True)
                        results.append(
                            types.TextContent(
                                type="text",
                                text=f"# Summary Metadata\n\n**Title:** {page.title}\n**Wikipedia Version:** English\n**Language Code:** en\n**URL:** {page.url}\n**Content Length:** {len(page.content)} characters\n**Note:** Auto-suggested from '{title}'",
                            )
                        )
                        results.append(
                            types.TextContent(
                                type="text", text=f"# Page Summary\n\n{page.summary}"
                            )
                        )
                        return results
                    except Exception:
                        pass
                results.append(
                    types.TextContent(
                        type="text",
                        text=f"# Summary Not Found\n\n**Wikipedia Version:** None (not found)\n**Language Code:** N/A\n**Requested Title:** {title}\n**Error:** Page does not exist in Simple English or English Wikipedia",
                    )
                )

        except Exception as e:
            logger.error(f"Summary retrieval error: {e}")
            results.append(
                types.TextContent(
                    type="text",
                    text=f"# Summary Error\n\n**Wikipedia Version:** Error\n**Language Code:** N/A\n**Requested Title:** {title}\n**Error:** {str(e)}",
                )
            )

    return results


async def handle_content(arguments: dict[str, Any]) -> list[types.TextContent]:
    """Handle Wikipedia page content requests."""
    title = arguments.get("title")
    auto_suggest = arguments.get("auto_suggest", False)

    if not title:
        raise ValueError("Title parameter is required")

    results = []

    # Try Simple English Wikipedia first (unless WIKIPEDIA_MODE=full)
    if USE_SIMPLE_FIRST:
        try:
            wikipedia.set_lang("simple")

            try:
                page = wikipedia.page(title, auto_suggest=auto_suggest)

                # Check if the page has reasonable content (not just a stub)
                if len(page.content) > 500:  # Arbitrary threshold for "good quality"
                    # Metadata
                    results.append(
                        types.TextContent(
                            type="text",
                            text=f"# Content Metadata\n\n**Title:** {page.title}\n**Wikipedia Version:** Simple English\n**Language Code:** simple\n**URL:** {page.url}\n**Content Length:** {len(page.content)} characters",
                        )
                    )
                    # Full Content
                    results.append(
                        types.TextContent(
                            type="text", text=f"# Page Content\n\n{page.content}"
                        )
                    )
                    return results
            except wikipedia.exceptions.DisambiguationError as e:
                # Handle disambiguation by showing options
                # Metadata
                results.append(
                    types.TextContent(
                        type="text",
                        text=f"# Disambiguation Metadata\n\n**Wikipedia Version:** Simple English\n**Language Code:** simple\n**Requested Title:** {title}\n**Options Count:** {len(e.options[:10])}",
                    )
                )
                # Disambiguation Options
                results.append(
                    types.TextContent(
                        type="text",
                        text="# Disambiguation Options\n\n**Did you mean:**\n"
                        + "\n".join([f"- {option}" for option in e.options[:10]]),
                    )
                )
                return results
            except wikipedia.exceptions.PageError:
                # If auto_suggest is False, try with True before giving up
                if not auto_suggest:
                    try:
                        page = wikipedia.page(title, auto_suggest=True)
                        if len(page.content) > 500:
                            results.append(
                                types.TextContent(
                                    type="text",
                                    text=f"# Content Metadata\n\n**Title:** {page.title}\n**Wikipedia Version:** Simple English\n**Language Code:** simple\n**URL:** {page.url}\n**Content Length:** {len(page.content)} characters\n**Note:** Auto-suggested from '{title}'",
                                )
                            )
                            results.append(
                                types.TextContent(
                                    type="text",
                                    text=f"# Page Content\n\n{page.content}",
                                )
                            )
                            return results
                    except Exception:
                        pass
                # Page doesn't exist in Simple English, will try regular English
                pass
        except Exception as e:
            logger.warning(f"Simple English lookup failed: {e}")

    # Fallback to English Wikipedia (or direct if WIKIPEDIA_MODE=full)
    if not results or not USE_SIMPLE_FIRST:
        try:
            wikipedia.set_lang("en")

            try:
                page = wikipedia.page(title, auto_suggest=auto_suggest)
                # Metadata
                results.append(
                    types.TextContent(
                        type="text",
                        text=f"# Content Metadata\n\n**Title:** {page.title}\n**Wikipedia Version:** English\n**Language Code:** en\n**URL:** {page.url}\n**Content Length:** {len(page.content)} characters\n**Note:** Simple English version not available",
                    )
                )
                # Full Content
                results.append(
                    types.TextContent(
                        type="text", text=f"# Page Content\n\n{page.content}"
                    )
                )
            except wikipedia.exceptions.DisambiguationError as e:
                # Metadata
                results.append(
                    types.TextContent(
                        type="text",
                        text=f"# Disambiguation Metadata\n\n**Wikipedia Version:** English\n**Language Code:** en\n**Requested Title:** {title}\n**Options Count:** {len(e.options[:10])}\n**Note:** Simple English version not available",
                    )
                )
                # Disambiguation Options
                results.append(
                    types.TextContent(
                        type="text",
                        text="# Disambiguation Options\n\n**Did you mean:**\n"
                        + "\n".join([f"- {option}" for option in e.options[:10]]),
                    )
                )
            except wikipedia.exceptions.PageError:
                # If auto_suggest is False, try with True before giving up
                if not auto_suggest:
                    try:
                        page = wikipedia.page(title, auto_suggest=True)
                        results.append(
                            types.TextContent(
                                type="text",
                                text=f"# Content Metadata\n\n**Title:** {page.title}\n**Wikipedia Version:** English\n**Language Code:** en\n**URL:** {page.url}\n**Content Length:** {len(page.content)} characters\n**Note:** Auto-suggested from '{title}'",
                            )
                        )
                        results.append(
                            types.TextContent(
                                type="text", text=f"# Page Content\n\n{page.content}"
                            )
                        )
                        return results
                    except Exception:
                        pass
                results.append(
                    types.TextContent(
                        type="text",
                        text=f"# Content Not Found\n\n**Wikipedia Version:** None (not found)\n**Language Code:** N/A\n**Requested Title:** {title}\n**Error:** Page does not exist in Simple English or English Wikipedia",
                    )
                )

        except Exception as e:
            logger.error(f"Content retrieval error: {e}")
            results.append(
                types.TextContent(
                    type="text",
                    text=f"# Content Error\n\n**Wikipedia Version:** Error\n**Language Code:** N/A\n**Requested Title:** {title}\n**Error:** {str(e)}",
                )
            )

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
