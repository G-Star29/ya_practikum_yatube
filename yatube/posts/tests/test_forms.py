from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from django import forms

from ..forms import PostForm
from ..models import Post

User = get_user_model()

class TestPostForm(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.form = PostForm()
        cls.user1 = User.objects.create_user(username='testuser')
        cls.post = Post.objects.create(author=cls.user1, text='T' * 30)

    def setUp(self):
        self.user2 = User.objects.create_user(username='testuser2')
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user2)

    def test_create_post(self):
        form_data = {
            'text': 'Z' * 30,
            'group': '',
        }
        posts_count = Post.objects.count()
        response = self.authorized_client.post(reverse('posts:post_create'), data=form_data, follow=True)
        self.assertRedirects(response, reverse('posts:profile', kwargs={'username': self.user2.username}))
        self.assertEqual(Post.objects.count(), posts_count + 1)
        self.assertTrue(Post.objects.filter(
            author=self.user2,
            text='Z' * 30,
            group=None
        ).exists())

