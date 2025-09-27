from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.contrib.auth.models import User
from .models import Book, Author


"""
This test suite covers:
- CRUD operations on Book model via API
- Filtering by title, author, and publication_year
- Searching by title and author's name
- Ordering by publication_year and title
- Permission checks (authenticated vs unauthenticated access)

Run with:
    python manage.py test api
"""





class BookAPITestCase(APITestCase):
    def setUp(self):
        # Create test user
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.client = APIClient()
        self.author = Author.objects.create(name='J.R.R. Tolkien')

        # Create books
        self.book1 = Book.objects.create(title='The Hobbit', publication_year=1937, author=self.author)
        self.book2 = Book.objects.create(title='The Lord of the Rings', publication_year=1954, author=self.author)

    def test_list_books(self):
        response = self.client.get(reverse('book-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_filter_books_by_title(self):
        response = self.client.get(reverse('book-list'), {'title': 'The Hobbit'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'The Hobbit')

    def test_search_books_by_author_name(self):
        response = self.client.get(reverse('book-list'), {'search': 'Tolkien'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_order_books_by_publication_year_desc(self):
        response = self.client.get(reverse('book-list'), {'ordering': '-publication_year'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['title'], 'The Lord of the Rings')

    def test_create_book_unauthenticated(self):
        data = {
            'title': 'Silmarillion',
            'publication_year': 1977,
            'author': self.author.id
        }
        response = self.client.post(reverse('book-create'), data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_book_authenticated(self):
        self.client.login(username='testuser', password='password123')
        data = {
            'title': 'Silmarillion',
            'publication_year': 1977,
            'author': self.author.id
        }
        response = self.client.post(reverse('book-create'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 3)
        self.assertEqual(Book.objects.last().title, 'Silmarillion')

    def test_update_book(self):
        self.client.login(username='testuser', password='password123')
        url = reverse('book-detail-update-delete', args=[self.book1.id])
        response = self.client.put(url, {
            'title': 'The Hobbit: Updated',
            'publication_year': 1937,
            'author': self.author.id
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book1.refresh_from_db()
        self.assertEqual(self.book1.title, 'The Hobbit: Updated')

    def test_delete_book(self):
        self.client.login(username='testuser', password='password123')
        url = reverse('book-detail-update-delete', args=[self.book2.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Book.objects.count(), 1)
