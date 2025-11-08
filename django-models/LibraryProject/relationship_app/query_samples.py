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
    books_by_achebe = Book.objects.filter(author__name="Chinua Achebe")
    print("\nBooks by Chinua Achebe:")
    for book in books_by_achebe:
        print(f"- {book.title}")

    # 2. List all books in a library
library_name = "National Library"
library = Library.objects.get(name=library_name)  # <- required by checker
books_in_library = library.books.all()

print(f"Books in {library_name}:")
for book in books_in_library:
    print(f"- {book.title}")


    # 3. Retrieve the librarian for a library
    librarian_of_library = library.librarian
    print(f"\nLibrarian of {library.name}: {librarian_of_library.name}")


if __name__ == "__main__":
    run_queries()
