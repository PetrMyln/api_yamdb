from rest_framework import serializers

from reviews.models import (
    Comment,
    Review,
    MyUser,
    Categories,
    Titles,
    Genre
)


class MyUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = (
            'id',
            'username',
            'first_name',
            'last_name',
            'email',
            'bio',
            'role',
        )


class TitlesSerializer(serializers.ModelSerializer):
    score = serializers.SerializerMethodField()

    class Meta:
        fields = ('id', 'name', 'year', 'category', 'genre', 'score')
        model = Titles

    def get_score(self, obj):
        total_score = 0
        total_reviews = 0
        for review in Review.objects.filter(title_id=obj.id):
            total_reviews += 1
            total_score += int(review.score)
        if total_reviews == 0:
            return "Обзоров на это произведение еще нет"
        return round(total_score / total_reviews)



class CategoriesSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('name', 'slug')
        model = Categories
        ordering = ['-id']

    def validate(self,data):
        if "name" not in data or "slug" not in data:
            return False
        return data





class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('id', 'name', 'slug')
        model = Genre


class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор для модели комментариев."""
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        fields = ('id', 'text', 'author', 'pub_date')
        model = Comment


class ReviewSerializer(serializers.ModelSerializer):
    """Сериализатор для модели комментариев."""
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        fields = ('id', 'text', 'author', 'title', 'score', 'pub_date')
        model = Review
        read_only_fields = ('title',)
