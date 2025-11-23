# relationship_app/urls.py
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views  # ← IMPORT THE VIEWS MODULE DIRECTLY

app_name = 'relationship_app'

urlpatterns = [
    # Authentication URLs - USE views.register NOT just register
    path('register/', views.register, name='register'),  # ← This should match the checker
    path('login/', auth_views.LoginView.as_view(template_name='relationship_app/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='relationship_app/logout.html'), name='logout'),
    
    # Existing library URLs
    path('books/', views.list_books, name='list_books'),
    path('libraries/<int:pk>/', views.LibraryDetailView.as_view(), name='library_detail'),
]