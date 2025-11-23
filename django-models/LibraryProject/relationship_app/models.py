from django.db import models
from django.contrib.auth.models import User 
from django.db.models.signals import post_save # ← ADDED
from django.dispatch import receiver # ← ADDED

# UserProfile model with roles
class UserProfile(models.Model):
    ADMIN = 'Admin'
    LIBRARIAN = 'Librarian' # ← ADDED
    MEMBER = 'Member'
    
    ROLE_CHOICES = [
        (ADMIN, 'Admin'),
        (LIBRARIAN, 'Librarian'), # ← ADDED
        (MEMBER, 'Member'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default=MEMBER)
    
    def __str__(self):
        return f"{self.user.username} - {self.role}"

# --- UserProfile Signal Handlers ---

# Creates a UserProfile automatically when a new User is created
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

# Saves the UserProfile automatically when the User is saved/updated
@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    # Use instance.profile.save() because related_name='profile' is used on the OneToOneField
    try:
        instance.profile.save()
    except UserProfile.DoesNotExist:
        # This can happen if a User is saved before the profile is created (e.g., in bulk operations)
        # The 'create_user_profile' signal should handle initial creation, but this is a safeguard
        pass 

# --- Existing Models ---

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