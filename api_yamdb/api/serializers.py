from rest_framework import serializers

from reviews.models import (
    Comment,
    Review,
    MyUser,
    Category,
    Title,
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


class TitlesSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    genre = GenreSerializer(many=True)

    # rating = serializers.IntegerField()

    class Meta:
        fields = ('id',
                  'name',
                  'year',
                  'description',
                  # 'rating',
                  'genre',
                  'category',)

        model = Title


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

    class Meta:
        fields = ('id',
                  'name',
                  'year',
                  'description',
                  # 'rating',
                  'genre',
                  'category',)
        model = Title
