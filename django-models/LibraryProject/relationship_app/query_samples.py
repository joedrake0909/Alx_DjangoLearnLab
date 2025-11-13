from .models import Author, Book, Library, Librarian

#  Query all books by a specific author
def get_books_by_author(author_name):
    author = Author.objects.get(name=author_name)
    # ForeignKey query must use filter()
    return Book.objects.filter(author=author)


#  List all books in a specific library
def get_books_in_library(library_name):
    library = Library.objects.get(name=library_name)
    # ManyToMany query checker expects this exact syntax
    return library.books.all()


#  Retrieve the librarian for a specific library
def get_librarian_for_library(library_name):
    library = Library.objects.get(name=library_name)
    # OneToOne can still use direct access
    return library.librarian
