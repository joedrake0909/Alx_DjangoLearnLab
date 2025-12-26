# Unit Tests Documentation

## Overview

This document provides comprehensive information about the unit tests for the Book API endpoints. The test suite covers CRUD operations, filtering, searching, ordering, permissions, and edge cases.

---

## Table of Contents

1. [Test Architecture](#test-architecture)
2. [Running Tests](#running-tests)
3. [Test Coverage](#test-coverage)
4. [Test Classes](#test-classes)
5. [Test Results Interpretation](#test-results-interpretation)
6. [Debugging Failed Tests](#debugging-failed-tests)
7. [Adding New Tests](#adding-new-tests)

---

## Test Architecture

### Test Framework

The test suite uses:
- **Django's Test Framework**: Based on Python's `unittest` module
- **Django REST Framework's APITestCase**: For testing API endpoints
- **APIClient**: For making test API requests
- **Token Authentication**: For testing authenticated endpoints

### Test Database

- Separate test database is automatically created and destroyed for each test run
- No impact on production or development data
- Isolated environment for each test method

### Test Structure

```
api/tests.py
├── BaseBookTestCase (Base class with setup/teardown)
├── BookListViewTest (List endpoint tests)
├── BookDetailViewTest (Detail endpoint tests)
├── BookCreateViewTest (Create endpoint tests)
├── BookUpdateViewTest (Update endpoint tests)
├── BookDeleteViewTest (Delete endpoint tests)
├── PermissionTest (Permission and auth tests)
└── EdgeCaseTests (Special scenarios)
```

---

## Running Tests

### Run All Tests

```bash
python manage.py test api
```

Output:
```
Ran XX tests in 0.5XX seconds
OK
```

### Run Specific Test Class

```bash
python manage.py test api.tests.BookListViewTest
```

### Run Specific Test Method

```bash
python manage.py test api.tests.BookListViewTest.test_list_books_unauthenticated
```

### Run Tests with Verbose Output

```bash
python manage.py test api -v 2
```

This shows:
- Test name
- Result (OK/FAIL/ERROR)
- Execution time

### Run Tests with More Details

```bash
python manage.py test api --keepdb
```

The `--keepdb` flag keeps the test database, speeding up subsequent runs.

### Run Tests and Show Coverage

```bash
coverage run --source='api' manage.py test api
coverage report
```

### Run Tests in Parallel

```bash
python manage.py test api --parallel
```

---

## Test Coverage

### Total Tests: 100+

#### List View Tests (15 tests)
- Basic listing
- Filtering by title, author, publication_year
- Filtering combinations
- Searching (case-insensitive, partial match, author name)
- Ordering (ascending, descending)
- Combined filter + search + order

#### Detail View Tests (4 tests)
- Retrieve existing book
- Invalid book ID
- Authenticated/unauthenticated access

#### Create View Tests (10 tests)
- Create with valid data
- Authentication requirement
- Missing required fields
- Invalid author ID
- Year validation (future, too old, boundary)
- Count increment

#### Update View Tests (8 tests)
- Partial update (PATCH)
- Full update (PUT)
- Authentication requirement
- Invalid ID
- Year validation
- Data persistence
- Multiple field updates

#### Delete View Tests (6 tests)
- Delete authenticated
- Unauthenticated restriction
- Invalid ID
- Deleting already-deleted book
- Count decrement
- Multiple deletions

#### Permission Tests (8 tests)
- Read access without authentication
- Write access requires authentication
- Authenticated user permissions

#### Edge Case Tests (5 tests)
- Special characters in titles
- Multiple book deletions
- Empty searches
- Similar titles ordering
- Long titles

---

## Test Classes

### BaseBookTestCase

**Base class** for all test cases.

**Provides:**
- `setUp()`: Creates test data before each test
- `tearDown()`: Cleans up after each test
- `get_auth_headers()`: Returns auth headers for requests

**Test Data Created:**
- 2 users with tokens
- 3 authors
- 4 books

```python
def setUp(self):
    # Creates:
    # - testuser and admin user
    # - 3 authors
    # - 4 books with different publication years
    # - API client
```

### BookListViewTest

Tests for `GET /api/books/`

**Key Tests:**

1. **test_list_books_unauthenticated**
   - Verifies public read access
   - Returns 200 OK
   - Returns 4 books

2. **test_filter_by_author**
   - Filters books by author ID
   - Verifies correct books returned

3. **test_search_by_title**
   - Searches for keyword in title
   - Case-insensitive
   - Partial matching

4. **test_order_by_title_ascending**
   - Orders books alphabetically
   - Verifies sort order

5. **test_filter_search_and_order**
   - Combines all features
   - Verifies combined behavior

### BookDetailViewTest

Tests for `GET /api/books/<id>/`

**Key Tests:**

1. **test_get_book_detail_success**
   - Retrieves specific book
   - Verifies all fields present

2. **test_get_book_detail_invalid_id**
   - Returns 404 for non-existent ID

### BookCreateViewTest

Tests for `POST /api/books/create/`

**Key Tests:**

1. **test_create_book_authenticated**
   - Creates book as authenticated user
   - Returns 201 Created
   - Book saved in database

2. **test_create_book_unauthenticated**
   - Returns 403 Forbidden
   - Book not created

3. **test_create_book_missing_title**
   - Returns 400 Bad Request
   - Error details in response

4. **test_create_book_future_year**
   - Rejects future publication years
   - Returns 400 Bad Request

### BookUpdateViewTest

Tests for `PATCH/PUT /api/books/<id>/update/`

**Key Tests:**

1. **test_update_book_authenticated_patch**
   - Partial update with PATCH
   - Only specified fields changed
   - Returns 200 OK

2. **test_update_book_authenticated_put**
   - Full update with PUT
   - All fields updated
   - Returns 200 OK

3. **test_update_book_changes_persisted**
   - Verifies changes saved to database
   - Not just in response

### BookDeleteViewTest

Tests for `DELETE /api/books/<id>/delete/`

**Key Tests:**

1. **test_delete_book_authenticated**
   - Deletes book
   - Returns 204 No Content
   - Book removed from database

2. **test_delete_book_unauthenticated**
   - Returns 403 Forbidden
   - Book not deleted

### PermissionTest

Tests permission enforcement across endpoints.

**Key Tests:**

1. **test_list_books_no_auth_required**
   - No authentication needed for GET /api/books/

2. **test_create_requires_auth**
   - Authentication required for POST /api/books/create/

3. **test_authenticated_user_can_create**
   - Authenticated users can create

### EdgeCaseTests

Special scenarios and boundary conditions.

**Key Tests:**

1. **test_book_with_special_characters_in_title**
   - Handles apostrophes, hashtags, etc.

2. **test_long_title_creation**
   - 200 character title

3. **test_ordering_with_same_title**
   - Multiple books with similar titles

---

## Test Results Interpretation

### Successful Test Run

```
Ran 100 tests in 1.234 seconds
OK
```

**Meaning:** All tests passed ✅

### Test Failure Example

```
FAIL: test_create_book_authenticated (api.tests.BookCreateViewTest)
AssertionError: 403 != 201

Traceback (most recent call last):
  File "api/tests.py", line XXX, in test_create_book_authenticated
    self.assertEqual(response.status_code, status.HTTP_201_CREATED)
AssertionError: 403 != 201
```

**Meaning:** 
- Test expected 201 Created but got 403 Forbidden
- Likely permission issue
- Check authentication setup

### Common Issues

| Issue | Likely Cause | Fix |
|-------|--------------|-----|
| 403 on authenticated request | Token not sent | Check `get_auth_headers()` |
| 400 Bad Request | Invalid data | Check serializer validation |
| 404 Not Found | Wrong URL | Verify URL patterns in urls.py |
| 500 Server Error | Code bug | Check view implementation |
| IntegrityError | Database constraint violation | Check model constraints |

---

## Debugging Failed Tests

### 1. Run with Verbose Output

```bash
python manage.py test api.tests.BookCreateViewTest -v 2
```

Shows detailed test execution flow.

### 2. Use Print Statements

```python
def test_example(self):
    response = self.client.post('/api/books/create/', data, **auth_headers)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.data}")
    self.assertEqual(response.status_code, status.HTTP_201_CREATED)
```

### 3. Inspect Response

```python
print(json.dumps(response.data, indent=2))
```

### 4. Check Database State

```python
print(Book.objects.all().count())
book = Book.objects.get(id=X)
print(book.title)
```

### 5. Use Debugger

```bash
python manage.py test api --pdb
```

Drops into Python debugger on test failure.

### 6. Check Test Database

```bash
python manage.py test api --keepdb
# Database persists for inspection
```

---

## Adding New Tests

### Template

```python
def test_descriptive_name(self):
    """
    Brief description of what is being tested.
    
    Arrange: Set up test data
    Act: Perform the action
    Assert: Verify the result
    """
    # ARRANGE
    auth_headers = self.get_auth_headers()
    data = {'title': 'Test Book', ...}
    
    # ACT
    response = self.client.post('/api/books/create/', data, **auth_headers)
    
    # ASSERT
    self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    self.assertEqual(response.data['title'], 'Test Book')
    self.assertTrue(Book.objects.filter(title='Test Book').exists())
```

### Best Practices

1. **One assertion per test** (ideally)
   - Makes it clear what failed

2. **Descriptive names**
   - `test_create_book_authenticated` (✅)
   - `test_create` (❌)

3. **Test one thing**
   - Don't test multiple features in one test

4. **Use setUp/tearDown**
   - Don't repeat test data creation

5. **Test edge cases**
   - Invalid input
   - Empty results
   - Boundary values

### Example: Adding New Test

```python
class BookListViewTest(BaseBookTestCase):
    # ... existing tests ...
    
    def test_filter_by_nonexistent_year(self):
        """Test filtering by year with no books."""
        response = self.client.get('/api/books/?publication_year=1900')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)
```

---

## Test Execution Timeline

### Before Each Test
1. Database created (fresh)
2. `setUp()` method called
3. Test data created
4. Test method runs

### After Each Test
1. Test method completes
2. `tearDown()` method called
3. Test database dropped
4. Results recorded

### Overall Test Run
1. Discover all test methods
2. Execute tests sequentially
3. Collect results
4. Display summary

---

## Continuous Testing

### Auto-run Tests on File Change

```bash
python manage.py test api --keepdb --liveserver=localhost:8000 &
```

### Watch for Changes and Re-run

Using external tool like `pytest-watch`:

```bash
ptw -- api/tests.py
```

---

## Performance Optimization

### Reduce Test Time

1. **Use `--keepdb`**
   ```bash
   python manage.py test api --keepdb
   ```

2. **Use `--parallel`**
   ```bash
   python manage.py test api --parallel
   ```

3. **Reduce test data**
   - Only create necessary data in `setUp()`

4. **Mock external calls**
   - Don't call real APIs in tests

---

## Test Maintenance

### When to Update Tests

- New feature added → Add new tests
- Bug fixed → Add regression test
- Endpoint behavior changed → Update tests
- Dependencies updated → Verify tests still work

### Running Tests After Changes

```bash
# After code changes
python manage.py test api -v 2

# Before committing
python manage.py test api --failfast
```

The `--failfast` flag stops at first failure (useful during development).

---

## Summary

| Task | Command |
|------|---------|
| Run all tests | `python manage.py test api` |
| Run specific test | `python manage.py test api.tests.BookListViewTest` |
| Verbose output | `python manage.py test api -v 2` |
| Keep test DB | `python manage.py test api --keepdb` |
| Run in parallel | `python manage.py test api --parallel` |
| With debugger | `python manage.py test api --pdb` |
| Stop on first fail | `python manage.py test api --failfast` |

---

## References

- [Django Testing Documentation](https://docs.djangoproject.com/en/5.2/topics/testing/)
- [Django REST Framework Testing](https://www.django-rest-framework.org/api-guide/testing/)
- [Python unittest Documentation](https://docs.python.org/3/library/unittest.html)

---

**Last Updated:** December 26, 2025
