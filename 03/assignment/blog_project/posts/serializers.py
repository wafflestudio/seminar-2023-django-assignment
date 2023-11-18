from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from rest_framework.serializers import ValidationError
from rest_framework.validators import UniqueValidator, UniqueTogetherValidator
from .models import User, Post, Comment
from django.core.validators import MaxLengthValidator, MinLengthValidator


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'post', 'created_by', 'created_at', 'updated_at', 'content', 'is_updated']

        read_only_fields = [
            'id',
            'post',
            'created_by',
            'created_at',
            'updated_at',
            'is_updated',
        ]

    # def update(self, instance, validated_data):
    #     if self.context['request'].user != instance.created_by:
    #         raise serializers.ValidationError("댓글을 수정할 권한이 없습니다.")
    #
    #     return super(CommentSerializer, self).update(instance, validated_data)


class PostDetailSerializer(serializers.ModelSerializer):
    comment_set = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'title', 'description', 'created_by', 'created_at', 'updated_at', 'comment_set']
        validators = [
            UniqueTogetherValidator(
                queryset=Post.objects.all(),
                fields=['title'],
            )
        ]
        read_only_fields = [
            'id',
            'created_by',
        ]


class PostCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = ['id', 'title', 'description', 'created_by']
        validators = [
            UniqueTogetherValidator(
                queryset=Post.objects.all(),
                fields=['title'],
            )
        ]
        read_only_fields = [
            'id',
            'created_by',
        ]


class PostListSerializer(serializers.ModelSerializer):

    description_summary = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ['id', 'title', 'description_summary', 'created_by']

    def get_description_summary(self, obj):
        return obj.description[:300]


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password')
        hashed_password = make_password(password)
        user = User.objects.create(password=hashed_password, **validated_data)
        return user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

