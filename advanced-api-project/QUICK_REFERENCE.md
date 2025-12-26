# Quick Reference: API Query Parameters

## Filter, Search & Order Quick Guide

### Base URL
```
http://localhost:8000/api/books/
```

---

## Filtering

| Parameter | Values | Example |
|-----------|--------|---------|
| `title` | string | `?title=Django` |
| `author` | integer (ID) | `?author=1` |
| `publication_year` | integer | `?publication_year=2020` |

**Examples:**
```bash
# Get books by specific author
GET /api/books/?author=1

# Get books from specific year
GET /api/books/?publication_year=2020

# Combine filters
GET /api/books/?author=1&publication_year=2020
```

---

## Searching

| Parameter | Searches In | Example |
|-----------|-------------|---------|
| `search` | title, author name | `?search=django` |

**Features:**
- Case-insensitive
- Partial matching (contains)
- Searches multiple fields

**Examples:**
```bash
# Search for keyword
GET /api/books/?search=django

# Search with multiple words
GET /api/books/?search=rest%20framework
```

---

## Ordering

| Parameter | Direction | Example |
|-----------|-----------|---------|
| `ordering` | ascending | `?ordering=title` |
| `ordering` | descending | `?ordering=-title` |

**Available Fields:**
- `title` - Book title
- `publication_year` - Publication year

**Examples:**
```bash
# Order A-Z by title
GET /api/books/?ordering=title

# Order Z-A by title
GET /api/books/?ordering=-title

# Order by year (oldest first)
GET /api/books/?ordering=publication_year

# Order by year (newest first)
GET /api/books/?ordering=-publication_year
```

---

## Combined Examples

### Filter + Order
```bash
GET /api/books/?author=1&ordering=-publication_year
# Books by author 1, newest first
```

### Search + Order
```bash
GET /api/books/?search=django&ordering=title
# Search results ordered alphabetically
```

### Filter + Search + Order
```bash
GET /api/books/?author=1&search=advanced&ordering=-publication_year
# Author 1's books matching "advanced", newest first
```

### Multiple Filters + Order
```bash
GET /api/books/?author=1&publication_year=2020&ordering=title
# Author 1's 2020 books, alphabetically ordered
```

---

## cURL Examples

```bash
# List all books
curl http://localhost:8000/api/books/

# Filter by author
curl "http://localhost:8000/api/books/?author=1"

# Search by keyword
curl "http://localhost:8000/api/books/?search=django"

# Order by title
curl "http://localhost:8000/api/books/?ordering=title"

# Combined: Filter + Search + Order
curl "http://localhost:8000/api/books/?author=1&search=django&ordering=-publication_year"
```

---

## Response Format

All queries return a JSON array of books:

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

No matches return an empty array:
```json
[]
```

---

## Tips & Tricks

1. **URL Encoding**: Special characters need encoding
   - Space → `%20`
   - `?` → `%3F`
   
   ```bash
   # Search with spaces
   curl "http://localhost:8000/api/books/?search=django%20rest"
   ```

2. **Multiple Parameter Syntax**: Use `&` to separate
   ```bash
   ?field1=value1&field2=value2&field3=value3
   ```

3. **Ordering Default**: If no ordering specified, results ordered by title

4. **Case Sensitivity**: 
   - Filtering: Exact match required
   - Searching: Case-insensitive

---

## Error Handling

| Scenario | Response | HTTP Status |
|----------|----------|-------------|
| Invalid parameter | Ignored or 400 | 200 or 400 |
| No matches | Empty array | 200 |
| Server error | Error message | 500 |

---

For detailed information, see `FILTERING_SEARCHING_ORDERING_GUIDE.md`
