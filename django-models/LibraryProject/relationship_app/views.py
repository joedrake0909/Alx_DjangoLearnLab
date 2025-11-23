from django.shortcuts import render, redirect, get_object_or_404 # ← ADDED get_object_or_404
from .models import Library, Book, UserProfile # ← UserProfile already added
from django.views.generic.detail import DetailView
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test, permission_required # ← ADDED permission_required
# from .forms import BookForm # ← You must create this form in forms.py for this code to run

# --- Role Check Functions ---
def is_admin(user):
    return user.is_authenticated and hasattr(user, 'profile') and user.profile.role == 'Admin'

def is_librarian(user):
    return user.is_authenticated and hasattr(user, 'profile') and user.profile.role == 'Librarian'

def is_member(user):
    return user.is_authenticated and hasattr(user, 'profile') and user.profile.role == 'Member'


# --- Role-based Views (Restricted Access) ---
@user_passes_test(is_admin, login_url='/login/')
def admin_view(request):
    """View only accessible to users with the 'Admin' role."""
    return render(request, 'relationship_app/admin_view.html')

@user_passes_test(is_librarian, login_url='/login/')
def librarian_view(request):
    """View only accessible to users with the 'Librarian' role."""
    return render(request, 'relationship_app/librarian_view.html')

@user_passes_test(is_member, login_url='/login/')
def member_view(request):
    """View only accessible to users with the 'Member' role."""
    return render(request, 'relationship_app/member_view.html')


# --- General Application Views ---

# Function-based view to list all books
def list_books(request):
    books = Book.objects.all()
    context = {'books': books}
    return render(request, 'relationship_app/list_books.html', context)

# Class-based view for library details
class LibraryDetailView(DetailView):
    model = Library
    template_name = 'relationship_app/library_detail.html'
    context_object_name = 'library'

# --- Permission-protected views for Book operations (NEWLY ADDED) ---

@permission_required('relationship_app.can_add_book', login_url='/login/')
def add_book(request):
    """Allows adding a new book, protected by the 'can_add_book' permission."""
    from .forms import BookForm # Temporary import to allow testing without forms.py, REMOVE IN PRODUCTION
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, f"Book '{form.cleaned_data['title']}' added successfully!")
            return redirect('relationship_app:list_books')
    else:
        form = BookForm()
    return render(request, 'relationship_app/add_book.html', {'form': form})

@permission_required('relationship_app.can_change_book', login_url='/login/')
def edit_book(request, book_id):
    """Allows editing an existing book, protected by the 'can_change_book' permission."""
    from .forms import BookForm # Temporary import
    book = get_object_or_404(Book, id=book_id)
    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            messages.success(request, f"Book '{book.title}' updated successfully!")
            return redirect('relationship_app:list_books')
    else:
        form = BookForm(instance=book)
    return render(request, 'relationship_app/edit_book.html', {'form': form, 'book': book})

@permission_required('relationship_app.can_delete_book', login_url='/login/')
def delete_book(request, book_id):
    """Allows deleting a book, protected by the 'can_delete_book' permission."""
    book = get_object_or_404(Book, id=book_id)
    if request.method == 'POST':
        book_title = book.title
        book.delete()
        messages.warning(request, f"Book '{book_title}' deleted.")
        return redirect('relationship_app:list_books')
    return render(request, 'relationship_app/delete_book.html', {'book': book})

# --- AUTHENTICATION VIEWS ---

def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful!")
            return redirect('relationship_app:list_books')
    else:
        form = UserCreationForm()
    return render(request, 'relationship_app/register.html', {'form': form})

def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, "Welcome back!")
            return redirect('relationship_app:list_books')
    else:
        form = AuthenticationForm()
    return render(request, 'relationship_app/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return render(request, 'relationship_app/logout.html')