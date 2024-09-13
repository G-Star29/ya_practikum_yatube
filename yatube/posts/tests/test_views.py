from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from django import forms
from ..models import Post, Group
from ..views import index


User = get_user_model()

class PostsPagesTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='testuser')
        for i in range(13):
            Post.objects.create(
                author=cls.user,
                text='test',
            )
        Group.objects.create(
            title='testgroup',
            slug='testgroup',
        )

    def setUp(self):
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)


    def test_all_pages_use_correct_template(self):
        self.pk = Post.objects.all()[0].pk
        urls_templates = {
            'posts/index.html': reverse('posts:main_index'),
            'posts/group_list.html': reverse('posts:group_list', kwargs={'slug': 'testgroup'}),
            'posts/profile.html': reverse('posts:profile', kwargs={'username': 'testuser'}),
            'posts/post_detail.html': reverse('posts:post_detail', kwargs={'post_id': self.pk}),
            'posts/create_post.html': reverse('posts:post_edit', kwargs={'post_id': self.pk}),
            'posts/create_post.html': reverse('posts:post_create'),
        }
        for template, url in urls_templates.items():
            with self.subTest(url=url):
                response = self.authorized_client.get(url)
                self.assertTemplateUsed(response, template)

    def test_home_page_show_correct_context(self):
        response = self.authorized_client.get(reverse('posts:main_index'))
        posts = response.context['page_obj'].object_list[0].text
        self.assertEqual(posts, 'test')

    def test_post_detail_page_show_correct_context(self):
        self.pk = Post.objects.all()[0].pk
        response = self.authorized_client.get(reverse('posts:post_detail', kwargs={'post_id': self.pk}))
        post = response.context['post']
        self.assertEqual(post.pk, 1)

    def test_post_create_page_show_correct_context(self):
        response = self.authorized_client.get(reverse('posts:post_create'))
        form = {
            'text': forms.fields.CharField,
            'group': forms.fields.ChoiceField
        }
        for value, expected in form.items():
            with self.subTest(value=value):
                form_field = response.context.get('form').fields.get(value)
                self.assertIsInstance(form_field, expected)

    def test_post_cache_index(self):
        response = self.authorized_client.get(reverse('posts:main_index'))
        posts = response.context['page_obj'].object_list
        Post.objects.create(
            text='test',
            author=self.user,
        )
        response_new = self.authorized_client.get(reverse('posts:main_index'))
        posts_new = response_new.context['page_obj'].object_list
        print(f'{posts.count()} {posts_new.count()}')
        self.assertNotEqual(posts, posts_new)