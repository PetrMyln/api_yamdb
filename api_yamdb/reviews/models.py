from django.core.validators import MaxValueValidator
from django.db import models

from api_yamdb.constant import LENGTH_256, LENGTH_50, CHOICES_SCORE
from api_yamdb.validators import date_year
from users.models import User


class BaseTitleModel(models.Model):
    name = models.CharField(
        max_length=LENGTH_256,
        verbose_name='Название'
    )

    class Meta:
        abstract = True
        ordering = ['name']

    def __str__(self):
        return self.name


class BaseReviewModel(models.Model):
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


class Category(BaseTitleModel):
    slug = models.SlugField(
        unique=True,
        verbose_name='Слаг',
    )

    class Meta(BaseTitleModel.Meta):
        default_related_name = 'categories'
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Genre(BaseTitleModel):
    slug = models.SlugField(
        unique=True,
        max_length=LENGTH_50,
        verbose_name='Слаг',
    )

    class Meta(BaseTitleModel.Meta):
        default_related_name = 'genres'
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'


class Title(BaseTitleModel):
    year = models.SmallIntegerField(
        validators=[MaxValueValidator(date_year())],
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
        max_length=LENGTH_256,
        null=True,
        blank=True,
        verbose_name='Описание'
    )

    class Meta(BaseTitleModel.Meta):
        default_related_name = 'titles'
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'


class Review(BaseReviewModel):
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
    )
    score = models.IntegerField(
        choices=CHOICES_SCORE,
        verbose_name='Рейтинг',
    )

    class Meta(BaseTitleModel.Meta):
        ordering = ['-pub_date']
        default_related_name = 'reviews'
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        constraints = [
            models.UniqueConstraint(
                fields=('author', 'title'),
                name='unique_author_title'
            )]


class Comment(BaseReviewModel):
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE,
        verbose_name='Отзыв',
    )

    class Meta(BaseTitleModel.Meta):
        ordering = ['-pub_date']
        default_related_name = 'comments'
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
