from django.db import models

from api_yamdb.constant import LENGTH_256, LENGTH_150, LENGTH_50
from users.models import MyUser

CHOICES = ((score, score) for score in range(11))


class Category(models.Model):
    name = models.CharField(max_length=LENGTH_256)
    slug = models.SlugField(unique=True)

    class Meta:
        ordering = ['name']
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Genre(models.Model):
    name = models.CharField(max_length=LENGTH_256)
    slug = models.SlugField(unique=True, max_length=LENGTH_50)

    class Meta:
        ordering = ['name']
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(max_length=256)
    year = models.SmallIntegerField()
    category = models.ForeignKey(
        Category,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='categories',
    )
    genre = models.ManyToManyField(
        Genre,
        blank=True,
        related_name='genres',
    )
    description = models.CharField(
        max_length=LENGTH_256,
        null=True,
        blank=True
    )

    class Meta:
        ordering = ['name']
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.name


class Review(models.Model):
    text = models.TextField()
    author = models.ForeignKey(
        MyUser, on_delete=models.CASCADE, related_name='review_author'
    )
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE, related_name='title'
    )
    score = models.IntegerField(choices=CHOICES)
    pub_date = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True
    )

    def __str__(self):
        return self.text

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        ordering = ['title']
        constraints = [
            models.UniqueConstraint(
                fields=('author', 'title'),
                name='unique_author_title'
            )]


class Comment(models.Model):
    author = models.ForeignKey(
        MyUser, on_delete=models.CASCADE, related_name='comment_author'
    )
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name='review'
    )
    text = models.TextField()
    pub_date = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True)

    class Meta:
        ordering = ['-pub_date']
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return self.text
