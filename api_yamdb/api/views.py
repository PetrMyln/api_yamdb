from rest_framework import viewsets

from reviews.models import (
    Comment,
    Review,
    MyUser,
    Categories,
    Titles,
    Genre
)

from api.serializers import (
    CommentSerializer,
    MyUserSerializer,
    TitlesSerializer,
    ReviewSerializer,
    CategoriesSerializer,
    GenreSerializer
)







class MyUserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = MyUser.objects.all()
    serializer_class = MyUserSerializer


class TitlesViewSet(viewsets.ModelViewSet):
    queryset = Titles.objects.all()
    serializer_class = TitlesSerializer


class CategoriesViewSet(viewsets.ModelViewSet):
    queryset = Categories.objects.all()
    serializer_class = CategoriesSerializer


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class CommentViewSet(viewsets.ModelViewSet):
    """Вьюсет для комментариев."""
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    """Вьюсет для ревью."""
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer


class MyUserViewSet(viewsets.ModelViewSet):
    queryset = MyUser.objects.all()
    serializer_class = MyUserSerializer



