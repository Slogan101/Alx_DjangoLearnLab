from rest_framework import serializers
from .models import Book, Author
from django.utils import timezone

# Seriliazers for Books
class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['id', 'title', 'publication_year', 'author']

    # Validation to make sure date isn't in the future
    def validate(self, data):
        current_year = timezone.now().year
        if data['publication_year'] > current_year:
            raise serializers.ValidationError("Publication year must not be in the future.")
        return data

# Author Serializer
class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ['id', 'name']


# NESTED SERIALIZERS

class AuthorSerializer(serializers.ModelSerializer):
    book = BookSerializer(many=True, read_only=True)

    class Meta:
        model = Author
        fields = ['id', 'name', 'books'] 