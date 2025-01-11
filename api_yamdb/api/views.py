from django.db.models import Avg
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from django.shortcuts import get_object_or_404
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.mixins import ListModelMixin, CreateModelMixin, \
    DestroyModelMixin, RetrieveModelMixin
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAdminUser
from rest_framework.viewsets import GenericViewSet
import django_filters

from api.permissions import AdminOrReadOnly, NotAnyOne, Admin, UserOrReadOnly
from reviews.models import (
    Comment,
    Review,
    MyUser,
    Category,
    Title,
    Genre
)

from api.serializers import (
    CommentSerializer,
    MyUserSerializer,
    TitlesSerializer,
    ReviewSerializer,
    CategorySerializer,
    GenreSerializer, TitleSerializersCreateUpdate
)


class CustomMixSet(ListModelMixin, CreateModelMixin,
                   DestroyModelMixin, GenericViewSet):
    pass


class MyUserViewSet(viewsets.ModelViewSet):
    queryset = MyUser.objects.all()
    serializer_class = MyUserSerializer


class TitleFilter(django_filters.FilterSet):
    category = django_filters.CharFilter(field_name="category__slug")
    genre = django_filters.CharFilter(field_name="genre__slug")

    class Meta:
        model = Title
        fields = ('name', 'year', 'category', 'genre')


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    permission_classes = (AdminOrReadOnly,)
    http_method_names = ['get', 'post', 'patch', 'delete']
    filterset_class = TitleFilter
    filter_backends = (DjangoFilterBackend, OrderingFilter)

    def get_serializer_class(self):
        if self.action in ('create', 'partial_update'):
            return TitleSerializersCreateUpdate
        return TitlesSerializer


"""    def get_queryset(self):
        return Title.objects.annotate(rating=Avg('reviews__score'))"""


class CategoryViewSet(CustomMixSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = PageNumberPagination
    filter_backends = (SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'
    permission_classes = (AdminOrReadOnly,)


class GenreViewSet(CustomMixSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    pagination_class = PageNumberPagination
    filter_backends = (SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'
    permission_classes = (AdminOrReadOnly,)


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
            Title,
            pk=self.kwargs.get('title_id')
        ).title.all()

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            title=get_object_or_404(
                Title,
                pk=self.kwargs.get('title_id')
            )
        )


class SignUp:
    pass


class GetToken:
    pass
