from django.shortcuts import render
from .models import Book, Library
from django.views.generic import DetailView

# Function-based view to list all books
def list_books(request):
    books = Book.objects.select_related('author').all()
    context = {'books': books}
    return render(request, 'relationship_app/list_books.html', context)

# Class-based view for library details
class LibraryDetailView(DetailView):
    model = Library
    template_name = 'library_detail.html'
    context_object_name = 'library' 

# Optionally override get_queryset to prefetch books for efficiency
    def get_queryset(self):
        # prefetch_related reduces DB hits when accessing many-to-many relations
        return super().get_queryset().prefetch_related('books__author')

