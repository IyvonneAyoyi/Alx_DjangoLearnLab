from rest_framework import serializers
from .models import Author, Book
from datetime import date

class BookSerializer(serializers.ModelSerializer):
    """
    Serializer for Book model.

    Purpose:
    - Converts Book instances to JSON for API responses.
    - Validates data before saving.

    Validations:
    - Ensures publication_year is not in the future.
    """
    class Meta:
        model = Book
        fields = ['id', 'title', 'publication_year', 'author']

    def validate_publication_year(self, value):
        """Custom field-level validation."""
        if value > date.today().year:
            raise serializers.ValidationError("Publication year cannot be in the future.")
        return value


class AuthorSerializer(serializers.ModelSerializer):
    """
    Serializer for Author model.

    Purpose:
    - Converts Author instances to JSON.
    - Includes all books by the author using nested BookSerializer.

    Relationship Handling:
    - One Author can have many Books (one-to-many).
    - Nested BookSerializer allows retrieving all related books in a single API response.
    """
    books = BookSerializer(many=True, read_only=True)  # Nested serialization

    class Meta:
        model = Author
        fields = ['id', 'name', 'books']
