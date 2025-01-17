from api_yamdb.constant import LENGTH_DISCRIPTION, LENGTH_TEXT, LENGTH_USERNAME
from api_yamdb.validators import validate_username
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from reviews.models import Category, Comment, Genre, Review, Title
from users.models import User


class AuthSerializer(serializers.Serializer):
    email = serializers.EmailField(
        required=True,
        max_length=LENGTH_TEXT
    )
    username = serializers.CharField(
        required=True,
        max_length=LENGTH_USERNAME,
        validators=(
            validate_username,
            UnicodeUsernameValidator()
        )
    )

    def validate(self, data):
        username = data.get('username')
        email = data.get('email')
        rule_username = User.objects.filter(username=username).exists()
        rule_email = User.objects.filter(email=email).exists()
        if (rule_email and rule_username) or (not rule_email
                                              and not rule_username):
            print(data)
            return data
        ans_error = (email, username)[rule_username]
        raise serializers.ValidationError(
            f'Проверьте {ans_error} уже используется!')

    def create(self, validated_data):
        user, _ = User.objects.get_or_create(
            username=validated_data.get('username'),
            email=validated_data.get('email')
        )
        return user


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

        return user


class UserSerializer(serializers.ModelSerializer):
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
    rating = serializers.IntegerField()

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

    class Meta:
        fields = ('id',
                  'name',
                  'year',
                  'description',
                  'genre',
                  'category',)
        model = Title

    def to_representation(self, instance):
        print(111111111111111111111111)

        serializer = TitlesSerializer(instance)
        print(serializer)
        return serializer

    def validate_genre(self, value):
        if not value:
            return serializers.ValidationError({
                'Ошибка': 'Необходимо указать жанр произведения.'
            })
        return value
