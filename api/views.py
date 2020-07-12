from rest_framework import viewsets, filters, exceptions, permissions, status, generics
from rest_framework.response import Response  
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from django_filters.rest_framework import DjangoFilterBackend
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django.db.models import Avg

from api.models import User, Genre, Category, Title, Review, Comment
from api.serializers import (UserSerializer, TokSerializer, SignUpSerializer, GenreSerializer, 
CategorySerializer, TitleSerializer, CommentSerializer, ReviewSerializer
)
from api.permissions import IsAdmin, IsAdminOrReadOnly, IsStaffOrOwnerOrReadOnly 
from api.filters import TitleFilter


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'username'
    permission_classes = [ permissions.IsAuthenticated , IsAdmin]


class MeProfileView(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_object(self):
        return self.request.user


class EmailSignUpView(APIView):
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        serializer = SignUpSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.data.get('email')
            code = generate_unique_code_here
            user = User.objects.create(email=email, code=code, is_active=False)
            send_mail(
                    'Подтверждение аккаунта',
                    'Ваш ключ активации {}'.format(code),
                    'from@example.com',
                    [email],
                    fail_silently=True,
            )
            return Response({"Код подтверждения отправлен на вашу почту"}, status=200)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Tok(TokenObtainPairView):
    serializer_class = TokSerializer


class GenreList(generics.ListCreateAPIView):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAdminOrReadOnly]
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
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAdminOrReadOnly]
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
    
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAdminOrReadOnly]
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
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsStaffOrOwnerOrReadOnly]
    
    def get_queryset(self):
        queryset = self.queryset
        return queryset.filter(title_id=self.kwargs['title_id'])

    def perform_create(self, serializer):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
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
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsStaffOrOwnerOrReadOnly]

    def get_queryset(self):
        queryset = self.queryset
        return queryset.filter(review_id=self.kwargs['review_id'])

    def perform_create(self, serializer):
        review = get_object_or_404(Review, pk=self.kwargs.get('review_id'))
        serializer.save(author=self.request.user, review_id=review)
