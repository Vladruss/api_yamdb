from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import  UserViewSet, user_contact, Tok


router = DefaultRouter()
router.register('users', UserViewSet)
#router.register(r'posts/(?P<post_id>\d+)/comments', CommentViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('auth/token/', Tok.as_view()),
    path('auth/email/', user_contact),

]
