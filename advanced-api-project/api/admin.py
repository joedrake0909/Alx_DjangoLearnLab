from django.contrib import admin
from .models import Author, Book


# Custom Admin class for Author model
# Provides enhanced admin interface for managing authors
@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    # Display these fields in the admin list view
    list_display = ['id', 'name', 'book_count']
    
    # Add search functionality for author names
    search_fields = ['name']
    
    # Add ordering
    ordering = ['name']
    
    # Custom method to display the count of books for each author
    def book_count(self, obj):
        return obj.books.count()
    book_count.short_description = 'Number of Books'


# Custom Admin class for Book model
# Provides enhanced admin interface for managing books
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    # Display these fields in the admin list view
    list_display = ['id', 'title', 'author', 'publication_year']
    
    # Add filters for easy navigation
    list_filter = ['author', 'publication_year']
    
    # Add search functionality
    search_fields = ['title', 'author__name']
    
    # Add ordering (newest books first)
    ordering = ['-publication_year', 'title']
    
    # Organize fields in the edit form
    fieldsets = (
        ('Book Information', {
            'fields': ('title', 'publication_year')
        }),
        ('Author', {
            'fields': ('author',)
        }),
    )
