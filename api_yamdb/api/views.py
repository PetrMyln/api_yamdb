from rest_framework import viewsets
from django.shortcuts import get_object_or_404
from rest_framework.filters import SearchFilter
from rest_framework.pagination import PageNumberPagination

from api.permissions import AdminOrReadOnly
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
    queryset = Categories.objects.all().order_by('id')
    serializer_class = CategoriesSerializer
    pagination_class = PageNumberPagination
    filter_backends = (SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'
    #permission_classes = (AdminOrReadOnly,)

    def fperform_create(self, serializer):
        print(11111111111111111111111111)
        print(serializer)


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
                pk=self.kwargs.get('review_id')
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




class SignUp:
    pass

class GetToken:
    pass