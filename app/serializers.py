from rest_framework import serializers
from .models import Post, City, Follow, CommentCity, CommentPost, CustomUser


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('title', 'author', 'id')


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'description')


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('username', 'id', 'email')


class DetailUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('username', 'id', 'email', 'image', 'description')


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ('title_ru', 'id')


class DetailPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'


class DetailCitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = '__all__'


class FollowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follow
        fields = '__all__'


class CommentPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommentPost
        fields = '__all__'


class CommentCitySerializer(serializers.ModelSerializer):
    class Meta:
        model = CommentCity
        fields = '__all__'