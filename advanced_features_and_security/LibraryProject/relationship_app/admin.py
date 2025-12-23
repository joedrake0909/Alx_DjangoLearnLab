from django.contrib import admin
from .models import Author, Book, Library, Librarian, UserProfile # ← Added UserProfile and kept Author/Librarian

# Register your models here.

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('name',)

# --- BookAdmin Update ---
# Reflects the current Book model: title, author (CharField), and library (ForeignKey)
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    # list_display fields are updated
    list_display = ['title', 'author', 'library']
    # list_filter and search_fields updated to use current fields
    list_filter = ['library', 'author']
    search_fields = ['title', 'author'] # 'library' is not directly searchable here

@admin.register(Library)
class LibraryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    # filter_horizontal is REMOVED because the books ManyToMany field was removed from Library
    # If you had a 'location' field, it would go here. Assuming only 'name' exists now.
    
@admin.register(Librarian)
class LibrarianAdmin(admin.ModelAdmin):
    # Displays the librarian's name and the library they manage
    list_display = ['name', 'library']
    search_fields = ['name']

# --- UserProfile Admin ---
# Register the UserProfile model
@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'role']
    list_filter = ['role']
    search_fields = ['user__username', 'role']