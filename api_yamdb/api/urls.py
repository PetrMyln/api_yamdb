from django.urls import include, path
from rest_framework import routers

from api.views import (
    CommentViewSet,
    CategoryViewSet,
    GenreViewSet,
    UserViewSet,
    ReviewViewSet,
    SignUpView,
    TokenView,
    TitleViewSet,
)

v1_router = routers.DefaultRouter()
v1_router.register('users', UserViewSet, basename='users')
v1_router.register('titles', TitleViewSet, basename='titles')
v1_router.register('categories', CategoryViewSet, basename='categories')
v1_router.register('genres', GenreViewSet, basename='genres')
v1_router.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='reviews'
)
v1_router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comments'
)

urlpatterns = [
    path('v1/', include(v1_router.urls)),
    path('v1/auth/signup/', SignUpView.as_view(), name='sign_up'),
    path('v1/auth/token/', TokenView.as_view(), name='get_token'),
    #ANTON
    # Урлы с одинаковым префиксом выносим в отдельный
    # список. Будет один список urlpatterns, в нем остается
    # префикс версии, и инклюдом подключаем список, в котором
    # останется два path, ведущий на роутер и на auth/.
]
