from rest_framework import serializers

from api.models import User, Genre, Category, Title, Comment, Review


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('username', 'id', 'first_name', 'last_name', 'email','role', 'bio')
        model = User
    

class TokenSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    code = serializers.CharField(required=True)


class SignUpSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = ('email',)


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        fields = ('name', 'slug')


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ('name', 'slug')


class TitleSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(many=True, read_only=True)
    category = CategorySerializer(read_only=True)
    
    class Meta:
        model = Title
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')
    
    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'pub_date')


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')
    title_id = serializers.ReadOnlyField(source='title.pk')
    score = serializers.IntegerField(min_value=1, max_value=10)
    
    class Meta:
        model = Review
        fields = '__all__'
