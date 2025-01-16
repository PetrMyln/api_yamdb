from django.db import models

from api_yamdb.constant import LENGTH_DISCRIPTION, CHOICES_SCORE
from users.models import User


class NameModel(models.Model):
    name = models.CharField(
        max_length=LENGTH_DISCRIPTION,
        verbose_name='Название'
    )

    class Meta:
        abstract = True
        ordering = ['name']

    def __str__(self):
        return self.name


class SlugModel(models.Model):
    slug = models.SlugField(
        unique=True,
        verbose_name='Слаг',
    )

    class Meta:
        abstract = True
        ordering = ['name']

    def __str__(self):
        return self.name


class TextAuthorDateModel(models.Model):
    text = models.TextField(verbose_name='Текст')
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор'
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
        verbose_name='Дата добавления'
    )

    class Meta:
        abstract = True
        ordering = ['-pub_date']

    def __str__(self):
        return self.text
