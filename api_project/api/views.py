from rest_framework import generics,viewsets
from .models import Book
from .serializers import BookSerializer

#List only view
class BookList(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

#Implement CRUD
class BookViewSet(viewsets.ModelViewSet):
    """
    Provides list, create, retrieve, update, and delete actions
    for the Book model.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer