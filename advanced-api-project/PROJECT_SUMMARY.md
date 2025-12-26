# Advanced API Project - Setup Summary

## Project Overview
Successfully created a Django REST Framework project with custom serializers that handle complex data structures and nested relationships.

## Project Structure
`
advanced-api-project/
 manage.py                          # Django management script
 db.sqlite3                         # SQLite database
 README.md                          # Project documentation
 test_serializers.py               # Serializer test script
 advanced_api_project/             # Main project directory
    settings.py                   # Project settings (configured with DRF)
    urls.py                       # URL routing
    wsgi.py                       # WSGI configuration
    asgi.py                       # ASGI configuration
 api/                              # API application
     models.py                     # Author and Book models
     serializers.py                # Custom serializers with validation
     admin.py                      # Django admin configuration
     views.py                      # API views (ready for implementation)
     tests.py                      # Unit tests
     migrations/                   # Database migrations
         0001_initial.py           # Initial migration
`

## Completed Tasks

###  Step 1: Installation
- Installed Django 6.0
- Installed Django REST Framework
- Created project directory: advanced-api-project

###  Step 2: Project Initialization
- Created Django project: advanced_api_project
- Created Django app: api
- Configured settings.py with:
  - rest_framework in INSTALLED_APPS
  - api app in INSTALLED_APPS
  - SQLite database (default)

###  Step 3: Data Models
Created two models with comprehensive documentation:

**Author Model:**
- Field: name (CharField, max_length=100)
- Serves as the "one" side of one-to-many relationship
- Includes __str__ method and Meta class for ordering

**Book Model:**
- Field: title (CharField, max_length=200)
- Field: publication_year (IntegerField)
- Field: author (ForeignKey to Author with CASCADE delete)
- Related name: 'books' for reverse lookups
- Includes __str__ method and Meta class for ordering

**Relationship:**
- One-to-many: One Author can have many Books
- Foreign key with on_delete=CASCADE
- Related name 'books' enables author.books.all() queries

###  Step 4: Migrations
- Created initial migration (0001_initial.py)
- Applied all migrations successfully
- Database tables created for Author and Book models

###  Step 5: Custom Serializers
Created two serializers with extensive documentation:

**BookSerializer:**
- Serializes all Book model fields
- Custom validation method: validate_publication_year()
  - Ensures publication_year is not in the future
  - Validates year is not before 1450 (printing press era)
  - Returns detailed error messages

**AuthorSerializer:**
- Serializes Author with nested Book data
- Uses BookSerializer(many=True, read_only=True) for books field
- Includes custom to_representation() method
- Adds computed field: book_count
- Demonstrates nested relationship handling

**Validation Features:**
- Future year validation (prevents years > current year)
- Historical validation (prevents unrealistic ancient years)
- Clear, descriptive error messages
- Automatic validation during serialization

###  Step 6: Documentation
Both models.py and serializers.py include:
- Detailed class-level comments
- Field-level documentation
- Method documentation with docstrings
- Relationship handling explanations
- Usage examples and data flow descriptions

###  Step 7: Django Admin Configuration
Configured admin interface for both models:

**AuthorAdmin:**
- List display: id, name, book_count
- Search by name
- Custom book_count method
- Alphabetical ordering

**BookAdmin:**
- List display: id, title, author, publication_year
- Filters: author, publication_year
- Search: title and author name
- Organized fieldsets
- Newest books first ordering

###  Step 8: Testing
Created and executed comprehensive test script (test_serializers.py):

**Test Results:**
1.  Author Creation & Serialization
   - Created author: J.K. Rowling
   - Serialized with empty books list and book_count: 0

2.  Book Creation & Serialization
   - Created 2 books successfully
   - Both books properly linked to author
   - Correct serialization of all fields

3.  Nested Serialization
   - Author serialized with nested books array
   - Both books included in author data
   - book_count computed field showing 2

