#!/usr/bin/env python3
"""
Debug test script for Wikipedia MCP Server issues.
Focuses on the specific problems with summary retrieval.
"""

import json

import wikipedia


def test_api_behavior():
    """Test how the wikipedia API behaves with different parameters."""
    print("=" * 60)
    print("TESTING API BEHAVIOR")
    print("=" * 60)

    # Test what happens when we get a page
    print("\n1. Testing page retrieval for 'Earth':")
    print("-" * 40)

    # Simple English
    wikipedia.set_lang("simple")
    print(f"Language set to: simple")
    print(f"API URL: {wikipedia.API_URL}")

    try:
        # First, search to see what titles are available
        search_results = wikipedia.search("Earth", results=3)
        print(f"Search results: {search_results}")

        # Try getting page with exact title
        page = wikipedia.page("Earth", auto_suggest=False)
        print(f"Page title: {page.title}")
        print(f"Page URL: {page.url}")
        print(f"Summary first 100 chars: {page.summary[:100]}...")
    except Exception as e:
        print(f"Error with auto_suggest=False: {e}")

    try:
        # Try with auto_suggest=True
        page = wikipedia.page("Earth", auto_suggest=True)
        print(f"With auto_suggest=True - Page title: {page.title}")
        print(f"Summary first 100 chars: {page.summary[:100]}...")
    except Exception as e:
        print(f"Error with auto_suggest=True: {e}")

    # English
    print("\n2. Testing page retrieval for 'Earth' in English:")
    print("-" * 40)

    wikipedia.set_lang("en")
    print(f"Language set to: en")
    print(f"API URL: {wikipedia.API_URL}")

    try:
        search_results = wikipedia.search("Earth", results=3)
        print(f"Search results: {search_results}")

        page = wikipedia.page("Earth", auto_suggest=False)
        print(f"Page title: {page.title}")
        print(f"Page URL: {page.url}")
        print(f"Summary first 100 chars: {page.summary[:100]}...")
    except Exception as e:
        print(f"Error with auto_suggest=False: {e}")

    try:
        page = wikipedia.page("Earth", auto_suggest=True)
        print(f"With auto_suggest=True - Page title: {page.title}")
        print(f"Summary first 100 chars: {page.summary[:100]}...")
    except Exception as e:
        print(f"Error with auto_suggest=True: {e}")


def test_moon_issue():
    """Test the specific issue with Moon returning Soon."""
    print("\n" + "=" * 60)
    print("TESTING MOON/SOON ISSUE")
    print("=" * 60)

    # Test in Simple English
    print("\n1. Simple English 'Moon':")
    print("-" * 40)
    wikipedia.set_lang("simple")

    try:
        # Search first
        search_results = wikipedia.search("Moon", results=5)
        print(f"Search results: {search_results}")

        # Try without auto_suggest
        page = wikipedia.page("Moon", auto_suggest=False)
        print(f"Without auto_suggest - Title: {page.title}")
        print(f"URL: {page.url}")
    except Exception as e:
        print(f"Error without auto_suggest: {e}")

    try:
        # Try with auto_suggest
        page = wikipedia.page("Moon", auto_suggest=True)
        print(f"With auto_suggest - Title: {page.title}")
        print(f"URL: {page.url}")
    except Exception as e:
        print(f"Error with auto_suggest: {e}")

    # Test in English
    print("\n2. Regular English 'Moon':")
    print("-" * 40)
    wikipedia.set_lang("en")

    try:
        search_results = wikipedia.search("Moon", results=5)
        print(f"Search results: {search_results}")

        page = wikipedia.page("Moon", auto_suggest=False)
        print(f"Without auto_suggest - Title: {page.title}")
        print(f"URL: {page.url}")
    except Exception as e:
        print(f"Error without auto_suggest: {e}")

    try:
        page = wikipedia.page("Moon", auto_suggest=True)
        print(f"With auto_suggest - Title: {page.title}")
        print(f"URL: {page.url}")
    except Exception as e:
        print(f"Error with auto_suggest: {e}")


def test_language_persistence():
    """Test if language settings persist between calls."""
    print("\n" + "=" * 60)
    print("TESTING LANGUAGE PERSISTENCE")
    print("=" * 60)

    # Set to simple, get a page, check if it stays
    wikipedia.set_lang("simple")
    print(f"Set language to 'simple'")
    print(f"API URL: {wikipedia.API_URL}")

    try:
        page1 = wikipedia.page("Water", auto_suggest=False)
        print(f"Page 1 URL: {page1.url}")
    except Exception as e:
        print(f"Error: {e}")

    # Check if language changed
    print(f"API URL after page 1: {wikipedia.API_URL}")

    # Get another page without setting language
    try:
        page2 = wikipedia.page("Sun", auto_suggest=False)
        print(f"Page 2 URL: {page2.url}")
    except Exception as e:
        print(f"Error: {e}")

    print(f"API URL after page 2: {wikipedia.API_URL}")

    # Now switch to en
    wikipedia.set_lang("en")
    print(f"\nSet language to 'en'")
    print(f"API URL: {wikipedia.API_URL}")

    try:
        page3 = wikipedia.page("Water", auto_suggest=False)
        print(f"Page 3 URL: {page3.url}")
    except Exception as e:
        print(f"Error: {e}")

    print(f"API URL after page 3: {wikipedia.API_URL}")


def test_suggest_behavior():
    """Test what auto_suggest actually does."""
    print("\n" + "=" * 60)
    print("TESTING AUTO_SUGGEST BEHAVIOR")
    print("=" * 60)

    test_terms = ["Eart", "Moo", "Watr"]  # Intentionally misspelled

    for term in test_terms:
        print(f"\nTesting '{term}':")
        print("-" * 40)

        # Simple English
        wikipedia.set_lang("simple")
        try:
            page = wikipedia.page(term, auto_suggest=False)
            print(f"Simple - Without suggest: {page.title}")
        except Exception as e:
            print(f"Simple - Without suggest failed: {type(e).__name__}")

        try:
            page = wikipedia.page(term, auto_suggest=True)
            print(f"Simple - With suggest: {page.title}")
        except Exception as e:
            print(f"Simple - With suggest failed: {type(e).__name__}")

        # English
        wikipedia.set_lang("en")
        try:
            page = wikipedia.page(term, auto_suggest=False)
            print(f"English - Without suggest: {page.title}")
        except Exception as e:
            print(f"English - Without suggest failed: {type(e).__name__}")

        try:
            page = wikipedia.page(term, auto_suggest=True)
            print(f"English - With suggest: {page.title}")
        except Exception as e:
            print(f"English - With suggest failed: {type(e).__name__}")


if __name__ == "__main__":
    print("Wikipedia API Debug Testing")
    print("============================\n")

    test_api_behavior()
    test_moon_issue()
    test_language_persistence()
    test_suggest_behavior()

    print("\n" + "=" * 60)
    print("TESTING COMPLETE")
    print("=" * 60)
