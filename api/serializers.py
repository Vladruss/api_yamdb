from rest_framework import serializers
from rest_framework .serializers import Serializer

from .models import Title, Genre, Category


class TitleSerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(many=True, read_only=True, slug_field='slug')
    category = serializers.SlugRelatedField(read_only=True, slug_field='slug')
    
    class Meta():
        model = Title
        fields = ('__all__')


class GenreSerializer(serializers.ModelSerializer):

    class Meta():
        model = Genre
        fields = ('id', 'name', 'slug')


class CategorySerializer(serializers.ModelSerializer):

    class Meta():
        model = Category
        fields = ('id', 'name', 'slug')
        