from rest_framework import serializers
from .models import Author, Book
from datetime import datetime


# BookSerializer
# This serializer handles the serialization and deserialization of Book model instances.
# It converts Book objects to JSON format for API responses and validates incoming
# JSON data when creating or updating Book instances.
class BookSerializer(serializers.ModelSerializer):
    # Meta class defines which model and fields to serialize
    class Meta:
        model = Book
        # Serialize all fields: id, title, publication_year, and author (as foreign key ID)
        fields = '__all__'
    
    # Custom validation method for the publication_year field
    # This method is automatically called during the validation process
    # Method naming convention: validate_<field_name>
    def validate_publication_year(self, value):
        """
        Validates that the publication year is not in the future.
        
        Args:
            value (int): The publication year to validate
            
        Returns:
            int: The validated publication year
            
        Raises:
            serializers.ValidationError: If the year is in the future
        """
        current_year = datetime.now().year
        
        # Check if the publication year exceeds the current year
        if value > current_year:
            raise serializers.ValidationError(
                f"Publication year cannot be in the future. Current year is {current_year}."
            )
        
        # Additional validation: reasonable lower bound (books can't be too old)
        if value < 1450:  # Gutenberg's printing press era
            raise serializers.ValidationError(
                "Publication year seems unrealistic. Please enter a valid year."
            )
            
        return value


# AuthorSerializer  
# This serializer handles the serialization of Author model instances with nested
# book data. It demonstrates how to handle one-to-many relationships in DRF by
# including related Book objects within the Author serialization.
class AuthorSerializer(serializers.ModelSerializer):
    # Nested serializer for related books
    # The 'books' field corresponds to the related_name='books' in the Book model's
    # ForeignKey relationship to Author.
    # many=True indicates this is a one-to-many relationship (one author, many books)
    # read_only=True means this field is only used for serialization (GET requests),
    # not for deserialization (POST/PUT requests). This prevents clients from
    # creating/updating books directly through the author endpoint.
    books = BookSerializer(many=True, read_only=True)
    
    class Meta:
        model = Author
        # Include the author's ID, name, and all related books
        fields = ['id', 'name', 'books']
    
    # Optional: Custom representation method to add computed fields
    def to_representation(self, instance):
        """
        Customizes the serialized representation of the Author instance.
        This method is called when converting the Author object to JSON.
        
        Args:
            instance: The Author model instance being serialized
            
        Returns:
            dict: The serialized representation with additional computed fields
        """
        # Get the default representation from the parent class
        representation = super().to_representation(instance)
        
        # Add a computed field showing the total number of books by this author
        # This provides useful summary information without additional queries
        representation['book_count'] = instance.books.count()
        
        return representation


# Relationship Handling Explanation:
# =====================================
# The Author-Book relationship is handled through Django's ForeignKey on the Book model.
# In the serializers:
# 
# 1. BookSerializer: 
#    - Serializes individual Book instances
#    - The 'author' field is represented as a foreign key ID by default
#    - Includes custom validation for publication_year
#
# 2. AuthorSerializer:
#    - Serializes Author instances with nested book data
#    - Uses BookSerializer(many=True, read_only=True) to serialize related books
#    - The 'books' field is populated from the reverse relationship (related_name='books')
#    - When an Author is serialized, it automatically includes all associated Book objects
#    - The relationship is read-only to maintain data integrity
#
# Data Flow:
# - GET /authors/<id>/ returns an Author with nested array of Books
# - POST /books/ creates a Book and links it to an existing Author via author_id
# - The nested structure allows clients to retrieve complete author information
#   including all their books in a single API call
