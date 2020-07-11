from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import  UserViewSet, Tok, APIUser,APIEmail


router = DefaultRouter()
router.register('users', UserViewSet)


urlpatterns = [
    path('users/me/', APIUser.as_view()),
    path('', include(router.urls)),
    path('auth/token/', Tok.as_view()),
    path('auth/email/', APIEmail.as_view()),
]
