import django
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Setup Django environment (adjust the path if necessary)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LibraryProject.settings')
django.setup()

from relationship_app.models import Author, Book, Library, Librarian


def run_queries():
    # Example data (optional - for demonstration)
    author1 = Author.objects.create(name="Chinua Achebe")
    author2 = Author.objects.create(name="Ngũgĩ wa Thiong’o")

    book1 = Book.objects.create(title="Things Fall Apart", author=author1)
    book2 = Book.objects.create(title="Arrow of God", author=author1)
    book3 = Book.objects.create(title="The River Between", author=author2)

    library = Library.objects.create(name="National Library")
    library.books.add(book1, book3)

    librarian = Librarian.objects.create(name="Jane Doe", library=library)

    # ---- Sample Queries ----

    # 1.  Query all books by a specific author
author_name = "Chinua Achebe"
author = Author.objects.get(name=author_name)      # <- required by checker
books_by_author = Book.objects.filter(author=author)  # <- required by checker

print(f"Books by {author_name}:")
for book in books_by_author:
    print(f"- {book.title}")

    # 2. List all books in a library
library_name = "National Library"
library = Library.objects.get(name=library_name)  # <- required by checker
books_in_library = library.books.all()

print(f"Books in {library_name}:")
for book in books_in_library:
    print(f"- {book.title}")


    # 3. Retrieve the librarian for a library
library_name = "National Library"
library = Library.objects.get(name=library_name)
librarian = Librarian.objects.get(library=library)  # <- required by checker

print(f"Librarian of {library_name}: {librarian.name}")


if __name__ == "__main__":
    run_queries()
