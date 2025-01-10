from django.db import models


from users.models import MyUser

CHOICES = ((score, score) for score in range(11))




class Categories(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(unique=True, default='empty')

    class Meta:
        ordering = ['-id']
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'




class Genre(models.Model):
    name = models.CharField(max_length=150)
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.name


class Titles(models.Model):
    name = models.CharField(max_length=150)
    year = models.IntegerField()
    category = models.ForeignKey(
        Categories,
        on_delete=models.CASCADE,
        related_name='categorys',
    )
    genre = models.ManyToManyField(
        Genre,
        related_name='genres',
    )

    class Meta:
        verbose_name = 'Название'

    def __str__(self):
        return self.name


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

    def __str__(self):
        return self.text

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'

class Comment(models.Model):
    """Модель комментариев."""
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
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return self.text
