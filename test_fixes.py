#!/usr/bin/env python3
"""
Test script to verify the Wikipedia MCP Server fixes.
Tests the key functionality after fixing auto_suggest issues.
"""

import asyncio
import os
import sys

# Add the current directory to path to import main
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from main import handle_content, handle_search, handle_summary


async def test_search():
    """Test search functionality."""
    print("\n" + "=" * 60)
    print("TESTING SEARCH")
    print("=" * 60)

    # Test normal search
    print("\nSearching for 'solar system':")
    results = await handle_search({"query": "solar system", "limit": 3})
    for result in results:
        print(f"- {result.text[:100]}...")

    # Test search with no results
    print("\nSearching for 'asdfghjkl123':")
    results = await handle_search({"query": "asdfghjkl123", "limit": 3})
    for result in results:
        if "Error" in result.text or "not found" in result.text:
            print("✓ Correctly handled no results")
            break


async def test_summary():
    """Test summary functionality."""
    print("\n" + "=" * 60)
    print("TESTING SUMMARY")
    print("=" * 60)

    # Test Earth (should work without auto_suggest)
    print("\nGetting summary for 'Earth' (auto_suggest=False):")
    results = await handle_summary({"title": "Earth", "auto_suggest": False})
    for result in results:
        if "Summary Metadata" in result.text:
            print("✓ Got metadata")
        elif "Page Summary" in result.text:
            print("✓ Got summary")
            print(f"  Preview: {result.text[15:100]}...")

    # Test Moon (previously had issues with auto_suggest)
    print("\nGetting summary for 'Moon' (auto_suggest=False):")
    results = await handle_summary({"title": "Moon", "auto_suggest": False})
    for result in results:
        if "Summary Metadata" in result.text:
            if "Moon" in result.text and "Soon" not in result.text:
                print("✓ Correctly got Moon (not Soon)")

    # Test Mercury (should show disambiguation)
    print("\nGetting summary for 'Mercury' (auto_suggest=False):")
    results = await handle_summary({"title": "Mercury", "auto_suggest": False})
    for result in results:
        if "Disambiguation" in result.text:
            print("✓ Correctly handled disambiguation")

    # Test with misspelling and auto_suggest=True
    print("\nGetting summary for 'Eart' (auto_suggest=True):")
    results = await handle_summary({"title": "Eart", "auto_suggest": True})
    for result in results:
        if "Earth" in result.text or "East" in result.text:
            print("✓ Auto-suggest worked for misspelling")
            break

    # Test nonexistent page
    print("\nGetting summary for 'NonExistentPage123':")
    results = await handle_summary(
        {"title": "NonExistentPage123", "auto_suggest": False}
    )
    for result in results:
        if "not found" in result.text or "Not Found" in result.text:
            print("✓ Correctly handled nonexistent page")
            break


async def test_content():
    """Test content functionality."""
    print("\n" + "=" * 60)
    print("TESTING CONTENT")
    print("=" * 60)

    # Test Water (should work well)
    print("\nGetting content for 'Water' (auto_suggest=False):")
    results = await handle_content({"title": "Water", "auto_suggest": False})
    for result in results:
        if "Content Metadata" in result.text:
            print("✓ Got metadata")
        elif "Page Content" in result.text:
            print("✓ Got content")
            # Check it's substantial
            if len(result.text) > 1000:
                print(f"✓ Content is substantial ({len(result.text)} chars)")


async def test_wikipedia_mode():
    """Test WIKIPEDIA_MODE environment variable."""
    print("\n" + "=" * 60)
    print("TESTING WIKIPEDIA_MODE")
    print("=" * 60)

    # Test default mode (should prioritize Simple English)
    print("\nDefault mode (Simple English priority):")
    os.environ.pop("WIKIPEDIA_MODE", None)

    # Need to reimport to pick up environment change
    import importlib

    import main

    importlib.reload(main)

    results = await main.handle_summary({"title": "Earth", "auto_suggest": False})
    for result in results:
        if "Simple English" in result.text:
            print("✓ Using Simple English in default mode")
            break

    # Test full mode
    print("\nFull Wikipedia mode:")
    os.environ["WIKIPEDIA_MODE"] = "full"
    importlib.reload(main)

    results = await main.handle_summary({"title": "Earth", "auto_suggest": False})
    for result in results:
        if "English" in result.text and "Simple" not in result.text:
            print("✓ Using full English in full mode")
            break

    # Reset environment
    os.environ.pop("WIKIPEDIA_MODE", None)


async def main():
    """Run all tests."""
    print("Wikipedia MCP Server - Fix Verification Tests")
    print("=" * 60)

    try:
        await test_search()
        await test_summary()
        await test_content()
        await test_wikipedia_mode()

        print("\n" + "=" * 60)
        print("ALL TESTS COMPLETED")
        print("=" * 60)
        print("\nIf you see ✓ marks above, the fixes are working correctly!")

    except Exception as e:
        print(f"\n❌ Error during testing: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())
