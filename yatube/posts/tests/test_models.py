from django.test import TestCase
from django.contrib.auth import get_user_model

from ..models import Group, Post

User = get_user_model()

class PostModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='testuser')
        cls.group = Group.objects.create(title='Test Group', slug='test-group', description='Test description')
        cls.post = Post.objects.create(author=cls.user, text='T' * 30, )

    def test_models_have_correct_objects_names(self):
        post = PostModelTest.post
        self.assertEqual(str(post), 'T' * 15, 'Метод str работает не так как ожидалось для Post')

class GroupModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.group = Group.objects.create(title='Test Group', slug='test-group', description='Test description')

    def test_models_have_correct_objects_names(self):
        group = GroupModelTest.group
        self.assertEqual(str(group), 'Test Group', 'Метод str не работает правильно для Group')

