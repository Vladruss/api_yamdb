from rest_framework import serializers, exceptions
from django.contrib.auth import models

from .models import Comment, Review, Title

class CommentSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')

    class Meta:
        fields = ('id', 'text', 'author', 'pub_date')
        model = Comment


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')

    class Meta:
        fields = ['id', 'text', 'author', 'score', 'pub_date']
        model = Review