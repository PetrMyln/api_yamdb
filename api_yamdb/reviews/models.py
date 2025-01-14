from django.contrib import admin
from django.core.validators import MaxValueValidator
from django.db import models

from api_yamdb.constant import CHOICES, LENGTH_256, LENGTH_150, LENGTH_50

from api_yamdb.validators import date_year
from users.models import MyUser


class BaseTitleModel(models.Model):
    name = models.CharField(max_length=LENGTH_256)

    class Meta:
        abstract = True
        ordering = ['name']

    def __str__(self):
        return self.name


class BaseReviewModel(models.Model):
    text = models.TextField()
    pub_date = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True
    )

    class Meta:
        abstract = True
        ordering = ['-pub_date']

    def __str__(self):
        return self.text


class Category(BaseTitleModel):
    slug = models.SlugField(unique=True)

    class Meta(BaseTitleModel.Meta):
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Genre(BaseTitleModel):
    slug = models.SlugField(unique=True, max_length=LENGTH_50)

    class Meta(BaseTitleModel.Meta):
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'


class Title(BaseTitleModel):
    year = models.SmallIntegerField(
        validators=[MaxValueValidator(date_year())]
    )
    category = models.ForeignKey(
        Category,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    genre = models.ManyToManyField(
        Genre,
        blank=True,
    )
    description = models.CharField(
        max_length=LENGTH_256,
        null=True,
        blank=True
    )

    class Meta(BaseTitleModel.Meta):
        default_related_name = 'titles'
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'


class Review(BaseReviewModel):
    author = models.ForeignKey(
        MyUser, on_delete=models.CASCADE, related_name='review_authors'
    )
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE, related_name='titles'
    )
    score = models.IntegerField(choices=CHOICES)

    class Meta(BaseReviewModel.Meta):
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        constraints = [
            models.UniqueConstraint(
                fields=('author', 'title'),
                name='unique_author_title'
            )]


class Comment(BaseReviewModel):
    author = models.ForeignKey(
        MyUser, on_delete=models.CASCADE, related_name='comment_authors'
    )
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name='reviews'
    )

    class Meta(BaseReviewModel.Meta):
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
