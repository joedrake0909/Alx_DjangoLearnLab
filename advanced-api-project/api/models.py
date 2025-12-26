from django.db import models

# Author Model
# This model represents an author in the system.
# It serves as the "one" side of a one-to-many relationship with the Book model.
# An author can have multiple books associated with them.
class Author(models.Model):
    # The name field stores the author's full name as a character field
    # max_length=100 provides sufficient space for most author names
    name = models.CharField(max_length=100)
    
    def __str__(self):
        # String representation returns the author's name for easy identification
        # in the Django admin interface and shell
        return self.name
    
    class Meta:
        # Metadata for the Author model
        ordering = ['name']  # Orders authors alphabetically by name
        verbose_name = 'Author'
        verbose_name_plural = 'Authors'


# Book Model  
# This model represents a book in the system.
# It establishes a many-to-one relationship with the Author model,
# meaning multiple books can be associated with a single author.
class Book(models.Model):
    # The title field stores the book's title
    title = models.CharField(max_length=200)
    
    # The publication_year field stores the year the book was published
    # This will be validated in the serializer to ensure it's not in the future
    publication_year = models.IntegerField()
    
    # Foreign key relationship to the Author model
    # related_name='books' allows reverse lookup from Author to Book instances
    # Example: author.books.all() returns all books by that author
    # on_delete=models.CASCADE ensures that if an author is deleted,
    # all their books are also deleted (maintains referential integrity)
    author = models.ForeignKey(
        Author, 
        on_delete=models.CASCADE, 
        related_name='books'
    )
    
    def __str__(self):
        # String representation shows book title and author for clarity
        return f"{self.title} by {self.author.name}"
    
    class Meta:
        # Metadata for the Book model
        ordering = ['-publication_year', 'title']  # Orders by newest first, then by title
        verbose_name = 'Book'
        verbose_name_plural = 'Books'
