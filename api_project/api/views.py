from rest_framework import generics, viewsets, permissions
from .models import Book
from .serializers import BookSerializer

# List-only view (optional: can also restrict)
class BookList(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]  # Only logged-in users can access

# CRUD ViewSet with permissions
class BookViewSet(viewsets.ModelViewSet):
    """
    Provides list, create, retrieve, update, and delete actions
    for the Book model.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated | permissions.IsAdminUser]

