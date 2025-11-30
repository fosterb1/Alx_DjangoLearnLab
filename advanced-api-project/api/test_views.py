from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from django.contrib.auth.models import User
from .models import Author, Book
from datetime import datetime


class BookAPITestCase(APITestCase):
    """
    Test case for Book API endpoints including CRUD operations,
    filtering, searching, ordering, and authentication.
    """
    
    def setUp(self):
        """
        Set up test data and client for all test methods.
        This method runs before each test.
        """
        # Create test users
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword123'
        )
        self.admin_user = User.objects.create_superuser(
            username='adminuser',
            password='adminpassword123',
            email='admin@example.com'
        )
        
        # Create test authors
        self.author1 = Author.objects.create(name='J.K. Rowling')
        self.author2 = Author.objects.create(name='George R.R. Martin')
        
        # Create test books
        self.book1 = Book.objects.create(
            title='Harry Potter and the Philosopher\'s Stone',
            publication_year=1997,
            author=self.author1
        )
        self.book2 = Book.objects.create(
            title='A Game of Thrones',
            publication_year=1996,
            author=self.author2
        )
        self.book3 = Book.objects.create(
            title='Harry Potter and the Chamber of Secrets',
            publication_year=1998,
            author=self.author1
        )
        
        # Initialize API client
        self.client = APIClient()
    
    def authenticate_user(self, user=None):
        """Helper method to authenticate a user for testing using login"""
        if user is None:
            user = self.user
        self.client.login(username=user.username, password='testpassword123')
    
    def unauthenticate_user(self):
        """Helper method to remove authentication using logout"""
        self.client.logout()


class BookCRUDTests(BookAPITestCase):
    """
    Test CRUD operations for Book model endpoints.
    """
    
    def test_list_books_unauthenticated(self):
        """
        Test that unauthenticated users can retrieve the book list.
        Expected: 200 OK status and correct book count.
        """
        self.unauthenticate_user()
        url = reverse('book-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)
    
    def test_retrieve_book_detail_unauthenticated(self):
        """
        Test that unauthenticated users can retrieve a single book's details.
        Expected: 200 OK status and correct book data.
        """
        self.unauthenticate_user()
        url = reverse('book-detail', kwargs={'pk': self.book1.pk})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], self.book1.title)
        self.assertEqual(response.data['publication_year'], self.book1.publication_year)
    
    def test_create_book_authenticated(self):
        """
        Test that authenticated users can create new books.
        Expected: 201 Created status and book is created in database.
        """
        # Use self.client.login to authenticate
        self.client.login(username='testuser', password='testpassword123')
        url = reverse('book-create')
        data = {
            'title': 'New Test Book',
            'publication_year': 2020,
            'author': self.author1.pk
        }
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 4)
        self.assertEqual(Book.objects.get(pk=response.data['id']).title, 'New Test Book')
    
    def test_create_book_unauthenticated(self):
        """
        Test that unauthenticated users cannot create books.
        Expected: 403 Forbidden status.
        """
        self.unauthenticate_user()
        url = reverse('book-create')
        data = {
            'title': 'Unauthorized Book',
            'publication_year': 2020,
            'author': self.author1.pk
        }
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_update_book_authenticated(self):
        """
        Test that authenticated users can update existing books.
        Expected: 200 OK status and book is updated in database.
        """
        # Use self.client.login to authenticate
        self.client.login(username='testuser', password='testpassword123')
        url = reverse('book-update', kwargs={'pk': self.book1.pk})
        data = {
            'title': 'Updated Book Title',
            'publication_year': 1997,
            'author': self.author1.pk
        }
        response = self.client.put(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book1.refresh_from_db()
        self.assertEqual(self.book1.title, 'Updated Book Title')
    
    def test_update_book_unauthenticated(self):
        """
        Test that unauthenticated users cannot update books.
        Expected: 403 Forbidden status.
        """
        self.unauthenticate_user()
        url = reverse('book-update', kwargs={'pk': self.book1.pk})
        data = {
            'title': 'Unauthorized Update',
            'publication_year': 1997,
            'author': self.author1.pk
        }
        response = self.client.put(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_delete_book_authenticated(self):
        """
        Test that authenticated users can delete books.
        Expected: 204 No Content status and book is removed from database.
        """
        # Use self.client.login to authenticate
        self.client.login(username='testuser', password='testpassword123')
        url = reverse('book-delete', kwargs={'pk': self.book1.pk})
        response = self.client.delete(url)
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Book.objects.count(), 2)
        self.assertFalse(Book.objects.filter(pk=self.book1.pk).exists())
    
    def test_delete_book_unauthenticated(self):
        """
        Test that unauthenticated users cannot delete books.
        Expected: 403 Forbidden status.
        """
        self.unauthenticate_user()
        url = reverse('book-delete', kwargs={'pk': self.book1.pk})
        response = self.client.delete(url)
        
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Book.objects.count(), 3)  # Book still exists
    
    def test_login_functionality(self):
        """
        Test that self.client.login works correctly for authentication.
        """
        # Test login with correct credentials
        login_success = self.client.login(username='testuser', password='testpassword123')
        self.assertTrue(login_success)
        
        # Test login with wrong password
        login_failure = self.client.login(username='testuser', password='wrongpassword')
        self.assertFalse(login_failure)
        
        # Test login with non-existent user
        login_failure = self.client.login(username='nonexistent', password='testpassword123')
        self.assertFalse(login_failure)


