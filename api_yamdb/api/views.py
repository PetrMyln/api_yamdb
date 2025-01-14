from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from django.db.models import Avg
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework import filters, permissions, status
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.views import TokenObtainPairView

from api.filters import TitleFilter
from api.mixin import MixinSet
from api.permissions import (
    AdminOrReadOnly,
    UserPermission, UserOrModeratorOrReadOnly,
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
    MyUser,
    Review,
    Title,
)

class MyUserViewSet(viewsets.ModelViewSet):
    # Использовать приставку Custom в неймингах - плохой тон. Так же как и My.
    # Все переменные/функции/классы/модули "кастомные" и "твои",
    # лишний раз об этом говорить не стоит.
    queryset = MyUser.objects.order_by('pk')
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
        if serializer.is_valid():
            # У метода is_valid есть параметр-флаг raise_exception,
            # если его поставить в True, то можно избавиться от проверок,
            # метод вернет ошибки валидации. Можно почитать тут.
            if self.request.method == 'PATCH':
                serializer.validated_data.pop('role', None)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        if request.method == 'PUT':
            return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
        return super().update(request, *args, **kwargs)


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    permission_classes = (AdminOrReadOnly,)
    http_method_names = ['get', 'post', 'patch', 'delete']
    filterset_class = TitleFilter
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    pagination_class = PageNumberPagination

    def get_queryset(self):
        return Title.objects.annotate(rating=Avg('title__score'))

    def get_serializer_class(self):
        if self.action in ('create', 'partial_update'):
            return TitleSerializersCreateUpdate
        return TitlesSerializer


class CategoryViewSet(MixinSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class GenreViewSet(MixinSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = (UserOrModeratorOrReadOnly,)
    http_method_names = ['get', 'post', 'patch', 'delete']

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
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = (UserOrModeratorOrReadOnly,)
    http_method_names = ['get', 'post', 'patch', 'delete']

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


class SignUpView(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        serializer = AuthSerializer(data=request.data)
        if serializer.is_valid():
            user = MyUser.objects.get(
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
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TokenView(TokenObtainPairView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        serializer = TokenSerializer(data=request.data)
        if serializer.is_valid():
            user = get_object_or_404(
                MyUser, username=request.data.get('username')
            )
            if not default_token_generator.check_token(
                    user, request.data.get('confirmation_code')
            ):
                return Response(
                    'Неверный confirmation_code',
                    status=status.HTTP_400_BAD_REQUEST
                )
            token = {'token': str(AccessToken.for_user(user))}
            return Response(token, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
