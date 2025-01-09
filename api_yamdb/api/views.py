from rest_framework import viewsets
from django.shortcuts import get_object_or_404
from rest_framework.pagination import LimitOffsetPagination

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


class MyUserViewSet(viewsets.ModelViewSet):
    queryset = MyUser.objects.all()
    serializer_class = MyUserSerializer
    

class TitlesViewSet(viewsets.ModelViewSet):
    queryset = Titles.objects.all()
    serializer_class = TitlesSerializer


class CategoriesViewSet(viewsets.ModelViewSet):
    queryset = Categories.objects.all()
    serializer_class = CategoriesSerializer
    pagination_class = LimitOffsetPagination

class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class CommentViewSet(viewsets.ModelViewSet):
    """Вьюсет для комментариев."""
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def get_queryset(self):
        return get_object_or_404(
            Review,
            pk=self.kwargs.get('review_id')
        ).review.all()
    
    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            review=get_object_or_404(
                Review,
                pk=self.kwargs.getself.kwargs.get('review_id')
            )
        )
    


class ReviewViewSet(viewsets.ModelViewSet):
    """Вьюсет для ревью."""
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer


    def get_queryset(self):
        return get_object_or_404(
            Titles,
            pk=self.kwargs.get('title_id')
        ).title.all()
    
    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            title=get_object_or_404(
                Titles,
                pk=self.kwargs.get('title_id')
            )
        )






