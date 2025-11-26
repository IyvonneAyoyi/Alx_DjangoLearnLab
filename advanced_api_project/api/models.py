from django.db import models
from django.core.exceptions import ValidationError
from datetime import date

class Author(models.Model):
    """
    Model representing an author.

    Fields:
    - name (CharField): Stores the full name of the author.

    Relationships:
    - One Author can have many Books (one-to-many).

    Purpose:
    - To store information about authors.
    """
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Book(models.Model):
    """
    Model representing a book written by an author.

    Fields:
    - title (CharField): Title of the book.
    - publication_year (IntegerField): Year the book was published.
    - author (ForeignKey): Links to the Author model (one-to-many).

    Validations:
    - publication_year cannot be in the future.

    Purpose:
    - To store information about books and link them to their authors.
    """
    title = models.CharField(max_length=255)
    publication_year = models.IntegerField()
    author = models.ForeignKey(Author, related_name='books', on_delete=models.CASCADE)

    def clean(self):
        """Custom validation to prevent future publication years."""
        if self.publication_year > date.today().year:
            raise ValidationError("Publication year cannot be in the future.")

    def __str__(self):
        return self.title