# relationship_app/urls.py
from django.urls import path
from django.contrib.auth import views as auth_views
from .views import list_books, LibraryDetailView, register_view

app_name = 'relationship_app'

urlpatterns = [
    # Authentication URLs
    path('register/', register_view, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='relationship_app/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='relationship_app/logout.html'), name='logout'),
    
    # Existing library URLs
    path('books/', list_books, name='list_books'),
    path('libraries/<int:pk>/', LibraryDetailView.as_view(), name='library_detail'),
]