from api_yamdb.constant import (LENGTH_ROLE, LENGTH_SHOW_NAME, LENGTH_TEXT,
                                LENGTH_USERNAME)
from api_yamdb.validators import validate_username
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models


class User(AbstractUser):
    class Role(models.TextChoices):
        USER = 'user', 'Пользователь'
        MODERATOR = 'moderator', 'Модератор'
        ADMIN = 'admin', 'Администратор'

    username = models.CharField(
        max_length=LENGTH_USERNAME,
        unique=True,
        verbose_name='Username аккаунта',
        validators=(validate_username, UnicodeUsernameValidator())
    )
    email = models.EmailField(
        max_length=LENGTH_TEXT,
        unique=True,
        verbose_name='Электронная почта',
        help_text='Укажите электронную почту'
    )
    role = models.CharField(
        max_length=LENGTH_ROLE,
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

    class Meta:
        ordering = ['id']
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username[:LENGTH_SHOW_NAME]

    @property
    def is_admin(self):
        return self.is_superuser or self.role == self.Role.ADMIN.value

    @property
    def is_moderator(self):
        return self.is_staff or self.role == self.Role.MODERATOR.value
