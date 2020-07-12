from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import ( 
    UserViewSet, EmailSignUpView, Tok, MeProfileView, GenreList, APIGenre, CategoryList, 
    APICategory, TitleViewSet, CommentViewSet, ReviewViewSet
)


router = DefaultRouter()
router.register('users', UserViewSet)
router.register('titles', TitleViewSet)
router.register(r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments', CommentViewSet)
router.register(r'titles/(?P<title_id>\d+)/reviews', ReviewViewSet)

urlpatterns = [
    path('users/me/', MeProfileView.as_view()),
    path('', include(router.urls)),
    path('auth/token/', Tok.as_view()),
    path('auth/email/', EmailSignUpView.as_view()),
    path('genres/', GenreList.as_view()),
    path('genres/<str:slug>/', APIGenre.as_view()),
    path('categories/', CategoryList.as_view()),
    path('categories/<str:slug>/', APICategory.as_view()),
]
