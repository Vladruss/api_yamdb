from rest_framework import serializers
from rest_framework .serializers import Serializer

from .models import Title, Genre, Category


class GenreSerializer(serializers.ModelSerializer):

    class Meta():
        model = Genre
        fields = ('name', 'slug')


class CategorySerializer(serializers.ModelSerializer):

    class Meta():
        model = Category
        fields = ('name', 'slug')
        

class TitleSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(many=True, read_only=True)
    category = CategorySerializer(read_only=True)
    #genre = serializers.SlugRelatedField(many=True, read_only=True, slug_field='slug')
    #category = serializers.SlugRelatedField(read_only=True, slug_field='slug')
    
    class Meta():
        model = Title
        fields = ('__all__')
