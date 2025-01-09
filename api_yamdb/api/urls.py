from django.urls import include, path
from rest_framework import routers

from api.views import (
    CommentViewSet,
    ReviewViewSet,
    MyUserViewSet,
    TitlesViewSet,
    CategoriesViewSet,
    GenreViewSet,
)

v1_router = routers.DefaultRouter()
v1_router.register('titles', TitlesViewSet, basename='titles')
v1_router.register('categories', CategoriesViewSet, basename='categories')
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
    path('v1/auth/', include('djoser.urls')),
    path('v1/', include('djoser.urls.jwt')),
]
