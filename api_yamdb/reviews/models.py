from django.db import models

from api_yamdb.constant import LENGTH_DISCRIPTION, CHOICES_SCORE
from api_yamdb.validators import date_year

from reviews.core import NameModel, TextAuthorDateModel, SlugModel


class Category(SlugModel):
    slug = models.SlugField(
        unique=True,
        verbose_name='Слаг',
    )

    class Meta(SlugModel.Meta):
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Genre(SlugModel):
    slug = models.SlugField(
        unique=True,
        verbose_name='Слаг',
    )

    class Meta(SlugModel.Meta):
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'


class Title(NameModel):
    year = models.SmallIntegerField(
        validators=[date_year],
        verbose_name='Год выхода'
    )
    category = models.ForeignKey(
        Category,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        verbose_name='Категория'
    )
    genre = models.ManyToManyField(
        Genre,
        blank=True,
        verbose_name='Жанр/Жанры'
    )
    description = models.CharField(
        max_length=LENGTH_DISCRIPTION,
        null=True,
        blank=True,
        verbose_name='Описание'
    )

    class Meta(NameModel.Meta):
        default_related_name = 'titles'
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'


class Review(TextAuthorDateModel):
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
    )
    score = models.IntegerField(
        choices=CHOICES_SCORE,
        verbose_name='Рейтинг',
    )

    class Meta(TextAuthorDateModel.Meta):
        default_related_name = 'reviews'
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        constraints = [
            models.UniqueConstraint(
                fields=('author', 'title'),
                name='unique_author_title'
            )]


class Comment(TextAuthorDateModel):
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE,
        verbose_name='Отзыв',
    )

    class Meta(TextAuthorDateModel.Meta):
        default_related_name = 'comments'
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'


