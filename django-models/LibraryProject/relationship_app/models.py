from django.db import models
from django.contrib.auth.models import User  # ← ADD THIS IMPORT

# UserProfile model with roles
class UserProfile(models.Model):
    ADMIN = 'Admin'
    MEMBER = 'Member'
    
    ROLE_CHOICES = [
        (ADMIN, 'Admin'),
        (MEMBER, 'Member'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default=MEMBER)
    
    def __str__(self):
        return f"{self.user.username} - {self.role}"

# Author can have many books
class Author(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

# Each Book is written by one Author (ForeignKey)
class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='books')
    publication_year = models.PositiveIntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.title} by {self.author.name}"

# A Library can have many Books (ManyToMany)
class Library(models.Model):
    name = models.CharField(max_length=100)
    books = models.ManyToManyField(Book, related_name='libraries')

    def __str__(self):
        return self.name

# A Library has exactly one Librarian (OneToOne)
class Librarian(models.Model):
    name = models.CharField(max_length=100)
    library = models.OneToOneField(Library, on_delete=models.CASCADE, related_name='librarian')

    def __str__(self):
        return self.name