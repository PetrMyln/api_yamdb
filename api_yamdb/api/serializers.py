from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import IntegrityError
from django.shortcuts import get_object_or_404
from rest_framework import serializers

from api_yamdb.constant import LENGTH_254, LENGTH_150
from reviews.models import (
    Category,
    Comment,
    Genre,
    MyUser,
    Review,
    Title,
)
from users.validators import validate_username


class AuthSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True, max_length=LENGTH_254)
    username = serializers.CharField(required=True, max_length=LENGTH_150,
                                     validators=(validate_username,
                                                 UnicodeUsernameValidator()))

    def validate(self, data):
        try:
            MyUser.objects.get_or_create(
                # ANTON
                # Метод validate ничего создавать не должен, его задача п
                # роверять валидность данных. За создание в сериализаторе
                # отвечает метод create.
                username=data.get('username'),
                email=data.get('email')
            )
        except IntegrityError:
            raise serializers.ValidationError(
                'Username или email уже используется кем-то другим!'
            )
        return data


class TokenSerializer(serializers.Serializer):
    # ANTON
    # Использовать приставку Custom в неймингах - плохой тон.
    # Так же как и My. Все переменные/функции/классы/модули "кастомные" и
    # "твои", лишний раз об этом говорить не стоит.
    username = serializers.CharField()
    confirmation_code = serializers.CharField()


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
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
        # DEN
        # Сверяемся со спецификацией, вывод не соответствует ТЗ.
        fields = ('id', 'text', 'author', 'title', 'score', 'pub_date')
        model = Review
        read_only_fields = ('title',)

    def validate(self, attrs):
        author = self.context['request'].user.pk
        title_id = self.context['request'].parser_context['kwargs'].get(
            'title_id')
        title_obj = get_object_or_404(Title, id=title_id)
        rule_obj_exists = title_obj.title.filter(author=author).exists()
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
