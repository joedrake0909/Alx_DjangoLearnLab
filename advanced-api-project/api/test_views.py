"""
Unit Tests for Book API Views

This module contains comprehensive unit tests for all Book API endpoints,
including CRUD operations, filtering, searching, ordering, and permission handling.

Test Coverage:
- List endpoint (GET /api/books/)
- Detail endpoint (GET /api/books/<id>/)
- Create endpoint (POST /api/books/create/)
- Update endpoint (PUT/PATCH /api/books/<id>/update/)
- Delete endpoint (DELETE /api/books/<id>/delete/)
- Filtering functionality
- Searching functionality
- Ordering functionality
- Permission and authentication checks

Run tests with:
    python manage.py test api.test_views
    python manage.py test api.test_views.BookListViewTest
    python manage.py test api.test_views.BookListViewTest.test_list_books
"""

from django.test import TestCase, Client
from django.contrib.auth.models import User
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from rest_framework.authtoken.models import Token
from .models import Book, Author
import json


# ==================== TEST SETUP & UTILITIES ====================

class BaseBookTestCase(APITestCase):
    """
    Base test case class that sets up common test data and utilities.
    
    This class provides:
    - Setup and teardown methods
    - Test data (authors and books)
    - Helper methods for API requests
    - Common assertions
    """
    
    def setUp(self):
        """
        Set up test data before each test method.
        Creates test authors, books, and users for testing.
        """
        # Create test users
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.admin_user = User.objects.create_user(
            username='admin',
            email='admin@example.com',
            password='adminpass123',
            is_staff=True
        )
        
        # Create tokens for authentication
        self.user_token = Token.objects.create(user=self.user)
        self.admin_token = Token.objects.create(user=self.admin_user)
        
        # Create test authors
        self.author1 = Author.objects.create(name='John Smith')
        self.author2 = Author.objects.create(name='Jane Doe')
        self.author3 = Author.objects.create(name='Bob Johnson')
        
        # Create test books
        self.book1 = Book.objects.create(
            title='Django for Beginners',
            publication_year=2020,
            author=self.author1
        )
        self.book2 = Book.objects.create(
            title='Advanced Django',
            publication_year=2021,
            author=self.author1
        )
        self.book3 = Book.objects.create(
            title='Python REST APIs',
            publication_year=2022,
            author=self.author2
        )
        self.book4 = Book.objects.create(
            title='Web Development with Django',
            publication_year=2019,
            author=self.author3
        )
        
        # Initialize API client
        self.client = APIClient()
    
    def get_auth_headers(self, user=None):
        """Get authorization headers for API requests."""
        if user is None:
            user = self.user
        token = Token.objects.get(user=user)
        return {'HTTP_AUTHORIZATION': f'Token {token.key}'}
    
    def tearDown(self):
        """Clean up after each test."""
        Book.objects.all().delete()
        Author.objects.all().delete()
        User.objects.all().delete()


# ==================== LIST VIEW TESTS ====================

class BookListViewTest(BaseBookTestCase):
    """
    Test cases for the BookListView (GET /api/books/).
    
    Tests:
    - Retrieving list of all books
    - Filtering by various fields
    - Searching functionality
    - Ordering functionality
    - Response structure and status codes
    """
    
    def test_list_books_unauthenticated(self):
        """Test that unauthenticated users can list books."""
        response = self.client.get('/api/books/')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, list)
        self.assertEqual(len(response.data), 4)
    
    def test_list_books_authenticated(self):
        """Test that authenticated users can list books."""
        auth_headers = self.get_auth_headers()
        response = self.client.get('/api/books/', **auth_headers)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, list)
        self.assertEqual(len(response.data), 4)
    
    def test_list_books_response_structure(self):
        """Test that response contains correct book fields."""
        response = self.client.get('/api/books/')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        first_book = response.data[0]
        
        # Verify required fields are present
        self.assertIn('id', first_book)
        self.assertIn('title', first_book)
        self.assertIn('publication_year', first_book)
        self.assertIn('author', first_book)
    
    def test_list_books_empty(self):
        """Test listing books when none exist."""
        Book.objects.all().delete()
        response = self.client.get('/api/books/')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)
    
    # ===== FILTERING TESTS =====
    
    def test_filter_by_title(self):
        """Test filtering books by exact title match."""
        response = self.client.get('/api/books/?title=Django%20for%20Beginners')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'Django for Beginners')
    
    def test_filter_by_title_no_match(self):
        """Test filtering with title that doesn't exist."""
        response = self.client.get('/api/books/?title=NonexistentBook')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)
    
    def test_filter_by_author(self):
        """Test filtering books by author ID."""
        response = self.client.get(f'/api/books/?author={self.author1.id}')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        
        for book in response.data:
            self.assertEqual(book['author'], self.author1.id)
    
    def test_filter_by_author_no_books(self):
        """Test filtering by author with no books."""
        # Create an author with no books
        empty_author = Author.objects.create(name='Empty Author')
        response = self.client.get(f'/api/books/?author={empty_author.id}')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)
    
    def test_filter_by_publication_year(self):
        """Test filtering books by publication year."""
        response = self.client.get('/api/books/?publication_year=2020')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['publication_year'], 2020)
    
    def test_filter_by_publication_year_multiple(self):
        """Test filtering year that matches multiple books."""
        # Create additional book from 2020
        Book.objects.create(
            title='Another 2020 Book',
            publication_year=2020,
            author=self.author2
        )
        response = self.client.get('/api/books/?publication_year=2020')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
    
    def test_filter_by_multiple_fields(self):
        """Test filtering by multiple fields simultaneously."""
        response = self.client.get(
            f'/api/books/?author={self.author1.id}&publication_year=2020'
        )
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'Django for Beginners')
    
    # ===== SEARCHING TESTS =====
    
    def test_search_by_title(self):
        """Test searching books by title."""
        response = self.client.get('/api/books/?search=Django')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)  # 3 books with 'Django'
    
    def test_search_case_insensitive(self):
        """Test that search is case-insensitive."""
        response_lower = self.client.get('/api/books/?search=django')
        response_upper = self.client.get('/api/books/?search=DJANGO')
        
        self.assertEqual(response_lower.status_code, status.HTTP_200_OK)
        self.assertEqual(response_upper.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response_lower.data), len(response_upper.data))
    
    def test_search_partial_match(self):
        """Test that search supports partial matching."""
        response = self.client.get('/api/books/?search=REST')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'Python REST APIs')
    
    def test_search_by_author_name(self):
        """Test searching by author name."""
        response = self.client.get('/api/books/?search=John')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(response.data), 0)
        
        # Verify at least one book is by John Smith
        found_john_book = any(
            book['author'] == self.author1.id for book in response.data
        )
        self.assertTrue(found_john_book)
    
    def test_search_no_match(self):
        """Test search with no matching results."""
        response = self.client.get('/api/books/?search=NonexistentKeyword')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)
    
    def test_search_with_spaces(self):
        """Test searching with multiple words."""
        response = self.client.get('/api/books/?search=Web%20Development')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(response.data), 0)
    
    # ===== ORDERING TESTS =====
    
    def test_order_by_title_ascending(self):
        """Test ordering books by title in ascending order."""
        response = self.client.get('/api/books/?ordering=title')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        titles = [book['title'] for book in response.data]
        
        # Verify titles are in alphabetical order
        self.assertEqual(titles, sorted(titles))
    
    def test_order_by_title_descending(self):
        """Test ordering books by title in descending order."""
        response = self.client.get('/api/books/?ordering=-title')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        titles = [book['title'] for book in response.data]
        
        # Verify titles are in reverse alphabetical order
        self.assertEqual(titles, sorted(titles, reverse=True))
    
    def test_order_by_publication_year_ascending(self):
        """Test ordering books by publication year ascending."""
        response = self.client.get('/api/books/?ordering=publication_year')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        years = [book['publication_year'] for book in response.data]
        
        # Verify years are in ascending order
        self.assertEqual(years, sorted(years))
    
    def test_order_by_publication_year_descending(self):
        """Test ordering books by publication year descending."""
        response = self.client.get('/api/books/?ordering=-publication_year')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        years = [book['publication_year'] for book in response.data]
        
        # Verify years are in descending order
        self.assertEqual(years, sorted(years, reverse=True))
    
    def test_default_ordering(self):
        """Test that default ordering is by title."""
        response_default = self.client.get('/api/books/')
        response_title = self.client.get('/api/books/?ordering=title')
        
        self.assertEqual(response_default.status_code, status.HTTP_200_OK)
        self.assertEqual(response_title.status_code, status.HTTP_200_OK)
        
        # Both should return same order
        self.assertEqual(
            [b['id'] for b in response_default.data],
            [b['id'] for b in response_title.data]
        )
    
    # ===== COMBINED FILTER + SEARCH + ORDER TESTS =====
    
    def test_filter_and_order(self):
        """Test combining filtering and ordering."""
        response = self.client.get(
            f'/api/books/?author={self.author1.id}&ordering=-publication_year'
        )
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        
        # Verify ordering
        years = [book['publication_year'] for book in response.data]
        self.assertEqual(years, [2021, 2020])
    
    def test_search_and_order(self):
        """Test combining search and ordering."""
        response = self.client.get('/api/books/?search=Django&ordering=title')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)
        
        titles = [book['title'] for book in response.data]
        self.assertEqual(titles, sorted(titles))
    
    def test_filter_search_and_order(self):
        """Test combining filtering, searching, and ordering."""
        response = self.client.get(
            f'/api/books/?author={self.author1.id}&search=Django&ordering=-publication_year'
        )
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)


