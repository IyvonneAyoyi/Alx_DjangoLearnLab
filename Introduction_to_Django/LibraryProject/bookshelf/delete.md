from bookshelf.models import Book

# Delete the renamed book
book = Book.objects.get(title="Nineteen Eighty-Four")
book.delete()

# Delete any remaining "1984" books (if any exist)
Book.objects.filter(title="1984").delete()

# Confirm all books removed
Book.objects.all()

(1, {'bookshelf.Book': 1})
(2, {'bookshelf.Book': 2})
<QuerySet []>
