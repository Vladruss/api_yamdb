from rest_framework import serializers, exceptions
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from api.models import User
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
        self.fields[self.Confirmation_code] = serializers.IntegerField()
class EmailSerializer(serializers.Serializer):
    email = serializers.EmailField()