from rest_framework import serializers
from django.utils import timezone

from .models import User, Post, Comment

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password']


class CommentSerializer(serializers.ModelSerializer):
    post = serializers.StringRelatedField()
    created_by = serializers.StringRelatedField()

    class Meta:
        model = Comment
        fields = ['post', 'tags', 'content', 'created_by', 'created_at', 'updated_at', 'is_updated']
        read_only_fields = ['updated_at', 'created_at', 'is_updated', 'tags']


class PostSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True)
    created_by = serializers.StringRelatedField()
    
    class Meta:
        model = Post
        fields = ['id', 'title', 'description', 'tags', 'comments', 'created_by', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at', 'tags']
    # id = serializers.IntegerField(read_only=True)
    # title = serializers.CharField(max_length=30)
    # description = serializers.CharField(max_length=300)
    # created_at = serializers.DateTimeField(read_only=True)
    # updated_at = serializers.DateTimeField(read_only=True)
    
    # def create(self, validated_data):
    #     validated_data['created_at'] = timezone.datetime.now()
    #     validated_data['updated_at'] = timezone.datetime.now()
        
    #     return Post.objects.create(**validated_data)

    # def update(self, instance, validated_data):
    #     instance.title = validated_data.get('title', instance.title)
    #     instance.description = validated_data.get('description', instance.description)
    #     instance.updated_at = validated_data.get('updated_at', instance.updated_at)
    #     instance.save()
    #     return instance

