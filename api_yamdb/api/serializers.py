from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.relations import SlugRelatedField

from reveiews.models import (
    MyUser,
    Categories,
    Titles,
    Genre
)


class MyUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = (
            'id',
            'username',
            'first_name',
            'last_name',
            'bio',
            'role',
        )



class TitlesSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('id', 'name', 'year', 'category', 'genge',)
        model = Titles


class CategoriesSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('id', 'name', 'slug')
        model = Categories


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('id', 'name', 'slug')
        model = Genre
