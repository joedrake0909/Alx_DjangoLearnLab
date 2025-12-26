from rest_framework import generics, filters
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from django_filters import rest_framework
from .models import Book
from .serializers import BookSerializer


# ==================== GENERIC VIEWS FOR BOOK MODEL ====================
# This module implements CRUD operations for the Book model using Django REST Framework's
# generic views. These views provide built-in functionality for handling common API patterns
# while allowing customization for specific requirements.


# ListView - Retrieve All Books
# This view handles GET requests to retrieve a list of all books in the database.
# It provides read-only access to all users (authenticated and unauthenticated).
class BookListView(generics.ListAPIView):
    """
    API endpoint for retrieving a list of all books.
    
    - Method: GET
    - URL: /books/
    - Permission: Read-only access for all users
    - Returns: JSON array of all book objects with their details
    
    The view automatically handles:
    - Queryset filtering
    - Pagination (if configured)
    - Serialization of Book instances
    - Filtering by title, author, and publication_year
    - Searching on title and author name
    - Ordering by title and publication_year
    
    Query Parameters for Filtering:
    - ?title=<title> - Filter by book title (exact match)
    - ?author=<author_id> - Filter by author ID
    - ?publication_year=<year> - Filter by publication year
    
    Query Parameters for Searching:
    - ?search=<query> - Search in title and author name fields
    
    Query Parameters for Ordering:
    - ?ordering=title - Order by title (ascending)
    - ?ordering=-title - Order by title (descending)
    - ?ordering=publication_year - Order by publication year (ascending)
    - ?ordering=-publication_year - Order by publication year (descending)
    
    Example requests:
    - GET /books/?title=Django - Filter books with "Django" in title
    - GET /books/?author=1 - Filter books by author with ID 1
    - GET /books/?publication_year=2020 - Filter books published in 2020
    - GET /books/?search=django - Search for books with "django" in title or author
    - GET /books/?ordering=title - Order books by title alphabetically
    - GET /books/?ordering=-publication_year - Order books by year (newest first)
    - GET /books/?title=Django&ordering=-publication_year - Combine filtering and ordering
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = []  # No authentication required for listing books
    
    # Configure filter backends for filtering, searching, and ordering
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    
    # Filtering configuration
    # Specify which fields can be filtered using exact matches
    filterset_fields = ['title', 'author', 'publication_year']
    
    # Search configuration
    # Specify which fields are searchable with text search queries
    # The search query will look for matches in these fields
    search_fields = ['title', 'author__name']  # author__name allows searching by author name
    
    # Ordering configuration
    # Specify which fields can be used for ordering results
    # Users can prefix field names with '-' for descending order
    ordering_fields = ['title', 'publication_year']
    ordering = ['title']  # Default ordering by title (ascending)


# DetailView - Retrieve a Single Book by ID
# This view handles GET requests to retrieve details of a specific book.
# It provides read-only access to all users.
class BookDetailView(generics.RetrieveAPIView):
    """
    API endpoint for retrieving a single book by its ID.
    
    - Method: GET
    - URL: /books/<int:pk>/
    - Permission: Read-only access for all users
    - Returns: JSON object containing the book's details
    
    The view automatically handles:
    - Object lookup by primary key (pk)
    - 404 responses for non-existent books
    - Serialization of the Book instance
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = []  # No authentication required for viewing book details


# CreateView - Add a New Book
# This view handles POST requests to create a new book in the database.
# Only authenticated users can create books.
class BookCreateView(generics.CreateAPIView):
    """
    API endpoint for creating a new book.
    
    - Method: POST
    - URL: /books/create/
    - Permission: Authenticated users only
    - Request Body: JSON object with book data (title, publication_year, author)
    - Returns: JSON object of the created book with 201 status
    
    Customization:
    - Validates publication_year (must be between 1450 and current year)
    - Requires valid author ID
    - Returns validation errors if data is invalid
    
    The view automatically handles:
    - Data deserialization
    - Validation using BookSerializer
    - Database insertion
    - Response generation
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]  # Only authenticated users can create
    
    def perform_create(self, serializer):
        """
        Custom method to handle book creation.
        This method is called after validation but before saving to the database.
        
        Args:
            serializer: The validated BookSerializer instance
        """
        # Save the book instance
        # Additional logic can be added here (e.g., logging, notifications)
        serializer.save()


# UpdateView - Modify an Existing Book
# This view handles PUT and PATCH requests to update a book's information.
# Only authenticated users can update books.
class BookUpdateView(generics.UpdateAPIView):
    """
    API endpoint for updating an existing book.
    
    - Methods: PUT (full update), PATCH (partial update)
    - URL: /books/<int:pk>/update/
    - Permission: Authenticated users only
    - Request Body: JSON object with updated book data
    - Returns: JSON object of the updated book
    
    Customization:
    - PUT requires all fields (title, publication_year, author)
    - PATCH allows updating individual fields
    - Validates all data using BookSerializer
    
    The view automatically handles:
    - Object lookup by primary key
    - Data validation
    - Database update
    - 404 responses for non-existent books
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]  # Only authenticated users can update
    
    def perform_update(self, serializer):
        """
        Custom method to handle book updates.
        This method is called after validation but before saving to the database.
        
        Args:
            serializer: The validated BookSerializer instance
        """
        # Save the updated book instance
        # Additional logic can be added here (e.g., audit logging, version tracking)
        serializer.save()


# DeleteView - Remove a Book
# This view handles DELETE requests to remove a book from the database.
# Only authenticated users can delete books.
class BookDeleteView(generics.DestroyAPIView):
    """
    API endpoint for deleting a book.
    
    - Method: DELETE
    - URL: /books/<int:pk>/delete/
    - Permission: Authenticated users only
    - Returns: 204 No Content on successful deletion
    
    The view automatically handles:
    - Object lookup by primary key
    - Database deletion
    - 404 responses for non-existent books
    - Cascade deletion of related objects (if configured in model)
    
    Note: Due to the CASCADE delete rule in the Book model's ForeignKey,
    deleting an author will automatically delete all their books.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]  # Only authenticated users can delete


# ==================== VIEW CONFIGURATION NOTES ====================
#
# Permission Strategy:
# - ListView and DetailView: No authentication required (public read access)
# - CreateView, UpdateView, DeleteView: IsAuthenticatedOrReadOnly permission
#   This means:
#   * Authenticated users can perform write operations (POST, PUT, PATCH, DELETE)
#   * Unauthenticated users get read-only access (but these views don't handle GET)
#
# Generic View Benefits:
# 1. Built-in HTTP method handling
# 2. Automatic serialization/deserialization
# 3. Standard error responses
# 4. Queryset and permission management
# 5. Reduces boilerplate code
#
# Customization Hooks Used:
# - perform_create(): Called before saving a new object
# - perform_update(): Called before updating an existing object
# These hooks allow adding custom logic without overriding the entire view method
#
# Testing Endpoints:
# - GET /books/ - List all books (no auth required)
# - GET /books/1/ - Get book with ID 1 (no auth required)
# - POST /books/create/ - Create new book (auth required)
# - PUT /books/1/update/ - Full update of book 1 (auth required)
# - PATCH /books/1/update/ - Partial update of book 1 (auth required)
# - DELETE /books/1/delete/ - Delete book 1 (auth required)
