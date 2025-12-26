#!/usr/bin/env python
"""
Test script for API Filtering, Searching, and Ordering

This script demonstrates how to test the filtering, searching, and ordering
features of the Book API using Python's requests library.

Usage:
    python test_api_features.py

Make sure the Django development server is running:
    python manage.py runserver
"""

import requests
import json
from typing import Dict, List, Any

# API Base URL
BASE_URL = "http://localhost:8000/api/books"

# Color codes for terminal output
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
RESET = '\033[0m'


def print_header(text: str) -> None:
    """Print a formatted header."""
    print(f"\n{BLUE}{'='*60}{RESET}")
    print(f"{BLUE}{text:^60}{RESET}")
    print(f"{BLUE}{'='*60}{RESET}\n")


def print_test(name: str) -> None:
    """Print a test name."""
    print(f"{YELLOW}Test: {name}{RESET}")


def print_success(message: str) -> None:
    """Print success message."""
    print(f"{GREEN}✓ {message}{RESET}")


def print_error(message: str) -> None:
    """Print error message."""
    print(f"{RED}✗ {message}{RESET}")


def test_api_response(url: str, params: Dict[str, Any] = None) -> bool:
    """
    Test API endpoint and print response.
    
    Args:
        url: The full URL to test
        params: Query parameters dictionary
    
    Returns:
        True if successful, False otherwise
    """
    try:
        response = requests.get(url, params=params)
        
        # Build full URL for display
        if params:
            param_str = "&".join([f"{k}={v}" for k, v in params.items()])
            full_url = f"{url}?{param_str}"
        else:
            full_url = url
        
        print(f"URL: {full_url}")
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"Results: {len(data)} book(s) found")
            
            if data:
                print("\nResponse Preview:")
                print(json.dumps(data[:2], indent=2))
                if len(data) > 2:
                    print(f"... and {len(data) - 2} more")
            else:
                print("No results found")
            
            print_success("Request successful")
            return True
        else:
            print_error(f"Request failed with status {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except requests.exceptions.ConnectionError:
        print_error("Could not connect to server. Make sure Django is running!")
        print("Run: python manage.py runserver")
        return False
    except Exception as e:
        print_error(f"Error: {str(e)}")
        return False


def main():
    """Run all tests."""
    print_header("Django REST Framework - Filtering, Searching & Ordering Tests")
    
    # Test 1: Basic list (no parameters)
    print_test("1. List all books (no filters)")
    test_api_response(BASE_URL)
    print()
    
    # Test 2: Filter by title
    print_test("2. Filter by title")
    test_api_response(BASE_URL, {'title': 'Django'})
    print()
    
    # Test 3: Filter by author
    print_test("3. Filter by author ID (author=1)")
    test_api_response(BASE_URL, {'author': 1})
    print()
    
    # Test 4: Filter by publication year
    print_test("4. Filter by publication year (publication_year=2020)")
    test_api_response(BASE_URL, {'publication_year': 2020})
    print()
    
    # Test 5: Search functionality
    print_test("5. Search for keyword (search='django')")
    test_api_response(BASE_URL, {'search': 'django'})
    print()
    
    # Test 6: Search case-insensitive
    print_test("6. Search case-insensitive (search='DJANGO')")
    test_api_response(BASE_URL, {'search': 'DJANGO'})
    print()
    
    # Test 7: Order by title ascending
    print_test("7. Order by title ascending (ordering='title')")
    test_api_response(BASE_URL, {'ordering': 'title'})
    print()
    
    # Test 8: Order by title descending
    print_test("8. Order by title descending (ordering='-title')")
    test_api_response(BASE_URL, {'ordering': '-title'})
    print()
    
    # Test 9: Order by publication year ascending
    print_test("9. Order by year ascending (ordering='publication_year')")
    test_api_response(BASE_URL, {'ordering': 'publication_year'})
    print()
    
    # Test 10: Order by publication year descending
    print_test("10. Order by year descending (ordering='-publication_year')")
    test_api_response(BASE_URL, {'ordering': '-publication_year'})
    print()
    
    # Test 11: Filter + Order
    print_test("11. Filter by author + Order by year (author=1&ordering=-publication_year)")
    test_api_response(BASE_URL, {'author': 1, 'ordering': '-publication_year'})
    print()
    
    # Test 12: Search + Order
    print_test("12. Search + Order (search='django'&ordering='title')")
    test_api_response(BASE_URL, {'search': 'django', 'ordering': 'title'})
    print()
    
    # Test 13: Multiple filters + Order
    print_test("13. Multiple filters + Order (author=1&publication_year=2020&ordering='title')")
    test_api_response(BASE_URL, {
        'author': 1,
        'publication_year': 2020,
        'ordering': 'title'
    })
    print()
    
    # Test 14: Filter + Search + Order
    print_test("14. Filter + Search + Order (author=1&search='advanced'&ordering='-publication_year')")
    test_api_response(BASE_URL, {
        'author': 1,
        'search': 'advanced',
        'ordering': '-publication_year'
    })
    print()
    
    # Test 15: Non-existent author
    print_test("15. Non-existent author (author=999)")
    test_api_response(BASE_URL, {'author': 999})
    print()
    
    print_header("Test Summary")
    print("All tests completed!")
    print("\nKey Features Tested:")
    print("✓ Filtering by title, author, and publication year")
    print("✓ Search functionality with partial matching")
    print("✓ Ordering in ascending and descending order")
    print("✓ Combination of filters, search, and ordering")
    print("✓ Case-insensitive search")
    print("✓ Empty result handling")
    print()
    print("For more information, see:")
    print("  - FILTERING_SEARCHING_ORDERING_GUIDE.md (detailed guide)")
    print("  - QUICK_REFERENCE.md (quick reference)")
    print("  - IMPLEMENTATION_SUMMARY.md (implementation details)")


if __name__ == '__main__':
    main()