4.  Future Year Validation
   - Correctly rejected publication_year: 2030
   - Error message: "Publication year cannot be in the future. Current year is 2025."

5.  Historical Year Validation
   - Correctly rejected publication_year: 1400
   - Error message: "Publication year seems unrealistic. Please enter a valid year."

## Key Features Implemented

1. **Custom Serializers**
   - ModelSerializer inheritance
   - Field-level validation
   - Custom validation methods
   - Nested serialization

2. **Nested Relationships**
   - One-to-many Author-Book relationship
   - Reverse relationship with related_name
   - Nested BookSerializer in AuthorSerializer
   - Read-only nested fields for data integrity

3. **Data Validation**
   - Custom validate_publication_year() method
   - Range validation (1450 to current year)
   - Descriptive error messages
   - Automatic invocation during deserialization

4. **Django Admin**
   - Custom admin classes for both models
   - Enhanced list displays
   - Search and filter capabilities
   - Computed fields (book_count)

## How to Use

### Access Django Admin
1. Create superuser:
   `powershell
   python manage.py createsuperuser
   `

2. Run development server:
   `powershell
   python manage.py runserver
   `

3. Access admin at: http://127.0.0.1:8000/admin/

### Test in Django Shell
`powershell
python manage.py shell
`

Then:
`python
from api.models import Author, Book
from api.serializers import AuthorSerializer, BookSerializer

# Create author
author = Author.objects.create(name="Jane Austen")

# Create book with validation
book_data = {
    'title': 'Pride and Prejudice',
    'publication_year': 1813,
    'author': author.id
}
serializer = BookSerializer(data=book_data)
if serializer.is_valid():
    book = serializer.save()
    print(serializer.data)

# Serialize author with nested books
author_serializer = AuthorSerializer(author)
print(author_serializer.data)
`

### Test Validation
`python
# This will fail - future year
future_book = BookSerializer(data={
    'title': 'Future Book',
    'publication_year': 2030,
    'author': 1
})
future_book.is_valid()  # Returns False
print(future_book.errors)  # Shows validation error
`

## Next Steps (Optional Enhancements)

1. **Create API Views**
   - List/Create views for Authors and Books
   - Detail/Update/Delete views
   - ViewSets for RESTful endpoints

2. **Add URL Routing**
   - Configure urls.py with API endpoints
   - Use Django REST Framework routers

3. **Add Permissions**
   - Authentication classes
   - Permission classes
   - Token authentication

4. **Add Filtering**
   - django-filter integration
   - Search functionality
   - Ordering options

5. **Add Pagination**
   - PageNumberPagination
   - LimitOffsetPagination

## Technical Details

- **Django Version:** 6.0
- **Python Version:** 3.14.0
- **Database:** SQLite3
- **Framework:** Django REST Framework
- **Models:** Author, Book (one-to-many relationship)
- **Serializers:** BookSerializer, AuthorSerializer (with nesting)
- **Validation:** Custom publication_year validation
- **Admin:** Fully configured for both models

## Validation Rules

**Publication Year:**
- Must be >= 1450 (Gutenberg printing press era)
- Must be <= current year (2025)
- Enforced in BookSerializer.validate_publication_year()
- Returns clear error messages for violations

## Project Location
`
C:\Users\X1 Carbon\desktop\Alx_DjangoLearnLab\advanced-api-project\
`

## Success Criteria Met 

All task requirements have been successfully completed:
-  Django and DRF installed
-  Project created (advanced_api_project)
-  App created (api)
-  rest_framework added to INSTALLED_APPS
-  SQLite database configured
-  Author and Book models created with proper relationships
-  Migrations created and applied
-  BookSerializer with all fields
-  AuthorSerializer with nested BookSerializer
-  Custom validation for publication_year
-  Comprehensive documentation in code
-  Django admin configured
-  Tested via Django shell

All tests passed successfully! The project is ready for further API development.
