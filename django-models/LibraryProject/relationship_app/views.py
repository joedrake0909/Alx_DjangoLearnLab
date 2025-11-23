from django.shortcuts import render, redirect
from .models import Library, Book, UserProfile # ← ADDED UserProfile
from django.views.generic.detail import DetailView
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test # ← ADDED

# --- Role Check Functions ---
# These functions check the 'role' field on the UserProfile linked to the authenticated user.

def is_admin(user):
    # Check if user is authenticated and has a profile with the role 'Admin'
    return user.is_authenticated and hasattr(user, 'profile') and user.profile.role == 'Admin'

def is_librarian(user):
    # Check if user is authenticated and has a profile with the role 'Librarian'
    return user.is_authenticated and hasattr(user, 'profile') and user.profile.role == 'Librarian'

def is_member(user):
    # Check if user is authenticated and has a profile with the role 'Member'
    # NOTE: Since related_name='profile' was used in models.py, we check for 'user.profile'
    return user.is_authenticated and hasattr(user, 'profile') and user.profile.role == 'Member'


# --- Role-based Views (Restricted Access) ---
# The user_passes_test decorator redirects to the login_url if the test function returns False.

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