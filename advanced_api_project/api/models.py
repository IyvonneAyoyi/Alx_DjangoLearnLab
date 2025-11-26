from django.db import models
from django.core.exceptions import ValidationError
from datetime import date

class Author(models.Model):
    """
    Model representing an author.
    Fields:
        - name: stores the full name of the author.
    """
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Book(models.Model):
    """
    Model representing a book written by an author.
    Fields:
        - title: title of the book
        - publication_year: the year the book was published
        - author: foreign key linking to the Author model
    """
    title = models.CharField(max_length=255)
    publication_year = models.IntegerField()
    author = models.ForeignKey(Author, related_name='books', on_delete=models.CASCADE)

    def clean(self):
        # Custom validation: publication year cannot be in the future
        if self.publication_year > date.today().year:
            raise ValidationError("Publication year cannot be in the future.")

    def __str__(self):
        return self.title
