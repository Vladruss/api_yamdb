from rest_framework import serializers

from api.models import User



class UserSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('username', 'id', 'first_name', 'last_name', 'email','role', 'bio')
        model = User
    
    

class UserMeSerializer(serializers.ModelSerializer):
    #author = serializers.ReadOnlyField(source='author.username')

    class Meta:
        fields = ('username', 'id', 'first_name', 'last_name', 'email','role', 'bio')
        model = User


from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import authenticate
from rest_framework import exceptions, serializers
class TokSerializer(TokenObtainPairSerializer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields[self.username_field] = serializers.CharField()