from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import permission_required
from .models import Book

# View to list books (Requires can_view)
@permission_required('relationship_app.can_view', raise_exception=True)
def book_list(request):
    books = Book.objects.all()
    return render(request, 'relationship_app/book_list.html', {'books': books})

# View to add a book (Requires can_create)
@permission_required('relationship_app.can_create', raise_exception=True)
def add_book(request):
    if request.method == "POST":
        # logic to save book
        pass
    return render(request, 'relationship_app/add_book.html')

# View to edit a book (Requires can_edit)
@permission_required('relationship_app.can_edit', raise_exception=True)
def edit_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == "POST":
        # logic to update book
        pass
    return render(request, 'relationship_app/edit_book.html', {'book': book})

# View to delete a book (Requires can_delete)
@permission_required('relationship_app.can_delete', raise_exception=True)
def delete_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == "POST":
        book.delete()
        return redirect('book_list')
    return render(request, 'relationship_app/delete_confirm.html', {'book': book})