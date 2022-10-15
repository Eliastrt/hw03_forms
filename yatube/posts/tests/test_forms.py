from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.shortcuts import get_object_or_404

from datetime import datetime as dt

from ..models import Post, Group


class PostsFormTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.User_mod = get_user_model()
        cls.user = cls.User_mod.objects.create_user(username="TestUser1")

        cls.dt_now = dt.utcnow()
        cls.test_text = "Тестовый текст"
        cls.test_edit_text = "Скорректированный тестовый текст"
        cls.group_cats = Group.objects.create(
            title="Cats",
            slug="cats",
            description="Cats group"
        )
        cls.group_dogs = Group.objects.create(
            title="Dogs",
            slug="dogs",
            description="Dogs group"
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

    def test_create_post(self):
        """Форма create_post создала корректный экземпляр."""

        posts_count = Post.objects.count()
        form_data = {
            "text": self.test_text,
            "group": self.group_dogs.id,
        }
        response = self.authorized_client.post(
            reverse("posts:post_create"),
            data=form_data,
            follow=True
        )

        post_0 = response.context["post_det"][0]

        self.assertRedirects(
            response,
            reverse("posts:profile", kwargs={"username": "TestUser1"}))
        self.assertEqual(Post.objects.count(), posts_count + 1)
        self.assertEqual(post_0.author, self.user)
        self.assertEqual(post_0.group, self.group_dogs)
        self.assertEqual(post_0.text, self.test_text)
        self.assertTrue(
            Post.objects.filter(
                text=self.test_text,
                author=self.user,
                group=self.group_dogs.id
            ).exists()
        )

    def test_edit_post(self):
        """Форма edit_post корректно изменила экземпляр."""
        test_post_id = 1
        post_before = get_object_or_404(Post, id=test_post_id)

        form_data = {
            "text": self.test_edit_text,
            "group": self.group_dogs.id,
        }

        response = self.authorized_client.post(
            reverse("posts:post_edit", kwargs={"post_id": post_before.id}),
            data=form_data,
            follow=True
        )

        post_0 = response.context["post_det"]

        self.assertRedirects(
            response,
            reverse("posts:post_detail", kwargs={"post_id": test_post_id}))
        self.assertEqual(post_0.text, self.test_edit_text)
        self.assertEqual(dt.date(post_0.pub_date), dt.date(self.dt_now))
        self.assertEqual(post_0.author, self.user)
        self.assertEqual(post_0.group, self.group_dogs)

        response2 = self.authorized_client.get(reverse("posts:group_list",
                                                       kwargs={
                                                          "slug": "cats"}
                                                       )
                                               )

        for post in response2.context["page_obj"]:
            self.assertNotEqual(post.pk, test_post_id)

        response3 = self.authorized_client.get(
            reverse("posts:group_list",
                    kwargs={
                        "slug": "cats"}
                    ) + "?page=2")

        for post in response3.context["page_obj"]:
            self.assertNotEqual(post.pk, test_post_id)
