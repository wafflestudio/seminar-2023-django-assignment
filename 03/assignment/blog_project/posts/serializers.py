from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from rest_framework.serializers import ValidationError
from rest_framework.validators import UniqueValidator, UniqueTogetherValidator
from .models import User, Post, Comment
from django.core.validators import MaxLengthValidator, MinLengthValidator


class PostDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'title', 'description', 'created_by', 'created_at', 'updated_at']
        validators = [
            UniqueTogetherValidator(
                queryset=Post.objects.all(),
                fields=['title'],
            )
        ]


class PostListSerializer(serializers.ModelSerializer):
    description_summary = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ['id', 'title', 'description_summary', 'created_by']
        validators = [
            UniqueTogetherValidator(
                queryset=Post.objects.all(),
                fields=['title'],
            )
        ]

    def get_description_summary(self, obj):
        return obj.description[:300]


class CommentSerializer(serializers.ModelSerializer):
    post = PostDetailSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'post', 'created_by', 'created_at', 'updated_at', 'content', 'is_updated']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'password']
        extra_kwargs = {'password': {'write_only': True}}


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

