from rest_framework import serializers
from .models import Post, Comment


class PostSerializer(serializers.ModelSerializer):
    tags = serializers.CharField(max_length=100, required=False)
    class Meta:
        model = Post
        fields = [
            'id',
            'title',
            'description',
            'created_at',
            'updated_at',
            'created_by',
            'tags'
        ]
        read_only_fields = [
            'id',
            'created_at',
            'created_by',
        ]

class CommentSerializer(serializers.ModelSerializer):
    tags = serializers.CharField(max_length=100, required=False)
    class Meta:
        model = Comment
        fields = [
            'id',
            'content',
            'post',
            'created_by',
            'created_at',
            'updated_at',
            'is_updated',
            'tags',
        ]
        read_only_fields = [
            'id',
            'created_at',
            'created_by'
        ]
        extra_kwargs = {
            'post': {'read_only': True}
        }

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        fields = [
            'content',
            'post',
            'comment',
        ]
        extra_kwargs = {
            'content': {'read_only': True},
            'post': {'read_only': True},
            'comment': {'read_only': True},
        }