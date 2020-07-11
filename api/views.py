from rest_framework import viewsets, filters, exceptions, permissions, status, generics
from rest_framework.response import Response  
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from django_filters.rest_framework import DjangoFilterBackend
from django.core.mail import send_mail
from django.contrib.auth import models
from django.shortcuts import get_object_or_404
from django.db.models import Avg

from api.models import User, Genre, Category, Title, Review, Comment
from api.serializers import UserSerializer, TokSerializer, EmailSerializer,  GenreSerializer, CategorySerializer, TitleSerializer, CommentSerializer, ReviewSerializer
from api.permissions import UserPermission, GenrePermission, CommentPermission 
from api.filters import TitleFilter


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'username'
    permission_classes = [ permissions.IsAuthenticated , UserPermission]


class APIUser(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        user = User.objects.get(username=request.user.username)
        serializer = UserSerializer(user)
        return Response(serializer.data)
    
    def patch(self, request):
        user = User.objects.get(username=request.user.username)
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class APIEmail(APIView):
    def post(self, request):
        serializer = EmailSerializer(data=request.data)
        if serializer.is_valid():
            Toemail = serializer.data.get('email')
            if User.objects.filter(email=email).exists():
                return Response({"Email занят"}, status=status.HTTP_400_BAD_REQUEST)
            else:
                user = User.objects.create(email=email)
                Confirmation_code = 1111
                send_mail(
                    'Подтверждение аккаунта',
                    'Ваш ключ активации {}'.format(Confirmation_code),
                    'from@example.com',
                    [Toemail],
                    fail_silently=True,
                )
            return Response({"Код подтверждения отправлен на вашу почту"}, status=200)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Tok(TokenObtainPairView):
    serializer_class = TokSerializer


class APIUser(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        user = User.objects.get(username=request.user.username)
        serializer = UserSerializer(user)
        return Response(serializer.data)
    
    def patch(self, request):
        user = User.objects.get(username=request.user.username)
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GenreList(generics.ListCreateAPIView):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, GenrePermission]
    filter_backends = [filters.SearchFilter]
    search_fields = [ 'name']


class APIGenre(APIView):
    permission_classes = [permissions.IsAdminUser]
    
    def delete(self, request, slug):
        genre = Genre.objects.get(slug=slug)
        genre.delete()
        return Response(status=204)


class CategoryList(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, GenrePermission]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']


class APICategory(APIView):
    permission_classes = [permissions.IsAdminUser]
    
    def delete(self, request, slug):
        category = Category.objects.get(slug=slug)
        category.delete()
        return Response(status=204)


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, GenrePermission]
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter

    def perform_create(self, serializer):
        serializer.save(
            genre=Genre.objects.filter(slug__in=self.request.data.getlist('genre')),
            category=Category.objects.get( slug=self.request.data.get('category'))
        )

    def perform_update(self, serializer):
        serializer.save(
            genre=Genre.objects.filter(slug__in=self.request.data.getlist('genre')),
            category=get_object_or_404(Category, slug=self.request.data.get('category'))
            )


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, CommentPermission]
    
    def get_queryset(self):
        queryset = self.queryset
        return queryset.filter(title_id=self.kwargs['title_id'])

    def perform_create(self, serializer):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        if int(self.request.data['score'])>10 or int(self.request.data['score'])<1:
            raise exceptions.ValidationError('Оценка должна быть от 1 до 10')
        if Review.objects.filter(author=self.request.user, title_id=title).exists():
            raise exceptions.ValidationError('Вы уже поставили оценку')
        serializer.save(author=self.request.user, title_id=title)
        avg_score = Review.objects.filter(title_id=title).aggregate(Avg('score'))
        title.rating = avg_score['score__avg']
        title.save(update_fields=['rating'])

    def perform_update(self, serializer):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, title_id=title)
        avg_score = Review.objects.filter(title_id=title).aggregate(Avg('score'))
        title.rating = avg_score['score__avg']
        title.save(update_fields=['rating'])


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, CommentPermission]

    def get_queryset(self):
        queryset = self.queryset
        return queryset.filter(review_id=self.kwargs['review_id'])

    def perform_create(self, serializer):
        review = get_object_or_404(Review, pk=self.kwargs.get('review_id'))
        serializer.save(author=self.request.user, review_id=review)
