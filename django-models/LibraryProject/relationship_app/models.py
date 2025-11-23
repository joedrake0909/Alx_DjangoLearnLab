from django.db import models
from django.contrib.auth.models import User 
from django.db.models.signals import post_save
from django.dispatch import receiver

# UserProfile model with roles
class UserProfile(models.Model):
    ADMIN = 'Admin'
    LIBRARIAN = 'Librarian'
    MEMBER = 'Member'
    
    ROLE_CHOICES = [
        (ADMIN, 'Admin'),
        (LIBRARIAN, 'Librarian'),
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

# Author can have many books (Model kept for compatibility with Librarian model, but Book no longer links to it)
class Author(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

# Each Book is written by one Author (now just a CharField) and belongs to a Library
class Book(models.Model):
    title = models.CharField(max_length=200)
    # The ForeignKey to Author and publication_year are REMOVED
    author = models.CharField(max_length=100) # ← CHANGED to CharField
    library = models.ForeignKey('Library', on_delete=models.CASCADE, related_name='inventory') # ← ADDED library link. related_name added for clarity.
    
    # Custom permissions for the Book model
    class Meta:
        permissions = [
            ("can_add_book", "Can add book"),
            ("can_change_book", "Can change book"),
            ("can_delete_book", "Can delete book"),
        ]
    
    def __str__(self):
        # Adjusted __str__ to reflect simpler author field
        return f"{self.title} by {self.author}"

# A Library can have many Books (ManyToMany is now one-to-many via Book.library)
class Library(models.Model):
    name = models.CharField(max_length=100)
    # books ManyToManyField is REMOVED as the relationship is now defined on the Book model (ForeignKey)
    
    def __str__(self):
        return self.name

# A Library has exactly one Librarian (OneToOne)
class Librarian(models.Model):
    name = models.CharField(max_length=100)
    # The Library model no longer has a ManyToMany field to Book, which simplifies this model's role contextually.
    library = models.OneToOneField(Library, on_delete=models.CASCADE, related_name='librarian')

    def __str__(self):
        return self.name