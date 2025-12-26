# Quick Test Reference

## Running Tests - Quick Commands

### Basic Commands

```bash
# Run all tests
python manage.py test api

# Run with output
python manage.py test api -v 2

# Run specific class
python manage.py test api.tests.BookListViewTest

# Run specific test
python manage.py test api.tests.BookListViewTest.test_list_books_unauthenticated
```

---

## Test Classes & Coverage

| Class | Tests | Purpose |
|-------|-------|---------|
| `BookListViewTest` | 15 | List, filter, search, order |
| `BookDetailViewTest` | 4 | Retrieve single book |
| `BookCreateViewTest` | 10 | Create books |
| `BookUpdateViewTest` | 8 | Update books (PATCH/PUT) |
| `BookDeleteViewTest` | 6 | Delete books |
| `PermissionTest` | 8 | Auth & permissions |
| `EdgeCaseTests` | 5 | Special scenarios |

---

## Test Methods by Feature

### Filtering Tests
```bash
python manage.py test api.tests.BookListViewTest.test_filter_by_title
python manage.py test api.tests.BookListViewTest.test_filter_by_author
python manage.py test api.tests.BookListViewTest.test_filter_by_publication_year
```

### Search Tests
```bash
python manage.py test api.tests.BookListViewTest.test_search_by_title
python manage.py test api.tests.BookListViewTest.test_search_case_insensitive
python manage.py test api.tests.BookListViewTest.test_search_by_author_name
```

### Ordering Tests
```bash
python manage.py test api.tests.BookListViewTest.test_order_by_title_ascending
python manage.py test api.tests.BookListViewTest.test_order_by_publication_year_descending
```

### Permission Tests
```bash
python manage.py test api.tests.PermissionTest
```

---

## Useful Flags

| Flag | Purpose | Example |
|------|---------|---------|
| `-v 2` | Verbose output | `test api -v 2` |
| `--keepdb` | Keep test DB | `test api --keepdb` |
| `--failfast` | Stop on first failure | `test api --failfast` |
| `--parallel` | Run in parallel | `test api --parallel` |
| `-k KEYWORD` | Run matching tests | `test api -k filter` |

---

## Expected Output

### Success
```
Ran 71 tests in 2.345s
OK
```

### With Verbose Output
```
test_list_books_unauthenticated (api.tests.BookListViewTest) ... ok
test_filter_by_title (api.tests.BookListViewTest) ... ok
...
Ran 71 tests in 2.345s
OK
```

### Failure Example
```
FAIL: test_create_book_authenticated (api.tests.BookCreateViewTest)
AssertionError: 403 != 201

Ran 71 tests in 2.345s
FAILED (failures=1)
```

---

## Development Workflow

### While Developing
```bash
python manage.py test api --failfast --keepdb -v 2
```

### Before Committing
```bash
python manage.py test api
```

### After Major Changes
```bash
python manage.py test api --parallel
```

---

## Debugging Tests

### Show prints/debugs
```bash
python manage.py test api -v 2
```

### Keep database for inspection
```bash
python manage.py test api --keepdb
# Then inspect: Book.objects.all()
```

### Drop into debugger
```bash
python manage.py test api --pdb
```

---

## Test Statistics

- **Total Tests:** 71+
- **Test Classes:** 8
- **Coverage:**
  - ✅ List endpoint
  - ✅ Detail endpoint
  - ✅ Create endpoint
  - ✅ Update endpoint
  - ✅ Delete endpoint
  - ✅ Filtering
  - ✅ Searching
  - ✅ Ordering
  - ✅ Permissions
  - ✅ Edge cases

---

## Common Test Scenarios

### Test Filtering
```bash
python manage.py test api.tests.BookListViewTest -v 2 -k filter
```

### Test CRUD Operations
```bash
# Create
python manage.py test api.tests.BookCreateViewTest -v 2

# Read
python manage.py test api.tests.BookDetailViewTest -v 2

# Update
python manage.py test api.tests.BookUpdateViewTest -v 2

# Delete
python manage.py test api.tests.BookDeleteViewTest -v 2
```

### Test Permissions
```bash
python manage.py test api.tests.PermissionTest -v 2
```

---

## Files to Review

- `api/tests.py` - Test implementations (922 lines)
- `TESTING_DOCUMENTATION.md` - Complete testing guide
- `UNIT_TESTS_IMPLEMENTATION.md` - Implementation details

---

## Quick Tips

✅ Use `--keepdb` for faster repeated runs  
✅ Use `--failfast` during development  
✅ Use `-v 2` to see test names  
✅ Run full suite before committing  
✅ Add tests when fixing bugs  
✅ One assertion per test (ideally)  

---

**Updated:** December 26, 2025
