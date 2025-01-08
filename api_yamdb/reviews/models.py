from django.db import models
from django.contrib.auth import get_user_model

CHOICES = ((score, score) for score in range(11))

User = get_user_model()
Title = get_user_model()


class Review(models.Model):
    """Модель отзывов."""
    text = models.TextField()
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='review_author'
    )  # Заменить модель пользователя
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE, related_name='title'
    )  # Добавить модель произведения
    score = models.IntegerField(choices=CHOICES)
    pub_date = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True
    )


class Comment(models.Model):
    """Модель комментариев."""
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comment_author'
    )
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name='review'
    )
    text = models.TextField()
    created = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True)
