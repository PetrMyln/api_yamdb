from django.shortcuts import render


from reveiews.models import (
    MyUser,
    Categories,
    Titles,
    Genre
)

from api.serializers import (
    MyUserSerializer,
    TitlesSerializer,
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
