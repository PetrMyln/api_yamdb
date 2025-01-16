from django.contrib.auth.validators import UnicodeUsernameValidator
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from django.contrib.auth.tokens import default_token_generator

from api_yamdb.constant import LENGTH_254, LENGTH_150
from reviews.models import (
    Category,
    Comment,
    Genre,
    User,
    Review,
    Title,
)
from users.validators import validate_username


class AuthSerializer(serializers.Serializer):
    email = serializers.EmailField(
        required=True,
        max_length=LENGTH_254
    )
    username = serializers.CharField(
        required=True,
        max_length=LENGTH_150,
        validators=(
            validate_username,
            UnicodeUsernameValidator())
    )

    def validate(self, data):
        username = data.get('username')
        email = data.get('email')
        rule_username = User.objects.filter(username=username).exists()
        rule_email = User.objects.filter(email=email).exists()
        if rule_username == rule_email:
            return data
        ans_error = (email, username)[rule_username]
        raise serializers.ValidationError(
            f'Проверьте {ans_error} уже используется!')


class TokenSerializer(serializers.Serializer):
    username = serializers.CharField()
    confirmation_code = serializers.CharField()

    def validate(self, data):
        user = get_object_or_404(
            User, username=data.get('username'))
        if not default_token_generator.check_token(
                user,
                data.get('confirmation_code')):
            raise serializers.ValidationError(
                'Неверный confirmation_code')
        return data


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'role',
            'first_name',
            'last_name',
            'bio',
        )


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('name', 'slug')
        model = Category


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('name', 'slug')
        model = Genre


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        fields = ('id', 'text', 'author', 'pub_date')
        model = Comment


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        fields = ('id', 'text', 'author', 'score', 'pub_date')
        model = Review

    def validate(self, attrs):
        author = self.context['request'].user.pk
        title_id = self.context['request'].parser_context['kwargs'].get(
            'title_id')
        title_obj = get_object_or_404(Title, id=title_id)
        rule_obj_exists = title_obj.reviews.filter(author=author).exists()
        rule_request = self.context['request'].method
        if rule_request == 'POST' and rule_obj_exists:
            raise serializers.ValidationError(
                f'Создать повтороно отзыв {title_obj.name} невозможно'
            )
        return super().validate(attrs)


class TitlesSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    genre = GenreSerializer(many=True)
    rating = serializers.FloatField()

    class Meta:
        fields = ('id',
                  'name',
                  'year',
                  'rating',
                  'description',
                  'genre',
                  'category',)
        model = Title


class TitleSerializersCreateUpdate(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all(),
    )

    genre = serializers.SlugRelatedField(
        slug_field='slug',
        many=True,
        queryset=Genre.objects.all(),
        required=True,
    )

    def validate_genre(self, value):
        if not value:
            return serializers.ValidationError({
                'Ошибка': 'Необходимо указать жанр произведения.'
            })
        return value

    class Meta:
        fields = ('id',
                  'name',
                  'year',
                  'description',
                  'genre',
                  'category',)
        model = Title
