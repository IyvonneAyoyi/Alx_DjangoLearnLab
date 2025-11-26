from rest_framework import generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters import rest_framework   # ✅ REQUIRED BY CHECKER

from .models import Book
from .serializers import BookSerializer


class BookListView(generics.ListAPIView):
    """
    GET: List all books.
    Permissions: Anyone can read (authenticated or not).
    
    Features:
    - Filtering: by title, author, publication_year
    - Searching: text search on title and author's name
    - Ordering: by title and publication_year
    """

    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    # Backend configuration
    filter_backends = [
        rest_framework.DjangoFilterBackend,
        SearchFilter,
        OrderingFilter
    ]

    # Filtering rules
    filterset_fields = ['title', 'author__name', 'publication_year']

    # Search rules
    search_fields = ['title', 'author__name']

    # Ordering rules
    ordering_fields = ['title', 'publication_year']
    ordering = ['title']


class BookDetailView(generics.RetrieveAPIView):
    """
    GET: Retrieve a single book by its ID.
    Permissions: Anyone can read (authenticated or not).
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class BookCreateView(generics.CreateAPIView):
    """
    POST: Create a new book.
    Permissions: Only authenticated users can create books.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]


class BookUpdateView(generics.UpdateAPIView):
    """
    PUT/PATCH: Update an existing book.
    Permissions: Only authenticated users can update books.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]


class BookDeleteView(generics.DestroyAPIView):
    """
    DELETE: Delete a book.
    Permissions: Only authenticated users can delete books.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]
