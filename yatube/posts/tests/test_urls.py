from http import HTTPStatus

from django.test import TestCase, Client
from django.contrib.auth import get_user_model

from ..models import Post, Group


class PostsURLTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.User_mod = get_user_model()
        cls.user = cls.User_mod.objects.create_user(username="TestUser1")
        cls.user2 = cls.User_mod.objects.create_user(username="TestUser2")

        group_cats = Group.objects.create(
            title="Cats",
            slug="cats",
            description="Cats group"
        )

        Post.objects.create(
            text="Тестовый текст",
            author=cls.user,
            group=group_cats,
        )

    def setUp(self):
        self.guest_client = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)
        self.authorized_client2 = Client()
        self.authorized_client2.force_login(self.user2)

    def test_pages_non_auth(self):
        """Страницы возвращают корректный статус для Гостя"""

        template_url_stat = {
            "/": HTTPStatus.OK.value,
            "/group/cats/": HTTPStatus.OK.value,
            "/profile/TestUser1/": HTTPStatus.OK.value,
            "/posts/1/": HTTPStatus.OK.value,
            "/unexist/": HTTPStatus.NOT_FOUND.value,
        }
        for url, stat in template_url_stat.items():
            with self.subTest(url=url):
                response = self.guest_client.get(url)
                self.assertEqual(response.status_code, stat)

    def test_pages_auth(self):
        """Страницы возвращают корректный статус для Авторизованного"""

        template_url_stat = {
            "/": HTTPStatus.OK.value,
            "/group/cats/": HTTPStatus.OK.value,
            "/profile/TestUser1/": HTTPStatus.OK.value,
            "/posts/1/": HTTPStatus.OK.value,
            "/posts/1/edit/": HTTPStatus.OK.value,
            "/create/": HTTPStatus.OK.value,
            "/unexist/": HTTPStatus.NOT_FOUND.value,
        }
        for url, stat in template_url_stat.items():
            with self.subTest(url=url):
                response = self.authorized_client.get(url)
                self.assertEqual(response.status_code, stat)

    def test_post_edit_non_auth(self):
        """Выполнен корректно редирект для Гостя со страницы post_edit"""
        response = self.guest_client.get("/posts/1/edit/", follow=True)
        self.assertRedirects(
            response, "/auth/login/?next=/posts/1/edit/")

    def test_post_det_auth_user2(self):
        """Выполнен корректно редирект для не Автора со страницы post_edit"""
        response = self.authorized_client2.get("/posts/1/edit/")
        self.assertRedirects(
            response, "/posts/1/")

    def test_post_create_non_auth(self):
        """Выполнен корректно редирект для Гостя со страницы post_create"""
        response = self.guest_client.get("/create/", follow=True)
        self.assertRedirects(
            response, "/auth/login/?next=/create/")

    def test_urls_uses_correct_template(self):
        """URL-адрес использует соответствующий шаблон."""
        templates_url_names = {
            "/": "posts/index.html",
            "/group/cats/": "posts/group_list.html",
            "/profile/TestUser1/": "posts/profile.html",
            "/posts/1/": "posts/post_detail.html",
            "/posts/1/edit/": "posts/create_post.html",
            "/create/": "posts/create_post.html",
        }
        for url, template in templates_url_names.items():
            with self.subTest(url=url):
                response = self.authorized_client.get(url)
                self.assertTemplateUsed(response, template)
