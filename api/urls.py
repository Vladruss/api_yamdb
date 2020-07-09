from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import CommentViewSet, ReviewViewSet
from django.contrib import admin

router = DefaultRouter()
router.register(r'posts/(?P<post_id>\d+)/comments', CommentViewSet)
router.register(r"title/(?P<review_id>\d+)/review", ReviewViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('admin/', admin.site.urls),
]
