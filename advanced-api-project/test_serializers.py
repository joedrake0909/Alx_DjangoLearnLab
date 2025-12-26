from api.models import Author, Book
from api.serializers import AuthorSerializer, BookSerializer
from datetime import datetime

# Test 1: Create and serialize an Author
print("="*50)
print("TEST 1: Creating and Serializing an Author")
print("="*50)

# Create an author
author = Author.objects.create(name="J.K. Rowling")
print(f"Created Author: {author}")

# Serialize the author (without books initially)
author_serializer = AuthorSerializer(author)
print(f"\nSerialized Author Data:")
print(author_serializer.data)

# Test 2: Create and serialize Books
print("\n" + "="*50)
print("TEST 2: Creating and Serializing Books")
print("="*50)

# Create books for the author
book1_data = {
    'title': 'Harry Potter and the Philosopher\'s Stone',
    'publication_year': 1997,
    'author': author.id
}

book_serializer1 = BookSerializer(data=book1_data)
if book_serializer1.is_valid():
    book1 = book_serializer1.save()
    print(f"Created Book 1: {book1}")
    print(f"Serialized Book 1 Data: {book_serializer1.data}")
else:
    print(f"Book 1 Validation Errors: {book_serializer1.errors}")

book2_data = {
    'title': 'Harry Potter and the Chamber of Secrets',
    'publication_year': 1998,
    'author': author.id
}

book_serializer2 = BookSerializer(data=book2_data)
if book_serializer2.is_valid():
    book2 = book_serializer2.save()
    print(f"\nCreated Book 2: {book2}")
    print(f"Serialized Book 2 Data: {book_serializer2.data}")
else:
    print(f"Book 2 Validation Errors: {book_serializer2.errors}")

# Test 3: Serialize Author with nested books
print("\n" + "="*50)
print("TEST 3: Author with Nested Books")
print("="*50)

# Re-serialize the author to include the books
author_with_books = AuthorSerializer(author)
print(f"Author with Nested Books:")
import json
print(json.dumps(author_with_books.data, indent=2))

# Test 4: Test custom validation - future year
print("\n" + "="*50)
print("TEST 4: Testing Custom Validation (Future Year)")
print("="*50)

future_book_data = {
    'title': 'Future Book',
    'publication_year': 2030,
    'author': author.id
}

future_book_serializer = BookSerializer(data=future_book_data)
if future_book_serializer.is_valid():
    print("Future book validated successfully (UNEXPECTED!)")
else:
    print(f"Validation correctly failed!")
    print(f"Errors: {future_book_serializer.errors}")

# Test 5: Test custom validation - old year
print("\n" + "="*50)
print("TEST 5: Testing Custom Validation (Too Old Year)")
print("="*50)

old_book_data = {
    'title': 'Ancient Book',
    'publication_year': 1400,
    'author': author.id
}

old_book_serializer = BookSerializer(data=old_book_data)
if old_book_serializer.is_valid():
    print("Old book validated successfully (UNEXPECTED!)")
else:
    print(f"Validation correctly failed!")
    print(f"Errors: {old_book_serializer.errors}")

print("\n" + "="*50)
print("ALL TESTS COMPLETED!")
print("="*50)
