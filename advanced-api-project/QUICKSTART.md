# Quick Start Guide - Advanced API Project

## Project Location
```
C:\Users\X1 Carbon\desktop\Alx_DjangoLearnLab\advanced-api-project\
```

## Quick Commands

### Navigate to Project
```powershell
cd "C:\Users\X1 Carbon\desktop\Alx_DjangoLearnLab\advanced-api-project"
```

### Run Development Server
```powershell
& "C:/Users/X1 Carbon/Desktop/Alx_DjangoLearnLab/advanced_features_and_security/.venv/Scripts/python.exe" manage.py runserver
```

### Create Superuser
```powershell
& "C:/Users/X1 Carbon/Desktop/Alx_DjangoLearnLab/advanced_features_and_security/.venv/Scripts/python.exe" manage.py createsuperuser
```

### Open Django Shell
```powershell
& "C:/Users/X1 Carbon/Desktop/Alx_DjangoLearnLab/advanced_features_and_security/.venv/Scripts/python.exe" manage.py shell
```

### Run Test Script
```powershell
Get-Content test_serializers.py | & "C:/Users/X1 Carbon/Desktop/Alx_DjangoLearnLab/advanced_features_and_security/.venv/Scripts/python.exe" manage.py shell
```

### Make Migrations
```powershell
& "C:/Users/X1 Carbon/Desktop/Alx_DjangoLearnLab/advanced_features_and_security/.venv/Scripts/python.exe" manage.py makemigrations
```

### Apply Migrations
```powershell
& "C:/Users/X1 Carbon/Desktop/Alx_DjangoLearnLab/advanced_features_and_security/.venv/Scripts/python.exe" manage.py migrate
```

## Django Shell Quick Test

```python
# Import models and serializers
from api.models import Author, Book
from api.serializers import AuthorSerializer, BookSerializer

# Create an author
author = Author.objects.create(name="George Orwell")

# Create a book (valid year)
book_data = {
    'title': '1984',
    'publication_year': 1949,
    'author': author.id
}
serializer = BookSerializer(data=book_data)
if serializer.is_valid():
    book = serializer.save()
    print("Book created:", book)
    print("Serialized data:", serializer.data)

# Test validation (this will fail)
invalid_book = BookSerializer(data={
    'title': 'Future Book',
    'publication_year': 2030,
    'author': author.id
})
print("Valid?", invalid_book.is_valid())
print("Errors:", invalid_book.errors)

# Get author with nested books
author_serializer = AuthorSerializer(author)
print("Author with books:", author_serializer.data)
```

## Key Files

- **models.py**: Author and Book models with detailed documentation
- **serializers.py**: Custom serializers with validation
- **admin.py**: Django admin configuration
- **test_serializers.py**: Automated test script
- **settings.py**: Project configuration (rest_framework enabled)
- **PROJECT_SUMMARY.md**: Complete project documentation

## Features

 Custom serializers with nested relationships  
 Publication year validation (1450 - current year)  
 One-to-many Author-Book relationship  
 Django admin with custom displays  
 Comprehensive code documentation  
 Tested and verified functionality  

## Next Steps

1. Create API views (ViewSets)
2. Configure URL routing
3. Add authentication
4. Implement permissions
5. Add filtering and pagination

For complete details, see PROJECT_SUMMARY.md
