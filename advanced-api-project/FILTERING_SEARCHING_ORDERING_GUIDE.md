# Filtering, Searching, and Ordering Implementation Guide

## Overview

This document explains how filtering, searching, and ordering have been implemented in the Book API using Django REST Framework. These features allow API consumers to refine, search, and sort book data according to their needs.

---

## Table of Contents

1. [Architecture Overview](#architecture-overview)
2. [Filtering Implementation](#filtering-implementation)
3. [Search Implementation](#search-implementation)
4. [Ordering Implementation](#ordering-implementation)
5. [Configuration Details](#configuration-details)
6. [API Query Parameters](#api-query-parameters)
7. [Usage Examples](#usage-examples)
8. [Testing Guide](#testing-guide)

---

## Architecture Overview

The filtering, searching, and ordering functionality is built using Django REST Framework's filter backends:

- **DjangoFilterBackend**: Provides field-based filtering
- **SearchFilter**: Enables text-based search across specified fields
- **OrderingFilter**: Allows sorting results by specified fields

These backends are configured in:
1. **settings.py**: Global REST framework configuration
2. **api/views.py**: BookListView configuration

---

## Filtering Implementation

### What is Filtering?

Filtering allows API users to narrow down the results to only books that match specific criteria. Filtering uses exact matches or specific conditions on fields.

### Configuration in BookListView

```python
filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
filterset_fields = ['title', 'author', 'publication_year']
```

### Filterable Fields

| Field | Type | Description |
|-------|------|-------------|
| **title** | String | Filter books by exact title match |
| **author** | Integer (FK) | Filter books by author ID |
| **publication_year** | Integer | Filter books by publication year |

### How Filtering Works

When a query parameter matches a filterable field name, DjangoFilterBackend automatically:
1. Extracts the filter value from the query parameter
2. Constructs a Django ORM filter query
3. Applies the filter to the queryset
4. Returns only matching results

### Example Filter Query

```
GET /api/books/?publication_year=2020
```

This generates the Django ORM query:
```python
Book.objects.filter(publication_year=2020)
```

---

## Search Implementation

### What is Search?

Search functionality allows users to perform full-text or partial text searches across multiple fields. Unlike filtering (exact matches), search supports partial matches and is case-insensitive by default.

### Configuration in BookListView

```python
filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
search_fields = ['title', 'author__name']
```

### Searchable Fields

| Field | Description |
|-------|-------------|
| **title** | Book title (direct field) |
| **author__name** | Author name (related field via ForeignKey) |

### Search Field Syntax

- `title`: Direct field on the Book model
- `author__name`: Related field accessed via the author ForeignKey relationship

### How Search Works

When a `search` query parameter is provided:
1. SearchFilter extracts the search term
2. Constructs queries that search across all specified search_fields
3. Uses case-insensitive partial matching (contains)
4. Returns all books where ANY search field contains the search term

### Example Search Query

```
GET /api/books/?search=django
```

This generates Django ORM queries equivalent to:
```python
Book.objects.filter(
    Q(title__icontains='django') |
    Q(author__name__icontains='django')
)
```

---

## Ordering Implementation

### What is Ordering?

Ordering allows users to sort the results by one or more fields in ascending or descending order. This helps organize results in a meaningful way.

### Configuration in BookListView

```python
filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
ordering_fields = ['title', 'publication_year']
ordering = ['title']  # Default ordering
```

### Orderable Fields

| Field | Description |
|-------|-------------|
| **title** | Sort alphabetically by book title |
| **publication_year** | Sort by year (oldest/newest first) |

### Sort Direction

- **Ascending** (default): Use field name directly → `?ordering=title`
- **Descending**: Prefix field name with hyphen → `?ordering=-title`

### Default Ordering

By default, books are ordered by `title` in ascending order. This is specified by:
```python
ordering = ['title']
```

### How Ordering Works

When an `ordering` query parameter is provided:
1. OrderingFilter extracts the ordering field
2. Validates that the field is in allowed orderable fields
3. Applies the ordering to the queryset
4. Returns results sorted accordingly

### Example Ordering Query

```
GET /api/books/?ordering=-publication_year
```

This generates Django ORM query:
```python
Book.objects.order_by('-publication_year')
```

---

## Configuration Details

### settings.py Configuration

```python
REST_FRAMEWORK = {
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter',
    ],
}
```

This global configuration makes these filter backends available to all DRF views (if not overridden locally).

### BookListView Configuration

```python
class BookListView(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = []
    
    # Configure filter backends (local override)
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    
    # Filtering
    filterset_fields = ['title', 'author', 'publication_year']
    
    # Searching
    search_fields = ['title', 'author__name']
    
    # Ordering
    ordering_fields = ['title', 'publication_year']
    ordering = ['title']
```

---

## API Query Parameters

### Format

Query parameters are appended to the endpoint URL using the `?` separator and `&` for multiple parameters:

```
GET /api/books/?param1=value1&param2=value2
```

### Filtering Parameters

| Parameter | Example | Description |
|-----------|---------|-------------|
| **title** | `?title=Django` | Filter by exact title |
| **author** | `?author=1` | Filter by author ID |
| **publication_year** | `?publication_year=2020` | Filter by year |

### Search Parameter

| Parameter | Example | Description |
|-----------|---------|-------------|
| **search** | `?search=django` | Search in title and author__name fields |

### Ordering Parameter

| Parameter | Example | Description |
|-----------|---------|-------------|
| **ordering** | `?ordering=title` | Order by title (ascending) |
| **ordering** | `?ordering=-publication_year` | Order by year (descending) |

### Combined Parameters

You can combine filtering, searching, and ordering in a single request:

```
?title=Django&author=1&search=advanced&ordering=-publication_year
```

---

## Usage Examples

### Example 1: Filter by Author

**Request:**
```bash
curl -X GET "http://localhost:8000/api/books/?author=1"
```

**URL:**
```
http://localhost:8000/api/books/?author=1
```

**Description:** Returns all books written by author with ID 1.

**Response:**
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
    "author": 1
  }
]
```

---

### Example 2: Filter by Publication Year

**Request:**
```bash
curl -X GET "http://localhost:8000/api/books/?publication_year=2020"
```

**URL:**
```
http://localhost:8000/api/books/?publication_year=2020
```

**Description:** Returns all books published in 2020.

**Response:**
```json
[
  {
    "id": 1,
    "title": "Django for Beginners",
    "publication_year": 2020,
    "author": 1
  }
]
```

---

### Example 3: Search by Keyword

**Request:**
```bash
curl -X GET "http://localhost:8000/api/books/?search=django"
```

**URL:**
```
http://localhost:8000/api/books/?search=django
```

**Description:** Searches for "django" in book titles and author names. Matches:
- Books with "django" in the title (case-insensitive)
- Books by authors with "django" in their name

**Response:**
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
    "author": 1
  }
]
```

---

### Example 4: Order by Title (Ascending)

**Request:**
```bash
curl -X GET "http://localhost:8000/api/books/?ordering=title"
```

**URL:**
```
http://localhost:8000/api/books/?ordering=title
```

**Description:** Returns all books ordered alphabetically by title.

**Response:**
```json
[
  {
    "id": 2,
    "title": "Advanced Django",
    "publication_year": 2021,
    "author": 1
  },
  {
    "id": 1,
    "title": "Django for Beginners",
    "publication_year": 2020,
    "author": 1
  }
]
```

---

### Example 5: Order by Year (Descending - Newest First)

**Request:**
```bash
curl -X GET "http://localhost:8000/api/books/?ordering=-publication_year"
```

**URL:**
```
http://localhost:8000/api/books/?ordering=-publication_year
```

**Description:** Returns all books ordered by publication year, newest first.

**Response:**
```json
[
  {
    "id": 2,
    "title": "Advanced Django",
    "publication_year": 2021,
    "author": 1
  },
  {
    "id": 1,
    "title": "Django for Beginners",
    "publication_year": 2020,
    "author": 1
  }
]
```

---

### Example 6: Combine Filtering and Ordering

**Request:**
```bash
curl -X GET "http://localhost:8000/api/books/?author=1&ordering=-publication_year"
```

**URL:**
```
http://localhost:8000/api/books/?author=1&ordering=-publication_year
```

**Description:** Returns all books by author 1, ordered by publication year (newest first).

**Response:**
```json
[
  {
    "id": 2,
    "title": "Advanced Django",
    "publication_year": 2021,
    "author": 1
  },
  {
    "id": 1,
    "title": "Django for Beginners",
    "publication_year": 2020,
    "author": 1
  }
]
```

---

### Example 7: Combine Search and Ordering

**Request:**
```bash
curl -X GET "http://localhost:8000/api/books/?search=django&ordering=title"
```

**URL:**
```
http://localhost:8000/api/books/?search=django&ordering=title
```

**Description:** Searches for "django" in titles/authors, then orders results alphabetically by title.

**Response:**
```json
[
  {
    "id": 2,
    "title": "Advanced Django",
    "publication_year": 2021,
    "author": 1
  },
  {
    "id": 1,
    "title": "Django for Beginners",
    "publication_year": 2020,
    "author": 1
  }
]
```

---

### Example 8: Multiple Filters

**Request:**
```bash
curl -X GET "http://localhost:8000/api/books/?author=1&publication_year=2020"
```

**URL:**
```
http://localhost:8000/api/books/?author=1&publication_year=2020
```

**Description:** Returns books by author 1 that were published in 2020.

**Response:**
```json
[
  {
    "id": 1,
    "title": "Django for Beginners",
    "publication_year": 2020,
    "author": 1
  }
]
```

---

### Example 9: Filter by Title and Order by Year

**Request:**
```bash
curl -X GET "http://localhost:8000/api/books/?title=Django&ordering=-publication_year"
```

**URL:**
```
http://localhost:8000/api/books/?title=Django&ordering=-publication_year
```

**Description:** Returns books with "Django" in the title, ordered by year (newest first).

**Response:**
```json
[
  {
    "id": 2,
    "title": "Advanced Django",
    "publication_year": 2021,
    "author": 1
  },
  {
    "id": 1,
    "title": "Django for Beginners",
    "publication_year": 2020,
    "author": 1
  }
]
```

---

### Example 10: Complex Query (All Features Combined)

**Request:**
```bash
curl -X GET "http://localhost:8000/api/books/?author=1&search=advanced&ordering=-publication_year"
```

**URL:**
```
http://localhost:8000/api/books/?author=1&search=advanced&ordering=-publication_year
```

**Description:** 
- Filter books by author 1
- Search for "advanced" in title/author name
- Order results by year (newest first)

**Response:**
```json
[
  {
    "id": 2,
    "title": "Advanced Django",
    "publication_year": 2021,
    "author": 1
  }
]
```

---

## Testing Guide

### Prerequisites

1. Django development server running: `python manage.py runserver`
2. Database with sample books: Create via Django admin or fixtures
3. API testing tool (cURL, Postman, or Python requests)

### Manual Testing Steps

#### Test 1: Verify Filtering Works

1. **List all books:**
   ```bash
   curl -X GET "http://localhost:8000/api/books/"
   ```
   Note the book IDs and authors.

2. **Filter by author:**
   ```bash
   curl -X GET "http://localhost:8000/api/books/?author=1"
   ```
   Verify only books by author 1 appear.

3. **Filter by year:**
   ```bash
   curl -X GET "http://localhost:8000/api/books/?publication_year=2020"
   ```
   Verify only 2020 books appear.

#### Test 2: Verify Search Works

1. **Search for partial match:**
   ```bash
   curl -X GET "http://localhost:8000/api/books/?search=django"
   ```
   Verify results contain "django" in title or author name.

2. **Search case-insensitivity:**
   ```bash
   curl -X GET "http://localhost:8000/api/books/?search=DJANGO"
   ```
   Should return same results as lowercase search.

3. **Search with spaces:**
   ```bash
   curl -X GET "http://localhost:8000/api/books/?search=for%20beginners"
   ```
   (Note: URL encode spaces as %20)

#### Test 3: Verify Ordering Works

1. **Order by title ascending:**
   ```bash
   curl -X GET "http://localhost:8000/api/books/?ordering=title"
   ```
   Verify books appear in alphabetical order.

2. **Order by year descending:**
   ```bash
   curl -X GET "http://localhost:8000/api/books/?ordering=-publication_year"
   ```
   Verify books appear with newest years first.

3. **Default ordering:**
   ```bash
   curl -X GET "http://localhost:8000/api/books/"
   ```
   Verify default ordering is by title (should match `?ordering=title`).

#### Test 4: Combined Operations

1. **Filter and order:**
   ```bash
   curl -X GET "http://localhost:8000/api/books/?author=1&ordering=title"
   ```
   Verify results are filtered AND ordered correctly.

2. **Search and order:**
   ```bash
   curl -X GET "http://localhost:8000/api/books/?search=django&ordering=-publication_year"
   ```
   Verify search results are ordered correctly.

3. **Complex query:**
   ```bash
   curl -X GET "http://localhost:8000/api/books/?author=1&publication_year=2020&ordering=title"
   ```
   Verify all conditions are applied.

### Testing with Postman

1. Create new request → GET
2. URL: `http://localhost:8000/api/books/`
3. Go to "Params" tab
4. Add query parameters:
   - Key: `author`, Value: `1`
   - Key: `ordering`, Value: `-publication_year`
5. Click "Send"
6. Verify response matches expectations

### Testing with Python

```python
import requests

# Test filtering
response = requests.get('http://localhost:8000/api/books/', {
    'author': 1,
    'publication_year': 2020
})
print(response.json())

# Test search
response = requests.get('http://localhost:8000/api/books/', {
    'search': 'django'
})
print(response.json())

# Test ordering
response = requests.get('http://localhost:8000/api/books/', {
    'ordering': '-publication_year'
})
print(response.json())

# Test combined
response = requests.get('http://localhost:8000/api/books/', {
    'author': 1,
    'search': 'django',
    'ordering': '-publication_year'
})
print(response.json())
```

### Edge Cases to Test

1. **Non-existent filter value:**
   ```bash
   curl -X GET "http://localhost:8000/api/books/?author=999"
   ```
   Should return empty array `[]`

2. **Invalid ordering field:**
   ```bash
   curl -X GET "http://localhost:8000/api/books/?ordering=invalid_field"
   ```
   Should return all books (ordering ignored or error).

3. **Empty search:**
   ```bash
   curl -X GET "http://localhost:8000/api/books/?search="
   ```
   Should return all books.

4. **Multiple filter values:**
   ```bash
   curl -X GET "http://localhost:8000/api/books/?author=1&author=2"
   ```
   Behavior depends on Django filter implementation.

---

## Technical Implementation Details

### Django ORM Equivalents

The DRF filter backends translate to the following Django ORM queries:

**Filtering:**
```python
# ?publication_year=2020
Book.objects.filter(publication_year=2020)
```

**Searching:**
```python
# ?search=django
from django.db.models import Q
Book.objects.filter(
    Q(title__icontains='django') |
    Q(author__name__icontains='django')
)
```

**Ordering:**
```python
# ?ordering=-publication_year
Book.objects.order_by('-publication_year')
```

**Combined:**
```python
# ?author=1&search=django&ordering=title
Book.objects.filter(author=1).filter(
    Q(title__icontains='django') |
    Q(author__name__icontains='django')
).order_by('title')
```

### Performance Considerations

1. **Database Indexes**: Consider adding database indexes to frequently filtered/searched fields for better performance:
   ```python
   class Book(models.Model):
       title = models.CharField(max_length=200, db_index=True)
       publication_year = models.IntegerField(db_index=True)
       author = models.ForeignKey(Author, on_delete=models.CASCADE, db_index=True)
   ```

2. **Related Field Searches**: Searching on `author__name` performs a JOIN operation. This is efficient but can be optimized with `select_related()` for larger datasets:
   ```python
   queryset = Book.objects.select_related('author').all()
   ```

3. **Pagination**: Consider implementing pagination to limit result sets when many books match the query criteria.

---

## Summary

The Book API now provides powerful query capabilities:

✅ **Filtering**: Narrow results by specific field values  
✅ **Searching**: Full-text search across multiple fields  
✅ **Ordering**: Sort results by specified fields  
✅ **Combination**: Use any combination of the above features

These features are implemented using Django REST Framework's battle-tested filter backends, providing:
- Standard query parameter syntax
- Efficient database queries
- Flexible and extensible architecture

For more information, see:
- [Django REST Framework Filtering](https://www.django-rest-framework.org/api-guide/filtering/)
- [Django-Filter Documentation](https://django-filter.readthedocs.io/)
