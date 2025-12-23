# bookshelf/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import permission_required
from django.db.models import Q  # For more complex queries
from .models import Book
from .forms import BookForm  # Assuming you have a BookForm

# View to list books with search (Requires can_view)
@permission_required('relationship_app.can_view', raise_exception=True)
def book_list(request):
    # SECURE: Using the ORM handles parameterization automatically
    query = request.GET.get('q', '')
    
    if query:
        # Safe search using Django ORM (prevents SQL injection)
        # Searching in both title and author fields
        books = Book.objects.filter(
            Q(title__icontains=query) | 
            Q(author__icontains=query)
        ).distinct()
    else:
        books = Book.objects.all()
    
    return render(request, 'relationship_app/book_list.html', {
        'books': books, 
        'query': query
    })

# View to add a book (Requires can_create)
@permission_required('relationship_app.can_create', raise_exception=True)
def add_book(request):
    if request.method == "POST":
        form = BookForm(request.POST)
        if form.is_valid():
            # SECURE: Form validation and cleaned data
            book = form.save(commit=False)
            # You can add additional processing here
            book.save()
            return redirect('book_list')
    else:
        form = BookForm()
    
    return render(request, 'relationship_app/add_book.html', {'form': form})

# View to edit a book (Requires can_edit)
@permission_required('relationship_app.can_edit', raise_exception=True)
def edit_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    
    if request.method == "POST":
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            return redirect('book_list')
    else:
        form = BookForm(instance=book)
    
    return render(request, 'relationship_app/edit_book.html', {
        'form': form, 
        'book': book
    })

# View to delete a book (Requires can_delete)
@permission_required('relationship_app.can_delete', raise_exception=True)
def delete_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    
    if request.method == "POST":
        book.delete()
        return redirect('book_list')
    
    return render(request, 'relationship_app/delete_confirm.html', {'book': book})

# Advanced search view (optional - for more complex searches)
@permission_required('relationship_app.can_view', raise_exception=True)
def advanced_search(request):
    books = Book.objects.all()
    
    # Get multiple search parameters safely
    title_query = request.GET.get('title', '')
    author_query = request.GET.get('author', '')
    year_query = request.GET.get('year', '')
    
    # Build query dynamically and safely
    if title_query:
        books = books.filter(title__icontains=title_query)
    if author_query:
        books = books.filter(author__icontains=author_query)
    if year_query:
        # Validate year is a number before using
        if year_query.isdigit():
            books = books.filter(published_year=year_query)
    
    return render(request, 'relationship_app/advanced_search.html', {
        'books': books,
        'title_query': title_query,
        'author_query': author_query,
        'year_query': year_query
    })