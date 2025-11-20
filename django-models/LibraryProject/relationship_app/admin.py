from django.contrib import admin
from .models import Author, Book, Library, Librarian


# Register your models here.

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'publication_year')
    search_fields = ('title', 'author__name')

@admin.register(Library)
class LibraryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    filter_horizontal = ('books',)  # nicer widget when many books