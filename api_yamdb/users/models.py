from django.contrib.auth import get_user_model
from django.db import models
from django.contrib.auth.models import AbstractUser



class MyUser(AbstractUser):
    bio = models.TextField('Биография', blank=True)
    role = models.TextField('Статус пользователя')
