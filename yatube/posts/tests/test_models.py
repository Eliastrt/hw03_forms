from django.contrib.auth import get_user_model
from django.test import TestCase

from ..models import Group, Post

User = get_user_model()


class PostModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='auth')
        cls.group = Group.objects.create(
            title="Тестовая группа",
            slug="Тестовый слаг",
            description="Тестовое описание",
        )

        cls.post = Post.objects.create(
            author=cls.user,
            text="Тестовый текст.Тестовый текст.Тестовый текст.",
        )

    def test_models_have_correct_object_names(self):
        """Проверяем, что у моделей корректно работает __str__."""
        """__str__  post - это строчка с содержимым post.text:15."""
        post = self.post
        group = self.group
        field_str = {
            post.text[:15]: str(post),
            group.title: str(group),
        }
        for expected_object_name, expected in field_str.items():
            self.assertEqual(expected_object_name, expected)

    def test_verbose_name(self):
        """verbose_name в полях совпадает с ожидаемым."""
        post = PostModelTest.post
        field_verboses = {
            "text": "Post's description",
            "pub_date": "Post's pub_date",
            "author": "Post's author",
            "group": "Post's group",
        }
        for field, expected_value in field_verboses.items():
            with self.subTest(field=field):
                self.assertEqual(
                    post._meta.get_field(field).verbose_name,
                    expected_value)

        group = PostModelTest.group
        field_verboses = {
            "title": "Group's title",
            "slug": "Group's slug",
            "description": "Group's description",
        }
        for field, expected_value in field_verboses.items():
            with self.subTest(field=field):
                self.assertEqual(
                    group._meta.get_field(field).verbose_name,
                    expected_value)

    def test_help_text(self):
        """help_text в полях совпадает с ожидаемым."""
        post = PostModelTest.post
        field_help_texts = {
            "text": "Введите текст поста",
        }
        for field, expected_value in field_help_texts.items():
            with self.subTest(field=field):
                self.assertEqual(
                    post._meta.get_field(field).help_text, expected_value)
