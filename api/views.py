from rest_framework import exceptions, filters, generics, permissions, viewsets, request
from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.auth import models

from .models import Title, Comment, Review
from .serializers import (
    CommentSerializer,
    ReviewSerializer,
)
from .permissions import IsOwnerOrReadOnly
import rest_framework
from rest_framework.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from django.db.models import Avg



class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsOwnerOrReadOnly]


    def perform_create(self, serializer):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        if request.method == 'POST' and Review.objects.filter(user=self.request.user, title=title).exists():
            raise ValidationError('Вы уже поставили оценку')
        serializer.save(author=self.request.user, title=title)
        score = Review.objects.filter(title=title).agregate(Avg('score'))
        title.rating = score['score__avg']
        title.save(update_fields=['rating'])

    def get_queryset(self):
        title = get_object_or_404(Title, pk=self.kwargs['title_id'])
        return Review.objects.filter(title=title)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        review = get_object_or_404(Review, pk=self.request.data.get('title_id'))
        serializer.save(author=self.request.user, review=review)
        
    def get_queryset(self):
        review = get_object_or_404(Review, pk=self.request.data.get('title_id'))
        return Comment.objects.filter(review=review)
