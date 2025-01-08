from django.urls import include, path
from rest_framework import routers

from api.views import (
    TitlesViewSet,
    CategoriesViewSet,
    GenreViewSet,
    ReviewViewSet,
    CommentViewSet,
)

v1_router = routers.DefaultRouter()
v1_router.register('titles', TitlesViewSet, basename='titles')
v1_router.register('categories', CategoriesViewSet, basename='categories')
v1_router.register('genres', GenreViewSet, basename='genres')
v1_router.register(
    'title/(?P<titele_id>\d+)/review/',
    ReviewViewSet,
    basename='review')
v1_router.register(
    r'title/(?P<titele_id>\d+)/review/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comment')

urlpatterns = [
    path('v1/', include(v1_router.urls)),
    path('v1/auth/', include('djoser.urls')),
    path('v1/', include('djoser.urls.jwt')),
]
