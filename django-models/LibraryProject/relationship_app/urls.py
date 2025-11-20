# relationship_app/urls.py
from django.urls import path
from .views import list_books  #  EXPLICIT IMPORT
from .views import LibraryDetailView

app_name = 'relationship_app'

urlpatterns = [
    path('books/', list_books, name='list_books'),  #  DIRECT FUNCTION REFERENCE
    path('libraries/<int:pk>/', LibraryDetailView.as_view(), name='library_detail'),
]