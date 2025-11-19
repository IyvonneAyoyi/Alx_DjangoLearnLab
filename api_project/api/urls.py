from django.urls import path
from .views import BookList  # or BookListCreateAPIView if you choose later

urlpatterns = [
    path('books/', BookList.as_view(), name='book-list'),
]
