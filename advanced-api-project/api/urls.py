from django.urls import path
from .views import (
    BookListView,
    BookDetailView,
    BookCreateView,
    BookUpdateView,
    BookDeleteView
)


# ==================== API URL CONFIGURATION ====================
# This module defines the URL patterns for the Book API endpoints.
# Each URL maps to a specific view that handles CRUD operations.

urlpatterns = [
    # List all books
    # Endpoint: GET /books/
    # View: BookListView
    # Permission: Public (no authentication required)
    # Returns: JSON array of all books
    path('books/', BookListView.as_view(), name='book-list'),
    
    # Retrieve a single book by ID
    # Endpoint: GET /books/<int:pk>/
    # View: BookDetailView
    # Permission: Public (no authentication required)
    # Returns: JSON object of the specified book
    # Example: GET /books/1/ returns book with ID 1
    path('books/<int:pk>/', BookDetailView.as_view(), name='book-detail'),
    
    # Create a new book
    # Endpoint: POST /books/create/
    # View: BookCreateView
    # Permission: Authenticated users only
    # Request Body: {"title": "Book Title", "publication_year": 2020, "author": 1}
    # Returns: JSON object of the created book with 201 status
    path('books/create/', BookCreateView.as_view(), name='book-create'),
    
    # Update an existing book (full or partial)
    # Endpoint: PUT /books/update/ or PATCH /books/update/ or PUT /books/<int:pk>/update/ or PATCH /books/<int:pk>/update/
    # View: BookUpdateView
    # Permission: Authenticated users only
    # Request Body (PUT): All fields required
    # Request Body (PATCH): Only fields to update
    # Returns: JSON object of the updated book
    # Example: PUT /books/1/update/ updates book with ID 1
    path('books/update/', BookUpdateView.as_view(), name='book-update-base'),
    path('books/<int:pk>/update/', BookUpdateView.as_view(), name='book-update'),
    
    # Delete a book
    # Endpoint: DELETE /books/delete/ or DELETE /books/<int:pk>/delete/
    # View: BookDeleteView
    # Permission: Authenticated users only
    # Returns: 204 No Content on successful deletion
    # Example: DELETE /books/1/delete/ deletes book with ID 1
    path('books/delete/', BookDeleteView.as_view(), name='book-delete-base'),
    path('books/<int:pk>/delete/', BookDeleteView.as_view(), name='book-delete'),
]


# ==================== URL PATTERN NOTES ====================
#
# URL Structure:
# - /books/ - List endpoint (collection resource)
# - /books/<pk>/ - Detail endpoint (individual resource)
# - /books/create/ - Creation endpoint
# - /books/<pk>/update/ - Update endpoint
# - /books/<pk>/delete/ - Delete endpoint
#
# Path Parameters:
# - <int:pk> - Primary key (ID) of the book, must be an integer
#
# Named URLs:
# Each URL pattern has a name for easy reference in:
# - Reverse URL lookups
# - Template rendering
# - API browsing
#
# URL Resolution Order:
# Django checks URLs from top to bottom, so more specific patterns
# should come before more general ones. In this configuration:
# 1. /books/create/ (specific)
# 2. /books/<int:pk>/ (with parameter)
# 3. /books/<int:pk>/update/ (specific with parameter)
# 4. /books/<int:pk>/delete/ (specific with parameter)
# 5. /books/ (general list)
#
# Testing URLs:
# To test these endpoints, prepend the API prefix (usually /api/)
# For example, if main urls.py includes api.urls at 'api/':
# - GET http://localhost:8000/api/books/
# - GET http://localhost:8000/api/books/1/
# - POST http://localhost:8000/api/books/create/
# - PUT http://localhost:8000/api/books/1/update/
# - PATCH http://localhost:8000/api/books/1/update/
# - DELETE http://localhost:8000/api/books/1/delete/
