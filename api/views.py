from rest_framework import viewsets, generics, filters, exceptions, permissions, status
from rest_framework.response import Response  
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView

from django.core.mail import send_mail
from django.contrib.auth import models
from api.models import User
from .serializers import UserSerializer, TokSerializer, EmailSerializer
from .permissions import UserPermission


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'username'
    permission_classes = [ UserPermission]


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
