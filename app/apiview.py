from rest_framework import generics, mixins, status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet, ModelViewSet

from app.service import PostPage

from .models import (Category, City, CommentCity, CommentPost, CustomUser,
                     Follow, Post)
from .serializers import (CitySerializer, CommentCitySerializer,
                          CommentPostSerializer, DetailCitySerializer,
                          DetailPostSerializer, FollowSerializer,
                          PostSerializer, ProfileSerializer, 
                          UserSerializer, DetailUserSerializer)


class ProflieView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, pk):
        return CustomUser.objects.get(id = pk)

    def get(self, request):
        user = self.get_object(request.user.id)
        serializer = ProfileSerializer(user)
        return Response({'get' : serializer.data})
    
    def patch(self, request):
        try:
            instance = self.get_object(request.user.id)
        except:
            return Response({'put' : 'User not found'})
        serializer = ProfileSerializer(data = request.data, instance = instance, context = {'request' : request}, partial=True)
        serializer.is_valid(raise_exception = True)
        serializer.save()
        return Response({'put' : serializer.data})


class UserViewSet(ModelViewSet):
    queryset = CustomUser.objects.all()
    filterset_fields = ['username', 'id']
    pagination_class = PostPage

    def get_permissions(self):
        if self.action == 'list':
            permission_classes = [permissions.AllowAny]
        else:
            permission_classes = [permissions.IsAdminUser]
        return [permission() for permission in permission_classes]

    def get_serializer_class(self, *args, **kwargs):
        if self.action == 'list':
            return UserSerializer
        else:
            return DetailUserSerializer



class PostViewSet(mixins.RetrieveModelMixin, mixins.ListModelMixin, GenericViewSet):
    queryset = Post.objects.all()
    filterset_fields = ['title']
    pagination_class = PostPage

    def get_serializer_class(self, *args, **kwargs):
        if self.action == 'list':
            return PostSerializer
        else:
            return DetailPostSerializer


class CommentPostViewSet(ModelViewSet):
    queryset = CommentPost.objects.all()
    serializer_class = CommentPostSerializer
    filterset_fields = ['user', 'post', 'id']
    pagination_class = PostPage


class CityViewSet(PostViewSet):
    queryset = City.objects.all()
    filterset_fields = ['title_ru']

    def get_serializer_class(self, *args, **kwargs):
        if self.action == 'list':
            return CitySerializer
        else:
            return DetailCitySerializer

class CommentsCityViewSet(ModelViewSet):
    queryset = CommentCity.objects.all()
    serializer_class = CommentCitySerializer
    filterset_fields = ['user', 'city', 'id']
    pagination_class = PostPage


class FollowViewSet(mixins.CreateModelMixin,
                   mixins.RetrieveModelMixin,
                   mixins.DestroyModelMixin,
                   mixins.ListModelMixin,
                   GenericViewSet):

    queryset = Follow.objects.all()
    serializer_class = FollowSerializer
    filterset_fields = ['follower', 'user']
    pagination_class = PostPage


    def create(self, request):
        users = request.data 
        if users['user']==users['follower']:
            return Response({'post':{'error': 'The user cannot be subscribed to himself'}})

        if Follow.objects.filter(user = users['user'], follower=users['follower']):
           return Response({'post':{'error': 'The object already exists'}})

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid()
        serializer.save()

        return Response({'post' : serializer.data})
    
    