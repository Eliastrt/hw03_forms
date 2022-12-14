from django.db import models
from django.contrib.auth import get_user_model

from .constants import POSTS_TEXT_LIM


User = get_user_model()


class Group(models.Model):
    title = models.CharField("Group's title", max_length=200)
    slug = models.SlugField("Group's slug", unique=True)
    description = models.TextField("Group's description")

    class Meta:
        verbose_name = "Group"
        verbose_name_plural = "Groups"
        default_related_name = "group"

    def __str__(self):
        return self.title


class Post(models.Model):
    text = models.TextField(verbose_name="Post's description",
                            help_text="Введите текст поста")
    pub_date = models.DateTimeField(verbose_name="Post's pub_date",
                                    auto_now_add=True)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="posts",
        verbose_name="Post's author"
    )

    group = models.ForeignKey(
        Group,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="posts",
        verbose_name="Post's group"
    )

    class Meta:
        ordering = ("-id",)
        verbose_name = "Post"
        verbose_name_plural = "Posts"

    def __str__(self):
        return self.text[:POSTS_TEXT_LIM]
