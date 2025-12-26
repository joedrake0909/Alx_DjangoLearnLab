# API Views Documentation

## Overview

This document provides comprehensive information about the Django REST Framework generic views implemented for the Book API. It details the configuration, behavior, permissions, and usage of each endpoint.

---

## Table of Contents

1. [View Architecture](#view-architecture)
2. [Endpoint Reference](#endpoint-reference)
3. [Permission System](#permission-system)
4. [Generic Views Configuration](#generic-views-configuration)
5. [Custom Hooks & Customizations](#custom-hooks--customizations)
6. [Data Validation](#data-validation)
7. [Testing Guide](#testing-guide)
8. [Error Handling](#error-handling)

---

## View Architecture

The API implements five generic views using Django REST Framework's built-in generic view classes. These views handle CRUD (Create, Read, Update, Delete) operations on the Book model with minimal boilerplate code.

### View Hierarchy

```
BaseAPIView (DRF)
├── ListAPIView (BookListView)
├── RetrieveAPIView (BookDetailView)
├── CreateAPIView (BookCreateView)
├── UpdateAPIView (BookUpdateView)
└── DestroyAPIView (BookDeleteView)
```

Each generic view comes with:
- Automatic HTTP method handling
- Built-in serialization/deserialization
- Standard error responses
- Queryset and permission management

---

## Endpoint Reference

### 1. List All Books

**View Class:** `BookListView` (ListAPIView)

| Property | Value |
|----------|-------|
| **HTTP Method** | GET |
| **URL Pattern** | `/api/books/` |
| **Permission** | Public (no authentication required) |
| **Response Code** | 200 OK |

**Description:**
Retrieves a paginated or complete list of all books in the database. Returns JSON array of book objects.

**cURL Example:**
```bash
curl -X GET http://localhost:8000/api/books/
```

**Response (200 OK):**
```json
[
  {
    "id": 1,
    "title": "Django for Beginners",
    "publication_year": 2020,
    "author": 1
  },
  {
    "id": 2,
    "title": "Advanced Django",
    "publication_year": 2021,
    "author": 2
  }
]
```

**Configuration Details:**
- **Queryset:** `Book.objects.all()` - Returns all books in the database
- **Serializer:** `BookSerializer` - Serializes Book instances to JSON
- **Permission Classes:** Empty list `[]` - Allows public access

---

### 2. Retrieve Single Book

**View Class:** `BookDetailView` (RetrieveAPIView)

| Property | Value |
|----------|-------|
| **HTTP Method** | GET |
| **URL Pattern** | `/api/books/<int:pk>/` |
| **Permission** | Public (no authentication required) |
| **Response Code** | 200 OK (success) / 404 Not Found (if book doesn't exist) |

**Description:**
Retrieves detailed information about a specific book identified by its primary key (ID).

**URL Parameters:**
- `pk` (int): Primary key/ID of the book (required)

**cURL Example:**
```bash
curl -X GET http://localhost:8000/api/books/1/
```

**Response (200 OK):**
```json
{
  "id": 1,
  "title": "Django for Beginners",
  "publication_year": 2020,
  "author": 1
}
```

**Response (404 Not Found):**
```json
{
  "detail": "Not found."
}
```

**Configuration Details:**
- **Queryset:** `Book.objects.all()` - Searches all books for the specified pk
- **Serializer:** `BookSerializer` - Serializes the Book instance to JSON
- **Permission Classes:** Empty list `[]` - Allows public access
- **Lookup Field:** Default `pk` (primary key)

---

### 3. Create New Book

**View Class:** `BookCreateView` (CreateAPIView)

| Property | Value |
|----------|-------|
| **HTTP Method** | POST |
| **URL Pattern** | `/api/books/create/` |
| **Permission** | `IsAuthenticatedOrReadOnly` (Authenticated users only) |
| **Response Code** | 201 Created / 400 Bad Request (validation error) / 403 Forbidden (not authenticated) |

**Description:**
Creates a new book in the database. Requires authentication and valid data.

**Request Body (JSON):**
```json
{
  "title": "New Book Title",
  "publication_year": 2024,
  "author": 1
}
```

**Required Fields:**
- `title` (string, max 200 chars): The book's title
- `publication_year` (integer): Year of publication (1450 - current year)
- `author` (integer): ID of an existing Author

**cURL Example:**
```bash
curl -X POST http://localhost:8000/api/books/create/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{
    "title": "New Book Title",
    "publication_year": 2024,
    "author": 1
  }'
```

**Response (201 Created):**
```json
{
  "id": 3,
  "title": "New Book Title",
  "publication_year": 2024,
  "author": 1
}
```

**Response (400 Bad Request) - Invalid Year:**
```json
{
  "publication_year": [
    "Publication year cannot be in the future. Current year is 2025."
  ]
}
```

**Response (403 Forbidden) - Unauthenticated:**
```json
{
  "detail": "Authentication credentials were not provided."
}
```

**Configuration Details:**
- **Queryset:** `Book.objects.all()` - Used for internal lookup
- **Serializer:** `BookSerializer` - Validates and serializes incoming data
- **Permission Classes:** `[IsAuthenticatedOrReadOnly]` - Only authenticated users can POST
- **Custom Hook:** `perform_create()` - Called before saving to database
  - Can be extended to add logging, notifications, or other logic

---

### 4. Update Existing Book

**View Class:** `BookUpdateView` (UpdateAPIView)

| Property | Value |
|----------|-------|
| **HTTP Method** | PUT (full update), PATCH (partial update) |
| **URL Pattern** | `/api/books/<int:pk>/update/` |
| **Permission** | `IsAuthenticatedOrReadOnly` (Authenticated users only) |
| **Response Code** | 200 OK / 400 Bad Request / 404 Not Found / 403 Forbidden |

**Description:**
Updates an existing book's information. Supports both full (PUT) and partial (PATCH) updates.

**URL Parameters:**
- `pk` (int): Primary key/ID of the book to update (required)

**Request Body (JSON):**

**PUT Example (Full Update - All fields required):**
```json
{
  "title": "Updated Book Title",
  "publication_year": 2023,
  "author": 2
}
```

**PATCH Example (Partial Update - Only changed fields):**
```json
{
  "title": "Updated Title Only"
}
```

**cURL Examples:**

Full Update (PUT):
```bash
curl -X PUT http://localhost:8000/api/books/1/update/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{
    "title": "Updated Book Title",
    "publication_year": 2023,
    "author": 2
  }'
```

Partial Update (PATCH):
```bash
curl -X PATCH http://localhost:8000/api/books/1/update/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{
    "title": "Updated Title Only"
  }'
```

**Response (200 OK):**
```json
{
  "id": 1,
  "title": "Updated Book Title",
  "publication_year": 2023,
  "author": 2
}
```

**Response (404 Not Found):**
```json
{
  "detail": "Not found."
}
```

**Configuration Details:**
- **Queryset:** `Book.objects.all()` - Finds book by pk for updating
- **Serializer:** `BookSerializer` - Validates and serializes updated data
- **Permission Classes:** `[IsAuthenticatedOrReadOnly]` - Only authenticated users can PUT/PATCH
- **Custom Hook:** `perform_update()` - Called before saving changes
  - Can be extended to add audit logging, version tracking, or notifications
- **Difference between PUT and PATCH:**
  - **PUT:** Requires all fields; missing fields treated as null/invalid
  - **PATCH:** Only processes provided fields; others remain unchanged

---

### 5. Delete Book

**View Class:** `BookDeleteView` (DestroyAPIView)

| Property | Value |
|----------|-------|
| **HTTP Method** | DELETE |
| **URL Pattern** | `/api/books/<int:pk>/delete/` |
| **Permission** | `IsAuthenticatedOrReadOnly` (Authenticated users only) |
| **Response Code** | 204 No Content / 404 Not Found / 403 Forbidden |

**Description:**
Permanently deletes a book from the database. Requires authentication.

**URL Parameters:**
- `pk` (int): Primary key/ID of the book to delete (required)

**cURL Example:**
```bash
curl -X DELETE http://localhost:8000/api/books/1/delete/ \
  -H "Authorization: Bearer YOUR_TOKEN"
```

**Response (204 No Content):**
```
(Empty body - indicates successful deletion)
```

**Response (404 Not Found):**
```json
{
  "detail": "Not found."
}
```

**Response (403 Forbidden):**
```json
{
  "detail": "Authentication credentials were not provided."
}
```

**Configuration Details:**
- **Queryset:** `Book.objects.all()` - Finds book by pk for deletion
- **Serializer:** `BookSerializer` - Not actively used but required by DRF
- **Permission Classes:** `[IsAuthenticatedOrReadOnly]` - Only authenticated users can DELETE
- **Cascade Behavior:** When a book is deleted, if an author is deleted, all their books cascade delete (due to `on_delete=models.CASCADE` in the Book model)

---

## Permission System

### Permission Class: `IsAuthenticatedOrReadOnly`

This permission class is used on write operations (POST, PUT, PATCH, DELETE) and allows:

| User Type | GET | POST | PUT | PATCH | DELETE |
|-----------|-----|------|-----|-------|--------|
| **Unauthenticated** | ✅ | ❌ | ❌ | ❌ | ❌ |
| **Authenticated** | ✅ | ✅ | ✅ | ✅ | ✅ |

### Authentication Methods

To authenticate and access protected endpoints, include authentication credentials in the request:

**Token Authentication (Bearer Token):**
```bash
Authorization: Bearer YOUR_TOKEN
```

**Session Authentication (from browser):**
- Session cookie automatically sent by browser
- Useful for DRF's browsable API interface

### Getting an Authentication Token

If using token authentication, obtain a token from your authentication endpoint (typically `/api-token-auth/`):

```bash
curl -X POST http://localhost:8000/api-token-auth/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "your_username",
    "password": "your_password"
  }'
```

Response:
```json
{
  "token": "9944b09199c62bcf9418ad846dd0e4bbea"
}
```

Use this token in subsequent requests:
```bash
curl -H "Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbea" \
  http://localhost:8000/api/books/
```

---

## Generic Views Configuration

### BookListView Configuration

```python
class BookListView(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = []  # Public access
```

**What it provides:**
- Automatic GET request handling
- Queryset filtering and pagination
- Response serialization
- Standard error handling

---

### BookDetailView Configuration

```python
class BookDetailView(generics.RetrieveAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = []  # Public access
```

**What it provides:**
- Automatic GET request handling for single objects
- Object lookup by primary key (pk)
- 404 handling for non-existent objects
- Response serialization

---

### BookCreateView Configuration

```python
class BookCreateView(generics.CreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    def perform_create(self, serializer):
        serializer.save()
```

**What it provides:**
- Automatic POST request handling
- Request data validation
- Object creation
- 201 Created responses
- 400 Bad Request error responses
- 403 Forbidden for unauthenticated users

**Customization Point:**
- `perform_create()` is called after validation, allowing custom logic before save

---

### BookUpdateView Configuration

```python
class BookUpdateView(generics.UpdateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    def perform_update(self, serializer):
        serializer.save()
```

**What it provides:**
- Automatic PUT/PATCH request handling
- Object lookup by pk
- Request data validation
- Object update
- 200 OK responses
- 400 Bad Request error responses
- 404 Not Found handling

**Customization Point:**
- `perform_update()` is called after validation, allowing custom logic before save

---

### BookDeleteView Configuration

```python
class BookDeleteView(generics.DestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
```

**What it provides:**
- Automatic DELETE request handling
- Object lookup by pk
- Object deletion
- 204 No Content responses
- 404 Not Found handling

---

## Custom Hooks & Customizations

### perform_create() Hook

**Location:** `BookCreateView.perform_create()`

**Purpose:** Called after validation but before saving a new object to the database.

**Current Implementation:**
```python
def perform_create(self, serializer):
    serializer.save()
```

**Extension Examples:**

Logging:
```python
def perform_create(self, serializer):
    import logging
    logger = logging.getLogger(__name__)
    logger.info(f"Creating book: {serializer.validated_data.get('title')}")
    serializer.save()
```

Adding metadata:
```python
def perform_create(self, serializer):
    # Add creation timestamp or user info if needed
    serializer.save(created_by=self.request.user)
```

Notifications:
```python
def perform_create(self, serializer):
    book = serializer.save()
    # Send notification to admins
    send_new_book_notification(book)
```

---

### perform_update() Hook

**Location:** `BookUpdateView.perform_update()`

**Purpose:** Called after validation but before updating an existing object in the database.

**Current Implementation:**
```python
def perform_update(self, serializer):
    serializer.save()
```

**Extension Examples:**

Audit Logging:
```python
def perform_update(self, serializer):
    # Track what changed
    old_instance = self.get_object()
    updated_instance = serializer.save()
    log_change(old_instance, updated_instance, self.request.user)
```

Version Control:
```python
def perform_update(self, serializer):
    book = serializer.save()
    # Create a version history record
    BookHistory.objects.create(
        book=book,
        version=book.version + 1,
        changed_by=self.request.user
    )
```

---

## Data Validation

### Publication Year Validation

**Validator:** `BookSerializer.validate_publication_year()`

**Rules:**
1. Publication year cannot be in the future (must be ≤ current year)
2. Publication year must be ≥ 1450 (Gutenberg's printing press era)

**Implementation:**
```python
def validate_publication_year(self, value):
    current_year = datetime.now().year
    
    if value > current_year:
        raise serializers.ValidationError(
            f"Publication year cannot be in the future. Current year is {current_year}."
        )
    
    if value < 1450:
        raise serializers.ValidationError(
            "Publication year seems unrealistic. Please enter a valid year."
        )
    
    return value
```

**Examples:**

Valid:
- `2024` (current year)
- `2000` (past year)
- `1500` (ancient but reasonable)

Invalid:
- `2026` (future)
- `1400` (too ancient)
- `0` (unreasonable)

---

## Testing Guide

### Prerequisites

Before testing, ensure:
1. Django development server is running: `python manage.py runserver`
2. Database is set up: `python manage.py migrate`
3. You have an authenticated user for POST/PUT/PATCH/DELETE operations

### Testing with cURL

**1. List All Books (No Authentication Required)**
```bash
curl -X GET http://localhost:8000/api/books/
```

**2. Get Single Book (No Authentication Required)**
```bash
curl -X GET http://localhost:8000/api/books/1/
```

**3. Create Book (Authentication Required)**
```bash
# First, get a token
curl -X POST http://localhost:8000/api-token-auth/ \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "password"}'

# Use token in create request
curl -X POST http://localhost:8000/api/books/create/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Token YOUR_TOKEN" \
  -d '{
    "title": "Test Book",
    "publication_year": 2023,
    "author": 1
  }'
```

**4. Update Book (Authentication Required)**
```bash
curl -X PATCH http://localhost:8000/api/books/1/update/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Token YOUR_TOKEN" \
  -d '{"title": "Updated Title"}'
```

**5. Delete Book (Authentication Required)**
```bash
curl -X DELETE http://localhost:8000/api/books/1/delete/ \
  -H "Authorization: Token YOUR_TOKEN"
```

### Testing with Postman

1. **Create a new request** → Set method to GET → URL: `http://localhost:8000/api/books/`
2. **For authenticated requests:**
   - Go to "Authorization" tab
   - Select "Bearer Token"
   - Paste your token
   - Send request

### Testing with Python

```python
import requests
from requests.auth import HTTPBasicAuth

# No auth needed for GET
response = requests.get('http://localhost:8000/api/books/')
print(response.json())

# With token auth for POST
headers = {'Authorization': 'Token YOUR_TOKEN'}
data = {
    'title': 'New Book',
    'publication_year': 2023,
    'author': 1
}
response = requests.post(
    'http://localhost:8000/api/books/create/',
    json=data,
    headers=headers
)
print(response.json())
```

### Manual Test Scenarios

**Scenario 1: Create, Read, Update, Delete Flow**
1. GET `/api/books/` → See empty list
2. POST `/api/books/create/` → Create new book
3. GET `/api/books/1/` → Verify creation
4. PATCH `/api/books/1/update/` → Update title
5. GET `/api/books/1/` → Verify update
6. DELETE `/api/books/1/delete/` → Delete book
7. GET `/api/books/1/` → Verify 404

**Scenario 2: Permission Testing**
1. Try POST `/api/books/create/` without token → Should get 403
2. Authenticate with token → Try POST again → Should succeed
3. Try DELETE with invalid token → Should fail

**Scenario 3: Validation Testing**
1. POST book with publication_year: 2030 → Should fail
2. POST book with publication_year: 1400 → Should fail
3. POST book with publication_year: 2023 → Should succeed

---

## Error Handling

### Common Error Responses

**400 Bad Request - Invalid Data**
```json
{
  "title": ["This field may not be blank."],
  "publication_year": ["Publication year cannot be in the future. Current year is 2025."]
}
```

**401 Unauthorized - Invalid Token**
```json
{
  "detail": "Invalid token."
}
```

**403 Forbidden - No Permission**
```json
{
  "detail": "Authentication credentials were not provided."
}
```

**404 Not Found - Book Doesn't Exist**
```json
{
  "detail": "Not found."
}
```

**405 Method Not Allowed**
```json
{
  "detail": "Method \"POST\" not allowed."
}
```

### Error Status Codes Summary

| Status Code | Meaning | Common Causes |
|-------------|---------|---------------|
| 200 OK | Success | GET, PATCH requests |
| 201 Created | Resource created | POST requests |
| 204 No Content | Success, no body | DELETE requests |
| 400 Bad Request | Invalid data | Validation errors, missing fields |
| 401 Unauthorized | Invalid authentication | Wrong/expired token |
| 403 Forbidden | No permission | Unauthenticated user on protected endpoint |
| 404 Not Found | Resource not found | Non-existent book ID |
| 405 Method Not Allowed | Wrong HTTP method | Using GET on create endpoint |
| 500 Server Error | Server error | Internal server issues |

---

## Summary

This API implements a complete CRUD interface for the Book model using Django REST Framework's generic views. The design emphasizes:

- **Simplicity:** Generic views eliminate boilerplate code
- **Security:** Permission classes protect write operations
- **Validation:** Custom validators ensure data integrity
- **Extensibility:** Hooks allow custom logic without overriding entire methods
- **Clarity:** Comprehensive documentation and comments explain behavior

For more information on Django REST Framework, visit: https://www.django-rest-framework.org/
