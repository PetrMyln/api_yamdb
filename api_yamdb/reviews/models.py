from django.contrib.auth import get_user_model
from django.db import models
from django.contrib.auth.models import AbstractUser



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
        related_name='category',
    )
    genge = models.ForeignKey(
        Genre,
        on_delete=models.CASCADE,
        related_name='genge',
    )

