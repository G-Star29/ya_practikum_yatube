from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from ..models import Post, Group

User = get_user_model()

class PostsURLTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='testuser')
        Post.objects.create(
            text='Test Post',
            author=cls.user,
        )
        Group.objects.create(
            title='Test Group',
            slug='test-group',
        )


    def setUp(self):
        self.guest_client = Client()
        self.user = User.objects.create_user(username='NoName')
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)
        self.pk_post = Post.objects.get(text='Test Post').pk

    def test_post_urls_free_for_no_auth_users(self):
        urls = ['/',
                f'/profile/{self.user.username}/',
                f'/posts/{str(self.pk_post)}/',
        ]
        for url in urls:
            with self.subTest(url=url):
                response = self.guest_client.get(url)
                self.assertEqual(response.status_code, 200)

    def test_post_urls_auth_for_no_auth_users(self):
        urls = [f'/posts/{str(self.pk_post)}/edit',]
        for url in urls:
            with self.subTest(url=url):
                response = self.guest_client.get(url)
                self.assertEqual(response.status_code, 301)


