from rest_framework import serializers
from rest_framework.serializers import ValidationError
from rest_framework.validators import UniqueValidator, UniqueTogetherValidator
from .models import User, Post, Comment
from django.core.validators import MaxLengthValidator, MinLengthValidator


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'title', 'description', 'created_by', 'created_at', 'updated_at']
        validators = [
            UniqueTogetherValidator(
                queryset=Post.objects.all(),
                fields=['title'],
            )
        ]


class CommentSerializer(serializers.ModelSerializer):
    post = PostSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'post', 'created_by', 'created_at', 'updated_at', 'content', 'is_updated']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id']
