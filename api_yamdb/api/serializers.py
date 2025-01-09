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
            'bio',
            'role',
        )


class TitlesSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('id', 'name', 'year', 'category', 'genge',)
        model = Titles


class CategoriesSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('id', 'name', 'slug')
        model = Categories


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
        fields = ('id', 'text', 'author', 'created')
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
