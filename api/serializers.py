from rest_framework import serializers
from rest_framework .serializers import Serializer

from .models import Title, Genre, Category


class TitleSerializer(serializers.ModelSerializer):
    year = serializers.DateField(format='%Y', input_formats=['%Y'])
    
    class Meta():
        model = Title
        fields = ('id', 'name', 'year', 'genre', 'category', 'description')


class GenreSerializer(serializers.ModelSerializer):

    class Meta():
        model = Genre
        fields = ('id', 'name', 'slug')


class CategorySerializer(serializers.ModelSerializer):

    class Meta():
        model = Category
        fields = ('id', 'name', 'slug')
        