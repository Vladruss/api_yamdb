from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import TitleViewSet, \
    CategoryList, APICategory, GenreList, APIGenre


router = DefaultRouter()
router.register('titles', TitleViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('categories/', CategoryList.as_view()),
    path('categories/<str:slug>/', APICategory.as_view()),
    path('genres/', GenreList.as_view()),
    path('genres/<str:slug>/', APIGenre.as_view()),
]
