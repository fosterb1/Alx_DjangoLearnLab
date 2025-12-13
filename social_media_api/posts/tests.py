from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from rest_framework.authtoken.models import Token
from .models import Post, Comment

User = get_user_model()

class PostModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        self.post = Post.objects.create(
            author=self.user,
            title='Test Post',
            content='This is a test post content'
        )

    def test_post_creation(self):
        self.assertEqual(self.post.title, 'Test Post')
        self.assertEqual(self.post.author, self.user)
        self.assertTrue(self.post.created_at)
        self.assertTrue(self.post.updated_at)

    def test_post_str(self):
        self.assertEqual(str(self.post), 'Test Post')

class CommentModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        self.post = Post.objects.create(
            author=self.user,
            title='Test Post',
            content='Test content'
        )
        self.comment = Comment.objects.create(
            post=self.post,
            author=self.user,
            content='Test comment'
        )

    def test_comment_creation(self):
        self.assertEqual(self.comment.post, self.post)
        self.assertEqual(self.comment.author, self.user)
        self.assertEqual(self.comment.content, 'Test comment')

class PostAPITest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user1 = User.objects.create_user(username='user1', password='pass123')
        self.user2 = User.objects.create_user(username='user2', password='pass123')
        self.token1 = Token.objects.create(user=self.user1)
        self.token2 = Token.objects.create(user=self.user2)

    def test_create_post_authenticated(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token1.key}')
        data = {'title': 'New Post', 'content': 'New content'}
        response = self.client.post('/api/posts/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Post.objects.count(), 1)
        self.assertEqual(response.data['author'], 'user1')

    def test_create_post_unauthenticated(self):
        data = {'title': 'New Post', 'content': 'New content'}
        response = self.client.post('/api/posts/', data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_list_posts(self):
        Post.objects.create(author=self.user1, title='Post 1', content='Content 1')
        Post.objects.create(author=self.user2, title='Post 2', content='Content 2')
        response = self.client.get('/api/posts/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)

    def test_update_own_post(self):
        post = Post.objects.create(author=self.user1, title='Original', content='Content')
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token1.key}')
        data = {'title': 'Updated', 'content': 'Updated content'}
        response = self.client.put(f'/api/posts/{post.id}/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        post.refresh_from_db()
        self.assertEqual(post.title, 'Updated')

    def test_update_others_post(self):
        post = Post.objects.create(author=self.user1, title='Original', content='Content')
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token2.key}')
        data = {'title': 'Updated', 'content': 'Updated content'}
        response = self.client.put(f'/api/posts/{post.id}/', data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_own_post(self):
        post = Post.objects.create(author=self.user1, title='To Delete', content='Content')
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token1.key}')
        response = self.client.delete(f'/api/posts/{post.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Post.objects.count(), 0)

    def test_delete_others_post(self):
        post = Post.objects.create(author=self.user1, title='To Delete', content='Content')
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token2.key}')
        response = self.client.delete(f'/api/posts/{post.id}/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_search_posts(self):
        Post.objects.create(author=self.user1, title='Django Tutorial', content='Learn Django')
        Post.objects.create(author=self.user1, title='Python Guide', content='Learn Python')
        response = self.client.get('/api/posts/?search=Django')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_filter_posts_by_author(self):
        Post.objects.create(author=self.user1, title='Post 1', content='Content 1')
        Post.objects.create(author=self.user2, title='Post 2', content='Content 2')
        response = self.client.get(f'/api/posts/?author={self.user1.id}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

class CommentAPITest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user1 = User.objects.create_user(username='user1', password='pass123')
        self.user2 = User.objects.create_user(username='user2', password='pass123')
        self.token1 = Token.objects.create(user=self.user1)
        self.token2 = Token.objects.create(user=self.user2)
        self.post = Post.objects.create(author=self.user1, title='Test Post', content='Content')

    def test_create_comment_authenticated(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token1.key}')
        data = {'post': self.post.id, 'content': 'Great post!'}
        response = self.client.post('/api/comments/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Comment.objects.count(), 1)

    def test_create_comment_unauthenticated(self):
        data = {'post': self.post.id, 'content': 'Great post!'}
        response = self.client.post('/api/comments/', data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_own_comment(self):
        comment = Comment.objects.create(post=self.post, author=self.user1, content='Original')
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token1.key}')
        data = {'post': self.post.id, 'content': 'Updated comment'}
        response = self.client.put(f'/api/comments/{comment.id}/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        comment.refresh_from_db()
        self.assertEqual(comment.content, 'Updated comment')

    def test_update_others_comment(self):
        comment = Comment.objects.create(post=self.post, author=self.user1, content='Original')
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token2.key}')
        data = {'post': self.post.id, 'content': 'Updated comment'}
        response = self.client.put(f'/api/comments/{comment.id}/', data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_filter_comments_by_post(self):
        post2 = Post.objects.create(author=self.user1, title='Post 2', content='Content 2')
        Comment.objects.create(post=self.post, author=self.user1, content='Comment 1')
        Comment.objects.create(post=post2, author=self.user1, content='Comment 2')
        response = self.client.get(f'/api/comments/?post={self.post.id}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
