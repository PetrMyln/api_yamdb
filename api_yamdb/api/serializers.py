from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import IntegrityError
from django.shortcuts import get_object_or_404
from rest_framework import serializers

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
    email = serializers.EmailField(required=True, max_length=254)
    username = serializers.CharField(required=True, max_length=150,
                                     validators=(validate_username,
                                                 UnicodeUsernameValidator()))

    def validate(self, data):
        try:
            MyUser.objects.get_or_create(
                username=data.get('username'),
                email=data.get('email')
            )
        except IntegrityError:
            raise serializers.ValidationError(
                'Username или email уже используется кем-то другим!'
            )
        return data


class TokenSerializer(serializers.Serializer):
    username = serializers.CharField()
    confirmation_code = serializers.CharField()


class MyUserSerializer(serializers.ModelSerializer):
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
        # ordering = ['-id']


class CategoryField(serializers.SlugRelatedField):
    def to_representation(self, value):
        serializer = CategorySerializer(value)
        return serializer.data


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
    rating = serializers.SerializerMethodField()

    class Meta:
        fields = ('id',
                  'name',
                  'year',
                  'description',
                  'rating',
                  'genre',
                  'category',)

        model = Title

    def get_rating(self, obj):
        total_rating = 0
        total_reviews = 0
        for review in Review.objects.filter(title_id=obj.id):
            total_reviews += 1
            total_rating += int(review.score)
        if total_reviews == 0:
            return None
        return round(total_rating / total_reviews)


class TitleSerializersCreateUpdate(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all(),
    )

    genre = serializers.SlugRelatedField(
        slug_field='slug',
        many=True,
        queryset=Genre.objects.all(),
    )
    rating = serializers.SerializerMethodField()

    class Meta:
        fields = ('id',
                  'name',
                  'year',
                  'description',
                  'rating',
                  'genre',
                  'category',)
        model = Title

    def get_rating(self, obj):
        total_rating = 0
        total_reviews = 0
        for review in Review.objects.filter(title_id=obj.id):
            total_reviews += 1
            total_rating += int(review.score)
        if total_reviews == 0:
            return None
        return round(total_rating / total_reviews)
