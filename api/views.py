from rest_framework import viewsets, generics, filters, exceptions, permissions
from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.auth import models
from rest_framework.views import APIView
from api.models import User
from .serializers import UserSerializer, TokSerializer, UserMeSerializer
from .permissions import UserPermission, UserMePermission
from django.http import HttpResponse
from rest_framework.response import Response  
from rest_framework import status
from django.core.mail import send_mail


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'username'
    permission_classes = [ UserPermission]


def user_contact(request):
    Toemail= request.data['email']
    send_mail(
    'Confirmtion Code',
    'Confirmtion Code',
    'from@example.com',  # Это поле "От кого"
    [Toemail],  # Это поле "Кому" (можно указать список адресов)
    fail_silently=False, # Сообщать об ошибках («молчать ли об ошибках?»)
)


from rest_framework_simplejwt.views import TokenObtainPairView

class Tok(TokenObtainPairView):
    serializer_class = TokSerializer



class APIUser(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request):
        user = User.objects.get(username=request.user.username)
        serializer = UserMeSerializer(user)
        return Response(serializer.data)
    def patch(self, request):
        user = User.objects.get(username=request.user.username)
        serializer = UserMeSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
