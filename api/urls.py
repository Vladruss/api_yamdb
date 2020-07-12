from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import ( 
    UserViewSet, EmailSignUpView, CodeConfirmView, MeProfileView, GenreListCreteDestroyView, 
    CategoryListCreteDestroyView, TitleViewSet, CommentViewSet, ReviewViewSet
)


router = DefaultRouter()
router.register('users', UserViewSet)
router.register('titles', TitleViewSet)
router.register('genres', GenreListCreteDestroyView)
router.register('categories', CategoryListCreteDestroyView)
router.register(r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments', CommentViewSet)
router.register(r'titles/(?P<title_id>\d+)/reviews', ReviewViewSet)

urlpatterns = [
    path('users/me/', MeProfileView.as_view()),
    path('', include(router.urls)),
    path('auth/token/', CodeConfirmView.as_view()),
    path('auth/email/', EmailSignUpView.as_view()),
]
