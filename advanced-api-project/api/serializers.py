from rest_framework import serializers
from .models import Author, Book
from datetime import datetime

class BookSerializer(serializers.ModelSerializer):
    """
    Serializer for the Book model that handles serialization of all book fields
    and includes custom validation for publication_year.
    
    Fields:
        id (auto): Primary key
        title: Book title
        publication_year: Year of publication with custom validation
        author: Foreign key to Author model
    
    Validation:
        - publication_year cannot be in the future
    """
    class Meta:
        model = Book
        fields = ['id', 'title', 'publication_year', 'author']
    
    def validate_publication_year(self, value):
        """
        Custom validation to ensure publication year is not in the future.
        
        Args:
            value (int): The publication year to validate
            
        Returns:
            int: The validated publication year
            
        Raises:
            serializers.ValidationError: If publication year is in the future
        """
        current_year = datetime.now().year
        if value > current_year:
            raise serializers.ValidationError(
                f"Publication year cannot be in the future. Current year is {current_year}."
            )
        return value

class AuthorSerializer(serializers.ModelSerializer):
    """
    Serializer for the Author model that includes nested book information.
    
    Fields:
        id (auto): Primary key
        name: Author's name
        books: Nested serialization of all books by this author using BookSerializer
    
    The nested relationship allows serializing an author along with all their books
    in a single API response, demonstrating handling of one-to-many relationships.
    """
    books = BookSerializer(many=True, read_only=True)
    
    class Meta:
        model = Author
        fields = ['id', 'name', 'books']