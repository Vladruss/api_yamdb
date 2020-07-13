from rest_framework import viewsets, filters, exceptions, permissions, status, generics, mixins
from rest_framework.response import Response  
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework_simplejwt.tokens import RefreshToken

from api.models import User, Genre, Category, Title, Review, Comment
from api.serializers import (UserSerializer, TokenSerializer, SignUpSerializer, GenreSerializer, 
CategorySerializer, TitleSerializer, CommentSerializer, ReviewSerializer
)
from api.permissions import IsAdmin, IsAdminOrReadOnly, IsStaffOrOwnerOrReadOnly 
from api.filters import TitleFilter
import uuid


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'username'
    permission_classes = [permissions.IsAuthenticated, IsAdmin]


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
            code = uuid.uuid4()
            user = User.objects.create(
                email=email, username=str(email), code=code, is_active=False
            )
            send_mail(
                'Подтверждение аккаунта',
                'Ваш ключ активации {}'.format(code),
                'from@example.com',
                [email],
                fail_silently=True,
            )
            return Response({'result':'Код подтверждения отправлен на вашу почту'}, status=200)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CodeConfirmView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, *args, **kwargs):
        serializer = TokenSerializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)  
        try:
            user = User.objects.get(
                email=serializer.data['email'], code=serializer.data['code']
            )
        except User.DoesNotExist:
            return Response(
                data={'detail': 'Invalid email or code'},
                status=status.HTTP_400_BAD_REQUEST
            )
        else:
            user.is_active = True
            user.save()
            refresh_token = RefreshToken.for_user(user)
            return Response({
                'token': str(refresh_token.access_token)
            })


class GenreListCreteDestroyView(mixins.CreateModelMixin,
                   mixins.DestroyModelMixin,
                   mixins.ListModelMixin,
                   viewsets.GenericViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly, 
        IsAdminOrReadOnly
    ]
    lookup_field = 'slug'
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']


class CategoryListCreteDestroyView(mixins.CreateModelMixin,
                   mixins.DestroyModelMixin,
                   mixins.ListModelMixin,
                   viewsets.GenericViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly, 
        IsAdminOrReadOnly
    ]
    lookup_field = 'slug'
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']


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
        title.update_rating()

    def perform_update(self, serializer):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, title_id=title)
        title.update_rating()

    def perform_destroy(self, instance):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        instance.delete()
        title.update_rating()


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
