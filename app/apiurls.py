from django.urls import include, path
from rest_framework.routers import SimpleRouter

from .apiview import (CityViewSet, CommentPostViewSet, CommentsCityViewSet,
                      FollowViewSet, PostViewSet, ProflieView, UserViewSet)

router = SimpleRouter()
router.register('city/comments', CommentsCityViewSet)
router.register('post/comments', CommentPostViewSet)
router.register('user', UserViewSet)
router.register('post',PostViewSet)
router.register('city', CityViewSet)
router.register('follow', FollowViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('profile/', ProflieView.as_view(),)
]