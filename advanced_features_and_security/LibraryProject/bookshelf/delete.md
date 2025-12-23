>>> from bookshelf.models import Book
>>> book = Book.objects.get(title="Nineteen Eighty-Four")
>>> book.delete()
(1, {'bookshelf.Book': 1})
>>> remaining_books = Book.objects.all()
>>> print(f"Remaining books: {list(remaining_books)}")
Remaining books: []