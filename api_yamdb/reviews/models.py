from django.db import models

# Create your models here.
class Group(models.Model):
    """Модель групп."""
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField()

    def __str__(self):
        return self.title
