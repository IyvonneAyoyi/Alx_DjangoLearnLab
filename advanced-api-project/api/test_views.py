from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User

from .models import Book, Author


class BookAPITestCase(APITestCase):
    """
    Test suite for Book API endpoints
    """

    def setUp(self):
        """
        Runs before every test
        """

        # Create user
        self.user = User.objects.create_user(
            username="testuser",
            password="testpass123"
        )

        # Create author
        self.author = Author.objects.create(name="Jane Doe")

        # Create books
        self.book1 = Book.objects.create(
            title="Book A",
            publication_year=2022,
            author=self.author
        )

        self.book2 = Book.objects.create(
            title="Book B",
            publication_year=2024,
            author=self.author
        )

        # URLs
        self.list_url = "/api/books/"
        self.create_url = "/api/books/create/"
        self.detail_url = f"/api/books/{self.book1.id}/"
        self.update_url = f"/api/books/{self.book1.id}/update/"
        self.delete_url = f"/api/books/{self.book1.id}/delete/"

    # -------------------------------
    # READ TESTS
    # -------------------------------

    def test_list_books(self):
        """Test retrieving the list of books"""
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_single_book(self):
        """Test retrieving one book"""
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "Book A")

    # -------------------------------
    # CREATE TEST
    # -------------------------------

    def test_create_book_authenticated(self):
        """Authenticated user can create book"""

        self.client.login(username="testuser", password="testpass123")

        data = {
            "title": "New Book",
            "publication_year": 2025,
            "author": self.author.id
        }

        response = self.client.post(self.create_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_book_unauthenticated(self):
        """Unauthenticated user cannot create book"""

        data = {
            "title": "Fail Book",
            "publication_year": 2025,
            "author": self.author.id
        }

        response = self.client.post(self.create_url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # -------------------------------
    # UPDATE TEST
    # -------------------------------

    def test_update_book_authenticated(self):
        """Authenticated user can update"""

        self.client.login(username="testuser", password="testpass123")

        data = {"title": "Updated Title"}

        response = self.client.patch(self.update_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # -------------------------------
    # DELETE TEST
    # -------------------------------

    def test_delete_book_authenticated(self):
        """Authenticated user can delete"""

        self.client.login(username="testuser", password="testpass123")

        response = self.client.delete(self.delete_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    # -------------------------------
    # FILTERING TEST
    # -------------------------------

    def test_filter_books_by_title(self):
        """Filter by title"""

        response = self.client.get("/api/books/?title=Book A")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # -------------------------------
    # SEARCH TEST
    # -------------------------------

    def test_search_books(self):
        """Search by author name"""

        response = self.client.get("/api/books/?search=Jane")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # -------------------------------
    # ORDERING TEST
    # -------------------------------

    def test_order_books(self):
        """Order by publication_year"""

        response = self.client.get("/api/books/?ordering=-publication_year")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