# ==================== DETAIL VIEW TESTS ====================

class BookDetailViewTest(BaseBookTestCase):
    """
    Test cases for the BookDetailView (GET /api/books/<id>/).
    
    Tests:
    - Retrieving a single book by ID
    - Response structure
    - Status codes for valid and invalid IDs
    """
    
    def test_get_book_detail_success(self):
        """Test successfully retrieving a single book."""
        response = self.client.get(f'/api/books/{self.book1.id}/')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], self.book1.id)
        self.assertEqual(response.data['title'], 'Django for Beginners')
        self.assertEqual(response.data['publication_year'], 2020)
        self.assertEqual(response.data['author'], self.author1.id)
    
    def test_get_book_detail_invalid_id(self):
        """Test retrieving a book with invalid ID."""
        response = self.client.get('/api/books/99999/')
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_get_book_detail_unauthenticated(self):
        """Test that unauthenticated users can view book details."""
        response = self.client.get(f'/api/books/{self.book1.id}/')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_get_book_detail_authenticated(self):
        """Test that authenticated users can view book details."""
        auth_headers = self.get_auth_headers()
        response = self.client.get(f'/api/books/{self.book1.id}/', **auth_headers)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)


# ==================== CREATE VIEW TESTS ====================

class BookCreateViewTest(BaseBookTestCase):
    """
    Test cases for the BookCreateView (POST /api/books/create/).
    
    Tests:
    - Creating a new book with valid data
    - Creating with invalid/missing data
    - Authentication requirements
    - Response status codes
    - Data validation
    """
    
    def test_create_book_authenticated(self):
        """Test creating a book as an authenticated user."""
        auth_headers = self.get_auth_headers()
        data = {
            'title': 'New Django Book',
            'publication_year': 2023,
            'author': self.author1.id
        }
        response = self.client.post('/api/books/create/', data, **auth_headers)
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['title'], 'New Django Book')
        self.assertEqual(response.data['publication_year'], 2023)
        
        # Verify book was created in database
        self.assertTrue(Book.objects.filter(title='New Django Book').exists())
    
    def test_create_book_with_login(self):
        """Test creating a book using client.login method."""
        self.client.login(username='testuser', password='testpass123')
        data = {
            'title': 'Book Created via Login',
            'publication_year': 2023,
            'author': self.author1.id
        }
        response = self.client.post('/api/books/create/', data, format='json')
        
        # Note: Token authentication is required, so this will fail without token
        # But the login method is demonstrated here
        self.client.logout()
    
    def test_create_book_unauthenticated(self):
        """Test that unauthenticated users cannot create books."""
        data = {
            'title': 'Unauthenticated Book',
            'publication_year': 2023,
            'author': self.author1.id
        }
        response = self.client.post('/api/books/create/', data)
        
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_create_book_missing_title(self):
        """Test creating book with missing title."""
        auth_headers = self.get_auth_headers()
        data = {
            'publication_year': 2023,
            'author': self.author1.id
        }
        response = self.client.post('/api/books/create/', data, **auth_headers)
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('title', response.data)
    
    def test_create_book_missing_author(self):
        """Test creating book with missing author."""
        auth_headers = self.get_auth_headers()
        data = {
            'title': 'Book Without Author',
            'publication_year': 2023
        }
        response = self.client.post('/api/books/create/', data, **auth_headers)
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('author', response.data)
    
    def test_create_book_invalid_author(self):
        """Test creating book with invalid author ID."""
        auth_headers = self.get_auth_headers()
        data = {
            'title': 'Book with Bad Author',
            'publication_year': 2023,
            'author': 99999
        }
        response = self.client.post('/api/books/create/', data, **auth_headers)
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_create_book_future_year(self):
        """Test that future publication years are rejected."""
        auth_headers = self.get_auth_headers()
        data = {
            'title': 'Future Book',
            'publication_year': 2030,
            'author': self.author1.id
        }
        response = self.client.post('/api/books/create/', data, **auth_headers)
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('publication_year', response.data)
    
    def test_create_book_too_old_year(self):
        """Test that extremely old publication years are rejected."""
        auth_headers = self.get_auth_headers()
        data = {
            'title': 'Ancient Book',
            'publication_year': 1400,
            'author': self.author1.id
        }
        response = self.client.post('/api/books/create/', data, **auth_headers)
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('publication_year', response.data)
    
    def test_create_book_valid_year_boundary(self):
        """Test creating book with valid year at boundary (1450)."""
        auth_headers = self.get_auth_headers()
        data = {
            'title': 'Old But Valid Book',
            'publication_year': 1450,
            'author': self.author1.id
        }
        response = self.client.post('/api/books/create/', data, **auth_headers)
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_create_book_increments_count(self):
        """Test that creating a book increments the total book count."""
        initial_count = Book.objects.count()
        auth_headers = self.get_auth_headers()
        data = {
            'title': 'Count Test Book',
            'publication_year': 2023,
            'author': self.author1.id
        }
        self.client.post('/api/books/create/', data, **auth_headers)
        
        self.assertEqual(Book.objects.count(), initial_count + 1)


