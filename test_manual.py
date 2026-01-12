#!/usr/bin/env python3
"""
Manual test script for Wikipedia MCP Server functionality.
Tests the Wikipedia API directly to debug issues.
"""

import traceback

import wikipedia


def test_search():
    """Test search functionality."""
    print("\n" + "=" * 60)
    print("TESTING SEARCH FUNCTIONALITY")
    print("=" * 60)

    test_queries = ["solar system", "Earth", "photosynthesis", "asdfghjkl123"]

    for query in test_queries:
        print(f"\nSearching for: '{query}'")
        print("-" * 40)

        # Test Simple English
        try:
            wikipedia.set_lang("simple")
            results = wikipedia.search(query, results=5)
            print(f"Simple English results ({len(results)}): {results}")
        except Exception as e:
            print(f"Simple English error: {e}")
            traceback.print_exc()

        # Test Regular English
        try:
            wikipedia.set_lang("en")
            results = wikipedia.search(query, results=5)
            print(f"Regular English results ({len(results)}): {results}")
        except Exception as e:
            print(f"Regular English error: {e}")
            traceback.print_exc()


def test_summary():
    """Test summary functionality."""
    print("\n" + "=" * 60)
    print("TESTING SUMMARY FUNCTIONALITY")
    print("=" * 60)

    test_titles = ["Earth", "Mercury", "Moon", "NonExistentPage123"]

    for title in test_titles:
        print(f"\nGetting summary for: '{title}'")
        print("-" * 40)

        # Test Simple English
        try:
            wikipedia.set_lang("simple")
            page = wikipedia.page(title, auto_suggest=True)
            summary = (
                page.summary[:200] + "..." if len(page.summary) > 200 else page.summary
            )
            print(f"Simple English summary: {summary}")
            print(f"Content length: {len(page.content)} characters")
        except wikipedia.exceptions.DisambiguationError as e:
            print(f"Simple English disambiguation: {e.options[:5]}")
        except wikipedia.exceptions.PageError as e:
            print(f"Simple English page not found: {e}")
        except Exception as e:
            print(f"Simple English error: {e}")
            traceback.print_exc()

        # Test Regular English
        try:
            wikipedia.set_lang("en")
            page = wikipedia.page(title, auto_suggest=True)
            summary = (
                page.summary[:200] + "..." if len(page.summary) > 200 else page.summary
            )
            print(f"Regular English summary: {summary}")
            print(f"Content length: {len(page.content)} characters")
        except wikipedia.exceptions.DisambiguationError as e:
            print(f"Regular English disambiguation: {e.options[:5]}")
        except wikipedia.exceptions.PageError as e:
            print(f"Regular English page not found: {e}")
        except Exception as e:
            print(f"Regular English error: {e}")
            traceback.print_exc()


def test_content():
    """Test content retrieval functionality."""
    print("\n" + "=" * 60)
    print("TESTING CONTENT FUNCTIONALITY")
    print("=" * 60)

    test_titles = ["Moon", "Water"]

    for title in test_titles:
        print(f"\nGetting content for: '{title}'")
        print("-" * 40)

        # Test Simple English
        try:
            wikipedia.set_lang("simple")
            page = wikipedia.page(title, auto_suggest=True)
            content_preview = (
                page.content[:300] + "..." if len(page.content) > 300 else page.content
            )
            print(f"Simple English content preview: {content_preview}")
            print(f"Total content length: {len(page.content)} characters")
            print(f"URL: {page.url}")
        except wikipedia.exceptions.DisambiguationError as e:
            print(f"Simple English disambiguation: {e.options[:5]}")
        except wikipedia.exceptions.PageError as e:
            print(f"Simple English page not found: {e}")
        except Exception as e:
            print(f"Simple English error: {e}")
            traceback.print_exc()

        # Test Regular English
        try:
            wikipedia.set_lang("en")
            page = wikipedia.page(title, auto_suggest=True)
            content_preview = (
                page.content[:300] + "..." if len(page.content) > 300 else page.content
            )
            print(f"Regular English content preview: {content_preview}")
            print(f"Total content length: {len(page.content)} characters")
            print(f"URL: {page.url}")
        except wikipedia.exceptions.DisambiguationError as e:
            print(f"Regular English disambiguation: {e.options[:5]}")
        except wikipedia.exceptions.PageError as e:
            print(f"Regular English page not found: {e}")
        except Exception as e:
            print(f"Regular English error: {e}")
            traceback.print_exc()


def test_language_setting():
    """Test language setting behavior."""
    print("\n" + "=" * 60)
    print("TESTING LANGUAGE SETTING")
    print("=" * 60)

    # Check if language setting persists
    wikipedia.set_lang("simple")
    print(f"Set language to 'simple'")
    results1 = wikipedia.search("Earth", results=2)
    print(f"Results after setting to simple: {results1}")

    wikipedia.set_lang("en")
    print(f"Set language to 'en'")
    results2 = wikipedia.search("Earth", results=2)
    print(f"Results after setting to en: {results2}")

    # Check current language API endpoint
    print(f"\nCurrent API URL: {wikipedia.API_URL}")


if __name__ == "__main__":
    print("Wikipedia MCP Server - Manual Testing")
    print("======================================")

    # Test each component
    test_language_setting()
    test_search()
    test_summary()
    test_content()

    print("\n" + "=" * 60)
    print("TESTING COMPLETE")
    print("=" * 60)
