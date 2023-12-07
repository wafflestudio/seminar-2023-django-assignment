from rest_framework import serializers
from .models import Post, Comment, Tag, User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password']

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['content']

class CommentSerializer(serializers.ModelSerializer):
    post = serializers.StringRelatedField()
    created_by = serializers.StringRelatedField()
    tag = TagSerializer(many=True, read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'content' ,'created_at', 'updated_at', 'created_by', 'post', 'is_updated', 'tag']
        read_only_fields = ['id', 'created_at', 'updated_at', 'created_by', 'post', 'is_updated']

class PostSerializer(serializers.ModelSerializer):
    #comments = CommentSerializer(many=True, read_only=True)
    comments = serializers.StringRelatedField(many=True, read_only=True)
    created_by = serializers.StringRelatedField()
    tag = TagSerializer(many=True, read_only=True)
    
    class Meta:
        model = Post
        fields = ['id', 'title', 'description', 'created_at', 'updated_at', 'created_by', 'comments', 'tag']
        read_only_fields = ['created_at', 'updated_at', 'created_by']