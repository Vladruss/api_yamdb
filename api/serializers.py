from rest_framework import serializers
from rest_framework .serializers import Serializer

from .models import Users, Title, Genre, Category



class UserSerializer(serializers.ModelSerializer):
    #author = serializers.ReadOnlyField(source='author.username')

    class Meta:
        fields = '__all__'
        model = Users



class TokSerializer(Serializer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['email'] = serializers.EmailField()
        self.fields['confirmition_code'] = serializers.CharField()


class TitleSerializer(serializers.ModelSerializer):
    year = serializers.DateField(format='%Y', input_formats=['%Y'])

    class Meta():
        model = Title
        fields = ('id', 'name', 'year', 'category')


class GenreSerializer(serializers.ModelSerializer):

    class Meta():
        model = Genre
        fields = ('id', 'name', 'slug')


class CategorySerializer(serializers.ModelSerializer):

    class Meta():
        model = Category
        fields = ('name', 'slug')
        