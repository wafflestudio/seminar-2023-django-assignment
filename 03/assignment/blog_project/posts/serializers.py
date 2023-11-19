from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from rest_framework.serializers import ValidationError
from rest_framework.validators import UniqueValidator, UniqueTogetherValidator
from .models import User, Post, Comment, Tag
from django.core.validators import MaxLengthValidator, MinLengthValidator


# class TagSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Tag
#         fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    comment_tags = serializers.CharField(required=False)
    #tags = TagSerializer(many=True, read_only=True)

    class Meta:
        model = Comment
        fields = '__all__'

        read_only_fields = [
            'id',
            'created_by',
            'is_updated',
            'post',
        ]

    def create(self, validated_data):
        tags_data = validated_data.pop('comment_tags', '')
        comment = Comment.objects.create(**validated_data)

        # Split the input string into individual tags
        tag_list = tags_data.split('#')

        for tag_data in tag_list:
            tag, created = Tag.objects.get_or_create(content=tag_data.strip())
            comment.comment_tags.add(tag)

        return comment



class CommentListSerializer(serializers.ModelSerializer):
    #comment_tags = TagSerializer(read_only=True, required=False)
    class Meta:
        model = Comment
        fields = '__all__'

        read_only_fields = [
            'id',
            'created_by',
            'is_updated',
            'post',
            'comment_tags',
        ]


class PostDetailSerializer(serializers.ModelSerializer):
    comment_set = CommentListSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = ['title', 'created_by', 'created_at', 'updated_at', 'tags',
                  'description', 'comment_set']
        validators = [
            UniqueTogetherValidator(
                queryset=Post.objects.all(),
                fields=['title'],
            )
        ]
        read_only_fields = [
            'id',
            'created_by',
            'tags',
        ]


class PostCreateSerializer(serializers.ModelSerializer):
    tags = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = Post
        fields = '__all__'

        read_only_fields = [
            'id',
            'created_by',
        ]

    def create(self, validated_data):
        tags_data = validated_data.pop('tags', '')
        post = Post.objects.create(**validated_data)

        # Split the input string into individual tags
        tag_list = tags_data.split('#')

        for tag_data in tag_list:
            tag, created = Tag.objects.get_or_create(content=tag_data.strip())
            post.tags.add(tag)

        return post


class PostListSerializer(serializers.ModelSerializer):
    description_summary = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ['id', 'title', 'tags', 'description_summary', 'created_by']

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

