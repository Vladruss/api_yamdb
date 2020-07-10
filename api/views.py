from rest_framework import viewsets, generics, filters, permissions
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.exceptions import ValidationError

from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from django.contrib.auth import models
from django.http import HttpResponse


from .models import Genre, Title, Category
from .serializers import TitleSerializer,\
    CategorySerializer, GenreSerializer
from .permissions import GenrePermission



class CategoryList(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [GenrePermission]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name',]
    pagination_classes = PageNumberPagination


class APICategory(APIView):
    permission_classes = [permissions.IsAdminUser]
    def delete(self, request, slug):
        category = Category.objects.get(slug=slug)
        category.delete()
        return Response(status=204)


class GenreList(generics.ListCreateAPIView):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [GenrePermission]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name',]


class APIGenre(APIView):
    permission_classes = [permissions.IsAdminUser]

    def delete(self, request, slug):
        genre = Genre.objects.get(slug=slug)
        genre.delete()
        return Response(status=204)


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    permission_classes = [GenrePermission]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['category', 'genre', 'year', 'name',]
    pagination_classes = PageNumberPagination

    def perform_create(self, serializer):
        serializer.save(
            genre=Genre.objects.filter(slug__in=self.request.data.getlist('genre')),
            category=get_object_or_404(Category, slug=self.request.data.get('category'))
        )

    def perform_update(self, serializer):
        serializer.save(
            genre=Genre.objects.filter(slug__in=self.request.data.getlist('genre')),
            category=get_object_or_404(Category, slug=self.request.data.get('category'))
        )