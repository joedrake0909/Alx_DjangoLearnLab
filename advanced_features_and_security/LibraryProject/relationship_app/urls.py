from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'relationship_app'

urlpatterns = [
    # Authentication URLs
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='relationship_app/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='relationship_app/logout.html'), name='logout'),
    
    # Role-based URLs
    path('admin/', views.admin_view, name='admin_view'),
    path('librarian/', views.librarian_view, name='librarian_view'),
    path('member/', views.member_view, name='member_view'),
    
    # Book management URLs with permissions - UPDATE THESE PATHS
    path('add_book/', views.add_book, name='add_book'),           # ← CHANGED from 'books/add/'
    path('edit_book/<int:book_id>/', views.edit_book, name='edit_book'),  # ← CHANGED from 'books/<int:book_id>/edit/'
    path('books/<int:book_id>/delete/', views.delete_book, name='delete_book'),
    
    # Existing library URLs
    path('books/', views.list_books, name='list_books'),
    path('libraries/<int:pk>/', views.LibraryDetailView.as_view(), name='library_detail'),
]