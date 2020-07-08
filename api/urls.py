from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import  UserViewSet, user_contact, Tok, TitleViewSet, \
    CategoryList, GenreList


router = DefaultRouter()
router.register('users', UserViewSet)
#router.register(r'posts/(?P<post_id>\d+)/comments', CommentViewSet)
router.register('titles', TitleViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('auth/token/', Tok.as_view()),
    path('auth/email/', user_contact),
    path('categories/', CategoryList.as_view()),
    path('categories/<str:slug>/', CategoryList.as_view()),
    path('genres/', GenreList.as_view()),
    path('genres/<str:slug>/', GenreList.as_view())
]
