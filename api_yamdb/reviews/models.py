from django.db import models

from users.models import MyUser

CHOICES = ((score, score) for score in range(11))


class Categories(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)


class Genre(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)


class Titles(models.Model):
    name = models.CharField(max_length=200)
    year = models.DateTimeField(
        'Дата выхода')
    category = models.ForeignKey(
        Categories,
        on_delete=models.CASCADE,
        related_name='categorys',
    )
    genge = models.ForeignKey(
        Genre,
        on_delete=models.CASCADE,
        related_name='genges',
    )


class Review(models.Model):
    """Модель отзывов."""
    text = models.TextField()
    author = models.ForeignKey(
        MyUser, on_delete=models.CASCADE, related_name='review_author'
    ) 
    title = models.ForeignKey(
        Titles, on_delete=models.CASCADE, related_name='title'
    ) 
    score = models.IntegerField(choices=CHOICES)
    pub_date = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True
    )


class Comment(models.Model):
    """Модель комментариев."""
    author = models.ForeignKey(
        MyUser, on_delete=models.CASCADE, related_name='comment_author'
    )
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name='review'
    )
    text = models.TextField()
    created = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True)
