from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Author, Post, Comment


class BlogApiTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="password123")
        self.author = Author.objects.create(user=self.user, bio="Test Bio")
        self.post = Post.objects.create(author=self.author, title="Test Title", content="Test Content")

    def test_health_endpoint(self):
        url = reverse("health")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {"status": "healthy"})

    def test_readiness_endpoint(self):
        url = reverse("readiness")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {"status": "ready"})

    def test_get_posts(self):
        url = reverse("posts")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_create_post_authenticated(self):
        self.client.force_authenticate(user=self.user)
        url = reverse("posts")
        data = {"title": "New Post", "content": "New Content"}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Post.objects.count(), 2)

    def test_get_post_comments(self):
        Comment.objects.create(post=self.post, author=self.author, content="Comment 1")
        url = reverse("post-comments", kwargs={"post_id": self.post.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_create_comment_authenticated(self):
        self.client.force_authenticate(user=self.user)
        url = reverse("post-comments", kwargs={"post_id": self.post.id})
        data = {"content": "New Comment"}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Comment.objects.count(), 1)