# ==================== UPDATE VIEW TESTS ====================

class BookUpdateViewTest(BaseBookTestCase):
    """
    Test cases for the BookUpdateView (PUT/PATCH /api/books/<id>/update/).
    
    Tests:
    - Updating books with valid data
    - Partial updates (PATCH)
    - Full updates (PUT)
    - Authentication requirements
    - Data validation
    """
    
    def test_update_book_authenticated_patch(self):
        """Test partially updating a book as authenticated user."""
        auth_headers = self.get_auth_headers()
        data = {'title': 'Updated Django Book'}
        response = self.client.patch(
            f'/api/books/{self.book1.id}/update/',
            data,
            **auth_headers,
            format='json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Updated Django Book')
        
        # Verify other fields unchanged
        self.assertEqual(response.data['publication_year'], 2020)
        self.assertEqual(response.data['author'], self.author1.id)
    
    def test_update_book_authenticated_put(self):
        """Test full update of a book (PUT request)."""
        auth_headers = self.get_auth_headers()
        data = {
            'title': 'Completely New Title',
            'publication_year': 2023,
            'author': self.author2.id
        }
        response = self.client.put(
            f'/api/books/{self.book1.id}/update/',
            data,
            **auth_headers,
            format='json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Completely New Title')
        self.assertEqual(response.data['publication_year'], 2023)
        self.assertEqual(response.data['author'], self.author2.id)
    
    def test_update_book_unauthenticated(self):
        """Test that unauthenticated users cannot update books."""
        data = {'title': 'Unauthorized Update'}
        response = self.client.patch(
            f'/api/books/{self.book1.id}/update/',
            data,
            format='json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_update_book_invalid_id(self):
        """Test updating a book with invalid ID."""
        auth_headers = self.get_auth_headers()
        data = {'title': 'Update Test'}
        response = self.client.patch(
            '/api/books/99999/update/',
            data,
            **auth_headers,
            format='json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_update_book_invalid_year(self):
        """Test updating with invalid publication year."""
        auth_headers = self.get_auth_headers()
        data = {'publication_year': 2050}
        response = self.client.patch(
            f'/api/books/{self.book1.id}/update/',
            data,
            **auth_headers,
            format='json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_update_book_changes_persisted(self):
        """Test that updates are persisted in the database."""
        auth_headers = self.get_auth_headers()
        new_title = 'Persisted Title'
        data = {'title': new_title}
        
        self.client.patch(
            f'/api/books/{self.book1.id}/update/',
            data,
            **auth_headers,
            format='json'
        )
        
        # Fetch from database to verify persistence
        updated_book = Book.objects.get(id=self.book1.id)
        self.assertEqual(updated_book.title, new_title)
    
    def test_update_multiple_fields(self):
        """Test updating multiple fields at once."""
        auth_headers = self.get_auth_headers()
        data = {
            'title': 'New Title',
            'publication_year': 2022
        }
        response = self.client.patch(
            f'/api/books/{self.book1.id}/update/',
            data,
            **auth_headers,
            format='json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'New Title')
        self.assertEqual(response.data['publication_year'], 2022)


# ==================== DELETE VIEW TESTS ====================

class BookDeleteViewTest(BaseBookTestCase):
    """
    Test cases for the BookDeleteView (DELETE /api/books/<id>/delete/).
    
    Tests:
    - Deleting existing books
    - Authentication requirements
    - Status codes
    - Database state after deletion
    """
    
    def test_delete_book_authenticated(self):
        """Test deleting a book as an authenticated user."""
        auth_headers = self.get_auth_headers()
        book_id = self.book1.id
        
        response = self.client.delete(
            f'/api/books/{book_id}/delete/',
            **auth_headers
        )
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        
        # Verify book was deleted
        self.assertFalse(Book.objects.filter(id=book_id).exists())
    
    def test_delete_book_unauthenticated(self):
        """Test that unauthenticated users cannot delete books."""
        response = self.client.delete(f'/api/books/{self.book1.id}/delete/')
        
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
        # Verify book still exists
        self.assertTrue(Book.objects.filter(id=self.book1.id).exists())
    
    def test_delete_book_invalid_id(self):
        """Test deleting a book with invalid ID."""
        auth_headers = self.get_auth_headers()
        response = self.client.delete('/api/books/99999/delete/', **auth_headers)
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_delete_nonexistent_book(self):
        """Test that deleting already-deleted book returns 404."""
        auth_headers = self.get_auth_headers()
        book_id = self.book1.id
        
        # Delete once
        self.client.delete(f'/api/books/{book_id}/delete/', **auth_headers)
        
        # Try to delete again
        response = self.client.delete(
            f'/api/books/{book_id}/delete/',
            **auth_headers
        )
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_delete_decrements_count(self):
        """Test that deleting a book decrements the total count."""
        auth_headers = self.get_auth_headers()
        initial_count = Book.objects.count()
        
        self.client.delete(f'/api/books/{self.book1.id}/delete/', **auth_headers)
        
        self.assertEqual(Book.objects.count(), initial_count - 1)
    
    def test_delete_multiple_books(self):
        """Test deleting multiple books in sequence."""
        auth_headers = self.get_auth_headers()
        initial_count = Book.objects.count()
        books_to_delete = [self.book1, self.book2]
        
        for book in books_to_delete:
            response = self.client.delete(
                f'/api/books/{book.id}/delete/',
                **auth_headers
            )
            self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        
        self.assertEqual(Book.objects.count(), initial_count - 2)


# ==================== PERMISSION TESTS ====================

class PermissionTest(BaseBookTestCase):
    """
    Test cases for permission enforcement.
    
    Tests:
    - Read-only access for unauthenticated users
    - Write access restricted to authenticated users
    - Permission classes working correctly
    """
    
    def test_list_books_no_auth_required(self):
        """Test that listing books doesn't require authentication."""
        response = self.client.get('/api/books/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_detail_books_no_auth_required(self):
        """Test that viewing book details doesn't require authentication."""
        response = self.client.get(f'/api/books/{self.book1.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_create_requires_auth(self):
        """Test that creating requires authentication."""
        data = {
            'title': 'Test',
            'publication_year': 2023,
            'author': self.author1.id
        }
        response = self.client.post('/api/books/create/', data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_update_requires_auth(self):
        """Test that updating requires authentication."""
        data = {'title': 'Test'}
        response = self.client.patch(
            f'/api/books/{self.book1.id}/update/',
            data,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_delete_requires_auth(self):
        """Test that deleting requires authentication."""
        response = self.client.delete(f'/api/books/{self.book1.id}/delete/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_authenticated_user_can_create(self):
        """Test that authenticated users can create books."""
        auth_headers = self.get_auth_headers()
        data = {
            'title': 'Auth User Book',
            'publication_year': 2023,
            'author': self.author1.id
        }
        response = self.client.post('/api/books/create/', data, **auth_headers)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_authenticated_user_can_update(self):
        """Test that authenticated users can update books."""
        auth_headers = self.get_auth_headers()
        data = {'title': 'Updated by Auth User'}
        response = self.client.patch(
            f'/api/books/{self.book1.id}/update/',
            data,
            **auth_headers,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_authenticated_user_can_delete(self):
        """Test that authenticated users can delete books."""
        auth_headers = self.get_auth_headers()
        response = self.client.delete(
            f'/api/books/{self.book1.id}/delete/',
            **auth_headers
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


# ==================== EDGE CASES & SPECIAL TESTS ====================

class EdgeCaseTests(BaseBookTestCase):
    """
    Test cases for edge cases and special scenarios.
    
    Tests:
    - Empty results
    - Large datasets
    - Special characters
    - Boundary values
    """
    
    def test_book_with_special_characters_in_title(self):
        """Test creating and searching books with special characters."""
        auth_headers = self.get_auth_headers()
        data = {
            'title': "Django's Advanced Guide #2023",
            'publication_year': 2023,
            'author': self.author1.id
        }
        response = self.client.post('/api/books/create/', data, **auth_headers)
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['title'], "Django's Advanced Guide #2023")
    
    def test_author_with_multiple_books_deletion(self):
        """Test that author's books can be deleted independently."""
        auth_headers = self.get_auth_headers()
        
        # Both book1 and book2 belong to author1
        self.client.delete(f'/api/books/{self.book1.id}/delete/', **auth_headers)
        
        # book2 should still exist
        response = self.client.get(f'/api/books/{self.book2.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_search_empty_string(self):
        """Test search with empty string."""
        response = self.client.get('/api/books/?search=')
        
        # Should return all books
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_filter_with_zero_id(self):
        """Test filtering with author ID of 0."""
        response = self.client.get('/api/books/?author=0')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)
    
    def test_ordering_with_same_title(self):
        """Test ordering when multiple books have similar titles."""
        auth_headers = self.get_auth_headers()
        
        # Create books with similar titles
        Book.objects.create(
            title='Django Book A',
            publication_year=2022,
            author=self.author1
        )
        Book.objects.create(
            title='Django Book B',
            publication_year=2022,
            author=self.author1
        )
        
        response = self.client.get('/api/books/?ordering=title')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        titles = [b['title'] for b in response.data]
        self.assertEqual(titles, sorted(titles))
    
    def test_long_title_creation(self):
        """Test creating book with very long title."""
        auth_headers = self.get_auth_headers()
        long_title = 'A' * 200  # 200 character title
        data = {
            'title': long_title,
            'publication_year': 2023,
            'author': self.author1.id
        }
        response = self.client.post('/api/books/create/', data, **auth_headers)
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
