from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models

from api_yamdb.constant import LENGTH_150, LENGTH_254, LENGTH_50
from users.validators import validate_username


class User(AbstractUser):
    class Role(models.TextChoices):
        USER = 'user', 'Пользователь'
        MODERATOR = 'moderator', 'Модератор'
        ADMIN = 'admin', 'Администратор'

    username = models.CharField(
        max_length=LENGTH_150,
        unique=True,
        validators=(validate_username, UnicodeUsernameValidator())
    )
    email = models.EmailField(
        max_length=LENGTH_254,
        unique=True,
        verbose_name='Электронная почта',
        help_text='Укажите электронную почту'
    )
    role = models.CharField(
        max_length=LENGTH_50,
        choices=Role.choices,
        default=Role.USER,
        verbose_name='Роль',
        help_text='Выберите роль пользователя'
    )
    bio = models.TextField(
        blank=True,
        null=True,
        verbose_name='Биография',
        help_text='Напишите о себе'
    )

    def __str__(self):
        return self.username[:20]

    class Meta:
        ordering = ['username']
        verbose_name = 'Пользователь'

    @property
    def is_admin(self):
        return self.is_superuser or self.role == self.Role.ADMIN.value

    @property
    def is_moderator(self):
        return self.is_staff or self.role == self.Role.MODERATOR.value
