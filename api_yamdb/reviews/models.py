from django.core.validators import MaxValueValidator
from django.db import models

from api_yamdb.constant import CHOICES, LENGTH_256, LENGTH_150, LENGTH_50
from api_yamdb.validators import date_year
from users.models import MyUser


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
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Genre(BaseTitleModel):
    slug = models.SlugField(
        unique=True,
        max_length=LENGTH_50,
        verbose_name='Слаг',
    )

    class Meta(BaseTitleModel.Meta):
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
    author = models.ForeignKey(
        MyUser,
        on_delete=models.CASCADE,
        related_name='review_authors',
        verbose_name='Автор'
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='titles',
        verbose_name='Произведение',
    )
    score = models.IntegerField(
        choices=CHOICES,
        verbose_name='Рейтинг',
    )

    class Meta(BaseTitleModel.Meta):
        ordering = ['-pub_date']
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        constraints = [
            models.UniqueConstraint(
                fields=('author', 'title'),
                name='unique_author_title'
            )]


class Comment(BaseReviewModel):
    author = models.ForeignKey(
        MyUser,
        on_delete=models.CASCADE,
        related_name='comment_authors',
    )
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name='reviews'
    )

    class Meta(BaseTitleModel.Meta):
        ordering = ['-pub_date']
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
