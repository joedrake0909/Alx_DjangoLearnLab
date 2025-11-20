from django.shortcuts import render, get_object_or_404
from .models import Library, Book  # REMOVED EXTRA COMMA
from django.views.generic import DetailView

# Function-based view to list all books
def list_books(request):
    books = Book.objects.all()
    context = {'books': books}
    return render(request, 'relationship_app/list_books.html', context)

# Class-based view for library details
class LibraryDetailView(DetailView):
    model = Library
    template_name = 'relationship_app/library_detail.html'  #  ADDED 'relationship_app/'
    context_object_name = 'library'