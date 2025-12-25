from django.urls import path
from . import views

app_name = "bookshelf"

urlpatterns = [
    path("", views.book_list, name="book_list"),
    path("add/", views.add_book, name="add_book"),
    path("<int:pk>/edit/", views.edit_book, name="edit_book"),
    path("<int:pk>/delete/", views.delete_book, name="delete_book"),
    path("advanced-search/", views.advanced_search, name="advanced_search"),
    path("form-example/", views.search_books, name="form_example"),
]
