from rest_framework import serializers

from .models import Users



class UserSerializer(serializers.ModelSerializer):
    #author = serializers.ReadOnlyField(source='author.username')

    class Meta:
        fields = '__all__'
        model = Users

from rest_framework .serializers import Serializer

class TokSerializer(Serializer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['email'] = serializers.EmailField()
        self.fields['confirmition_code'] = serializers.CharField()