class BookFilterSearchOrderTests(BookAPITestCase):
    """
    Test filtering, searching, and ordering functionalities.
    """
    
    def test_filter_books_by_author(self):
        """
        Test filtering books by author ID.
        Expected: Only books by specified author are returned.
        """
        url = reverse('book-list')
        response = self.client.get(url, {'author': self.author1.pk})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)  # Both Harry Potter books
        for book in response.data:
            self.assertEqual(book['author'], self.author1.pk)
    
    def test_filter_books_by_publication_year(self):
        """
        Test filtering books by publication year.
        Expected: Only books from specified year are returned.
        """
        url = reverse('book-list')
        response = self.client.get(url, {'publication_year': 1997})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'Harry Potter and the Philosopher\'s Stone')
    
    def test_search_books_by_title(self):
        """
        Test searching books by title text.
        Expected: Only books matching search query are returned.
        """
        url = reverse('book-list')
        response = self.client.get(url, {'search': 'Harry'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)  # Both Harry Potter books
        for book in response.data:
            self.assertIn('Harry', book['title'])
    
    def test_search_books_by_author_name(self):
        """
        Test searching books by author name.
        Expected: Only books by authors matching search query are returned.
        """
        url = reverse('book-list')
        response = self.client.get(url, {'search': 'Rowling'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)  # Both Harry Potter books
    
    def test_order_books_by_title_ascending(self):
        """
        Test ordering books by title in ascending order.
        Expected: Books are returned in alphabetical order by title.
        """
        url = reverse('book-list')
        response = self.client.get(url, {'ordering': 'title'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        titles = [book['title'] for book in response.data]
        self.assertEqual(titles, sorted(titles))
    
    def test_order_books_by_publication_year_descending(self):
        """
        Test ordering books by publication year in descending order.
        Expected: Books are returned from newest to oldest.
        """
        url = reverse('book-list')
        response = self.client.get(url, {'ordering': '-publication_year'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        publication_years = [book['publication_year'] for book in response.data]
        self.assertEqual(publication_years, sorted(publication_years, reverse=True))
    
    def test_combined_filter_search_order(self):
        """
        Test combining filtering, searching, and ordering in one request.
        Expected: Complex query returns correct filtered, searched, and ordered results.
        """
        url = reverse('book-list')
        response = self.client.get(url, {
            'author': self.author1.pk,
            'search': 'Harry',
            'ordering': '-publication_year'
        })
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)  # Both Harry Potter books by Rowling
        # Should be ordered by publication year descending
        self.assertEqual(response.data[0]['title'], 'Harry Potter and the Chamber of Secrets')  # 1998
        self.assertEqual(response.data[1]['title'], 'Harry Potter and the Philosopher\'s Stone')  # 1997


class BookValidationTests(BookAPITestCase):
    """
    Test data validation and error handling.
    """
    
    def test_create_book_with_future_publication_year(self):
        """
        Test that books cannot be created with future publication years.
        Expected: 400 Bad Request status with validation error.
        """
        # Use self.client.login for authentication
        self.client.login(username='testuser', password='testpassword123')
        url = reverse('book-create')
        future_year = datetime.now().year + 1
        data = {
            'title': 'Future Book',
            'publication_year': future_year,
            'author': self.author1.pk
        }
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('publication_year', response.data)
    
    def test_create_book_with_invalid_author(self):
        """
        Test that books cannot be created with non-existent author.
        Expected: 400 Bad Request status with validation error.
        """
        # Use self.client.login for authentication
        self.client.login(username='testuser', password='testpassword123')
        url = reverse('book-create')
        data = {
            'title': 'Book with Invalid Author',
            'publication_year': 2020,
            'author': 999  # Non-existent author ID
        }
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_retrieve_nonexistent_book(self):
        """
        Test retrieving a book that doesn't exist.
        Expected: 404 Not Found status.
        """
        url = reverse('book-detail', kwargs={'pk': 999})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class AuthenticationTests(BookAPITestCase):
    """
    Specific tests for authentication using self.client.login
    """
    
    def test_client_login_success(self):
        """
        Test that self.client.login works with correct credentials.
        """
        result = self.client.login(username='testuser', password='testpassword123')
        self.assertTrue(result)
    
    def test_client_login_failure_wrong_password(self):
        """
        Test that self.client.login fails with wrong password.
        """
        result = self.client.login(username='testuser', password='wrongpassword')
        self.assertFalse(result)
    
    def test_client_login_failure_wrong_username(self):
        """
        Test that self.client.login fails with wrong username.
        """
        result = self.client.login(username='wronguser', password='testpassword123')
        self.assertFalse(result)
    
    def test_access_protected_endpoint_after_login(self):
        """
        Test that protected endpoints work after successful login.
        """
        # Login first
        self.client.login(username='testuser', password='testpassword123')
        
        # Then access protected endpoint
        url = reverse('book-create')
        data = {
            'title': 'Book After Login',
            'publication_year': 2020,
            'author': self.author1.pk
        }
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class AuthorAPITests(APITestCase):
    """
    Test Author API endpoints for completeness.
    """
    
    def setUp(self):
        self.author = Author.objects.create(name='Test Author')
        self.client = APIClient()
    
    def test_list_authors(self):
        """
        Test retrieving list of authors.
        Expected: 200 OK status with author data.
        """
        url = reverse('author-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], 'Test Author')
    
    def test_retrieve_author_detail(self):
        """
        Test retrieving a single author's details.
        Expected: 200 OK status with author and nested books data.
        """
        url = reverse('author-detail', kwargs={'pk': self.author.pk})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Test Author')
        self.assertEqual(response.data['books'], [])  # No books for this author