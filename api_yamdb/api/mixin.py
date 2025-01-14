from rest_framework.filters import SearchFilter
from rest_framework.mixins import (
    ListModelMixin,
    CreateModelMixin,
    DestroyModelMixin)
from rest_framework.pagination import PageNumberPagination
from rest_framework.viewsets import GenericViewSet

from api.permissions import AdminOrReadOnly


class MixinSet(ListModelMixin, CreateModelMixin,
               DestroyModelMixin, GenericViewSet):
    pagination_class = PageNumberPagination
    filter_backends = (SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'
    permission_classes = (AdminOrReadOnly,)
