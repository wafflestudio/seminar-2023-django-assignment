from rest_framework import serializers
from .models import Post, Comment


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = [
            'id',
            'title',
            'description',
            'created_at',
            'updated_at',
            'created_by',
        ]
        read_only_fields = [
            'id',
            'created_at',
            'created_by',
        ]

class CommentSerializer(serializers.ModelSerializer):
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
        ]
        read_only_fields = [
            'id',
            'created_at',
        ]
        extra_kwargs = {
            'post': {'read_only': True}
        }
