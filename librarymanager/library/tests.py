from django.test import TestCase
from .models import Book, Author, Genre 
from django.contrib.auth.models import User, Group
from django.urls import reverse 

class BookModelTest(TestCase):
    def setUp(self):
        self.author = Author.objects.create(name="Test Author", biography="Biography", nationality="Country")
        self.genre = Genre.objects.create(name="Fiction")
        self.book = Book.objects.create(
            title="Test Book",
            author=self.author,
            publication_year=2022,
            isbn="0123456789123",
            availability_status="available"
        )
        self.book.genre.add(self.genre)

    def test_book_str(self):
        self.assertEqual(str(self.book), "Test Book")

class AuthorizationTests(TestCase):
    
    def setUp(self):
        self.admin_user = User.objects.create_superuser(username='admin', password='password')
        self.librarian_user = User.objects.create_user(username='librarian', password='password')
        self.non_librarian_user = User.objects.create_user(username='user', password='password')
        self.librarian_group = Group.objects.create(name='Librarian')
        self.librarian_user.groups.add(self.librarian_group)
        
        self.genre = Genre.objects.create(name='Science Fiction')
        self.author = Author.objects.create(name='Author Name', biography='Bio', nationality='Country')
        self.book = Book.objects.create(
            title='Test Book',
            author=self.author,
            publication_year=2023,
            isbn='1234567890123',
            genre=self.genre
        )

    def test_librarian_can_add_book(self):
        self.client.login(username='librarian', password='password')
        response = self.client.get(reverse('add_book'))
        self.assertEqual(response.status_code, 200)

    def test_non_librarian_cannot_add_book(self):
        self.client.login(username='user', password='password')
        response = self.client.get(reverse('add_book'))
        self.assertEqual(response.status_code, 403)  # Forbidden

    def test_admin_can_access_all_views(self):
        self.client.login(username='admin', password='password')
        response = self.client.get(reverse('add_book'))
        self.assertEqual(response.status_code, 200)
        response = self.client.get(reverse('add_author'))
        self.assertEqual(response.status_code, 200)
        response = self.client.get(reverse('add_genre'))
        self.assertEqual(response.status_code, 200)