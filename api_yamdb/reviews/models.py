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
        ordering = ['-id']
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(max_length=256)
    year = models.IntegerField()
    category = models.ForeignKey(
        Categories,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='categorys',
    )
    genre = models.ManyToManyField(
        Genre,
        blank=True,
        related_name='genres',
    )
    description = models.CharField(
        max_length=256,
        null=True,
        blank=True
    )

    class Meta:
        ordering = ['-id']
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'
    def __str__(self):
        return self.name


class Review(models.Model):
    """Модель отзывов."""
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


"""class GenreTitle(models.Model):
    title = models.ForeignKey(Title, on_delete=models.CASCADE)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.title} {self.genre}'"""