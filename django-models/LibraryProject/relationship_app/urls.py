# relationship_app/urls.py
from django.urls import path
from .views import list_books, LibraryDetailView, register_view, login_view, logout_view  # ← ALL EXPLICIT IMPORTS

app_name = 'relationship_app'

urlpatterns = [
    # Authentication URLs
    path('register/', register_view, name='register'),      # DIRECT FUNCTION REFERENCE
    path('login/', login_view, name='login'),               #  DIRECT FUNCTION REFERENCE  
    path('logout/', logout_view, name='logout'),            #  DIRECT FUNCTION REFERENCE
    
    # Existing library URLs
    path('books/', list_books, name='list_books'),         #  DIRECT FUNCTION REFERENCE
    path('libraries/<int:pk>/', LibraryDetailView.as_view(), name='library_detail'),
]