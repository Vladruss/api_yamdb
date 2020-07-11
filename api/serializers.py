from rest_framework import serializers, exceptions
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from api.models import User, Genre, Category, Title, Comment, Review
from django.contrib.auth import authenticate


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('username', 'id', 'first_name', 'last_name', 'email','role', 'bio')
        model = User
    

class TokSerializer(TokenObtainPairSerializer):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields[self.username_field] = serializers.CharField()
        self.fields.pop('password', None)
        #self.fields[self.Confirmation_code] = serializers.IntegerField()
        def validate(self, attrs):
            authenticate_kwargs = {
            self.username_field: attrs[self.username_field],
            
            }
            try:
                authenticate_kwargs.pop('password', None)
                authenticate_kwargs['request'] = self.context['request']
            except KeyError:
                pass

            self.user = authenticate(**authenticate_kwargs)

            # Prior to Django 1.10, inactive users could be authenticated with the
            # default `ModelBackend`.  As of Django 1.10, the `ModelBackend`
            # prevents inactive users from authenticating.  App designers can still
            # allow inactive users to authenticate by opting for the new
            # `AllowAllUsersModelBackend`.  However, we explicitly prevent inactive
            # users from authenticating to enforce a reasonable policy and provide
            # sensible backwards compatibility with older Django versions.
            if self.user is None or not self.user.is_active:
                raise exceptions.AuthenticationFailed(
                    self.error_messages['no_active_account'],
                    'no_active_account',
                )

            return {}


class EmailSerializer(serializers.Serializer):
    email = serializers.EmailField()


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

class CommentSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')
    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'pub_date')


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')
    title_id = serializers.ReadOnlyField(source='title.pk')
    class Meta:
        model = Review
        fields = ('__all__')