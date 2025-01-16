from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from django.db.models import Avg
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework import filters, permissions, status
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.mixins import (
    ListModelMixin,
    DestroyModelMixin,
    CreateModelMixin
)
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet
from rest_framework_simplejwt.tokens import AccessToken

from api.filters import TitleFilter
from api.permissions import (
    AdminOrReadOnly,
    UserPermission,
    AuthorOrModeratorOrReadOnly,
)
from api.serializers import (
    AuthSerializer,
    CategorySerializer,
    CommentSerializer,
    GenreSerializer,
    CustomUserSerializer,
    ReviewSerializer,
    TitlesSerializer,
    TitleSerializersCreateUpdate,
    TokenSerializer
)
from reviews.models import (
    Category,
    Comment,
    Genre,
    Review,
    Title,
)
from users.models import User


class ListCreateDestroy(ListModelMixin, CreateModelMixin,
                        DestroyModelMixin, GenericViewSet):
    pagination_class = PageNumberPagination
    filter_backends = (SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'
    permission_classes = (AdminOrReadOnly,)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.order_by('pk')
    serializer_class = CustomUserSerializer
    permission_classes = (UserPermission,)
    lookup_field = 'username'
    filter_backends = (filters.SearchFilter,)
    search_fields = ('=username',)
    pagination_class = PageNumberPagination

    @action(
        methods=['GET', 'PATCH'], detail=False, url_path='me',
        permission_classes=(permissions.IsAuthenticated,)
    )
    def get_update_me(self, request):
        serializer = self.get_serializer(
            request.user,
            data=request.data,
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        if self.request.method == 'PATCH':
            serializer.validated_data.pop('role', None)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        if request.method == 'PUT':
            return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
        return super().update(request, *args, **kwargs)


class TitleViewSet(viewsets.ModelViewSet):
    permission_classes = (AdminOrReadOnly,)
    http_method_names = ['get', 'post', 'patch', 'delete']
    filterset_class = TitleFilter
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    pagination_class = PageNumberPagination

    def get_queryset(self):
        return Title.objects.annotate(
            rating=Avg('reviews__score')).order_by('name')

    def get_serializer_class(self):
        if self.action in ('create', 'partial_update'):
            return TitleSerializersCreateUpdate
        return TitlesSerializer


class CategoryViewSet(ListCreateDestroy):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class GenreViewSet(ListCreateDestroy):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = (
        IsAuthenticatedOrReadOnly,
        AuthorOrModeratorOrReadOnly
    )
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_review(self):
        return get_object_or_404(
            Review,
            title_id=self.kwargs.get('title_id'),
            id=self.kwargs.get('review_id'),
        )

    def get_queryset(self):
        return self.get_review().comments.all()

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            review=self.get_review()
        )


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = (
        IsAuthenticatedOrReadOnly,
        AuthorOrModeratorOrReadOnly
    )
    http_method_names = ['get', 'post', 'patch', 'delete']

    def title_obj(self):
        return get_object_or_404(
            Title,
            pk=self.kwargs.get('title_id')
        )

    def get_queryset(self):
        return self.title_obj().reviews.all()

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            title=self.title_obj()
        )


class SignUpView(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        serializer = AuthSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user, created = User.objects.get_or_create(
            username=request.data.get('username'),
            email=request.data.get('email')
        )
        confirmation_code = default_token_generator.make_token(user)
        send_mail(
            'Код подтверждения',
            f'Ваш код - {confirmation_code}',
            settings.SENDER_EMAIL,
            [request.data.get('email')]
        )

        return Response(serializer.data, status=status.HTTP_200_OK)


class TokenView(APIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = TokenSerializer

    def post(self, request):
        serializer = TokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        token = {'token': str(AccessToken.for_user(
            serializer.validated_data))}
        return Response(token, status=status.HTTP_200_OK)
