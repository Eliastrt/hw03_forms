from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from django import forms

from datetime import datetime as dt

from ..models import Post, Group


class PostsViewTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.User_mod = get_user_model()
        cls.user = cls.User_mod.objects.create_user(username="TestUser1")

        cls.dt_now = dt.utcnow()
        cls.test_text = "Тестовый текст"
        cls.grp_cat_title = "Cats"
        cls.grp_cat_slug = "cats"
        cls.grp_cat_description = "Cats group"

        cls.group_cats = Group.objects.create(
            title=cls.grp_cat_title,
            slug=cls.grp_cat_slug,
            description=cls.grp_cat_description
        )

        for i in range(15):
            Post.objects.create(
                text=cls.test_text,
                author=cls.user,
                group=cls.group_cats,
            )

    def setUp(self):
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_pages_uses_correct_template(self):
        """URL-адрес использует соответствующий шаблон."""
        templates_page_names = {
            reverse('posts:index'): 'posts/index.html',
            reverse('posts:group_list', kwargs={'slug': 'cats'}):
                'posts/group_list.html',
            reverse('posts:profile', kwargs={'username': 'TestUser1'}):
                'posts/profile.html',
            reverse('posts:post_detail', kwargs={'post_id': '1'}):
                'posts/post_detail.html',
            reverse('posts:post_edit', kwargs={'post_id': '1'}):
                'posts/create_post.html',
            reverse('posts:post_create'): 'posts/create_post.html',
        }

        for reverse_name, template in templates_page_names.items():
            with self.subTest(template=template):
                response = self.authorized_client.get(reverse_name)
                self.assertTemplateUsed(response, template)

    def test_index_show_correct_context(self):
        """Шаблон index сформирован с правильным контекстом."""
        response = self.authorized_client.get(reverse("posts:index"))
        response2 = self.authorized_client.get(
            reverse("posts:index") + "?page=2")

        post_0 = response.context["page_obj"][0]

        self.assertEqual(post_0.text, self.test_text)
        self.assertEqual(dt.date(post_0.pub_date), dt.date(self.dt_now))
        self.assertEqual(post_0.author, self.user)
        self.assertEqual(post_0.group, self.group_cats)
        self.assertEqual(len(response.context["page_obj"]), 10)
        self.assertEqual(len(response2.context["page_obj"]), 5)

    def test_group_show_correct_context(self):
        """Шаблон group_list сформирован с правильным контекстом."""
        response = self.authorized_client.get(reverse("posts:group_list",
                                                      kwargs={
                                                          "slug": "cats"}
                                                      ))
        response2 = self.authorized_client.get(
            reverse("posts:group_list",
                    kwargs={
                        'slug': "cats"}
                    ) + "?page=2")

        post_0 = response.context["page_obj"][0]
        group_0 = response.context["group"]

        self.assertEqual(post_0.text, self.test_text)
        self.assertEqual(dt.date(post_0.pub_date), dt.date(self.dt_now))
        self.assertEqual(post_0.author, self.user)
        self.assertEqual(post_0.group, self.group_cats)
        self.assertEqual(group_0.title, self.grp_cat_title)
        self.assertEqual(group_0.slug, self.grp_cat_slug)
        self.assertEqual(group_0.description, self.grp_cat_description)
        self.assertEqual(len(response.context["page_obj"]), 10)
        self.assertEqual(len(response2.context["page_obj"]), 5)

    def test_profile_show_correct_context(self):
        """Шаблон profile сформирован с правильным контекстом."""
        response = self.authorized_client.get(
            reverse("posts:profile",
                    kwargs={"username": "TestUser1"}
                    ))
        response2 = self.authorized_client.get(
            reverse("posts:profile",
                    kwargs={"username": "TestUser1"}
                    ) + "?page=2")

        post_0 = response.context["page_obj"][0]
        author_0 = response.context["author"]

        self.assertEqual(post_0.text, self.test_text)
        self.assertEqual(dt.date(post_0.pub_date), dt.date(self.dt_now))
        self.assertEqual(post_0.author, self.user)
        self.assertEqual(post_0.group, self.group_cats)
        self.assertEqual(author_0.username, self.user.username)
        self.assertEqual(len(response.context["page_obj"]), 10)
        self.assertEqual(len(response2.context["page_obj"]), 5)

    def test_post_det_show_correct_context(self):
        """Шаблон post_detail сформирован с правильным контекстом."""
        response = self.authorized_client.get(
            reverse("posts:post_detail",
                    kwargs={"post_id": "15"}))

        post_0 = response.context["post_det"]

        self.assertEqual(post_0.text, self.test_text)
        self.assertEqual(dt.date(post_0.pub_date), dt.date(self.dt_now))
        self.assertEqual(post_0.author, self.user)
        self.assertEqual(post_0.group, self.group_cats)

    def test_post_edit_show_correct_context(self):
        """Шаблон post_edit сформирован с правильным контекстом."""
        response = self.authorized_client.get(
            reverse("posts:post_edit",
                    kwargs={"post_id": "15"}))

        post_0 = response.context["form"]
        is_edit_flag = response.context["is_edit"]

        self.assertEqual(post_0.text, self.test_text)
        self.assertEqual(dt.date(post_0.pub_date), dt.date(self.dt_now))
        self.assertEqual(post_0.author, self.user)
        self.assertEqual(post_0.group, self.group_cats)
        self.assertEqual(is_edit_flag, "edit")

        form_fields = {
            "text": forms.fields.CharField,
            "group": forms.fields.ChoiceField,
        }

        for value, expected in form_fields.items():
            with self.subTest(value=value):
                form_field = response.context.get("form").fields.get(value)
                self.assertIsInstance(form_field, expected)

    def test_post_create_show_correct_context(self):
        """Шаблон post_create сформирован с правильным контекстом."""
        response = self.authorized_client.get(
            reverse("posts:post_create"))

        is_edit_flag = response.context["is_edit"]

        self.assertEqual(is_edit_flag, "create")

        form_fields = {
            "text": forms.fields.CharField,
            "group": forms.fields.ChoiceField,
        }

        for value, expected in form_fields.items():
            with self.subTest(value=value):
                form_field = response.context.get("form").fields.get(value)
                self.assertIsInstance(form_field, expected)
