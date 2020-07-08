from rest_framework import viewsets, generics, filters, exceptions, permissions
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.auth import models

from .models import Users, Genre, Title, Category
from .serializers import UserSerializer, TokSerializer, TitleSerializer,\
    CategorySerializer, GenreSerializer
from .permissions import IsAdminOrReadOnly #AuthorRightPermission
from django.http import HttpResponse
  
class UserViewSet(viewsets.ModelViewSet):
    queryset = Users.objects.all()
    serializer_class = UserSerializer
    #permission_classes = [permissions.IsAuthenticatedOrReadOnly, AuthorRightPermission]
    #filter_backends = [DjangoFilterBackend]
    #filterset_fields = ['group',]
    
    #def perform_create(self, serializer):
        #serializer.save(author=self.request.user)

def user_contact(request):
    pass

from rest_framework_simplejwt.views import TokenObtainPairView

class Tok(TokenObtainPairView):
    serializer_class = TokSerializer


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'category', 'year', 'genre',]
    pagination_classes = PageNumberPagination

    def perform_create(self, serializer):
        serializer.save(name=self.request.name)


class CategoryList(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [
        IsAdminOrReadOnly
    ]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name',]
    pagination_classes = PageNumberPagination

    def perform_create(self, serializer):
        serializer.save(name=self.request.data['name'])

    def perform_destroy(self, instance):
        instance.delete(name=self.request.name)


class GenreList(generics.ListCreateAPIView):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [
        IsAdminOrReadOnly
    ]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'slug',]
    pagination_classes = PageNumberPagination

    def perform_create(self, serializer):
        serializer.save()

    def perform_destroy(self, instance):
        instance.delete(name=self.request.name)