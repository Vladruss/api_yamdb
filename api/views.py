from rest_framework import viewsets, generics, filters, exceptions, permissions
from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.auth import models

from .models import Users
from .serializers import UserSerializer, TokSerializer
#from .permissions import AuthorRightPermission
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

