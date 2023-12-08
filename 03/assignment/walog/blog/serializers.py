from rest_framework import serializers
from django.utils import timezone

from .models import User, Post, Comment, Tag
from . import views

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password']

class TagSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=200)
    class Meta:
        model = Tag
        fields = ['name']

class CommentSerializer(serializers.ModelSerializer):
    post = serializers.StringRelatedField()
    created_by = serializers.StringRelatedField()
    tags = TagSerializer(many=True)

    class Meta:
        model = Comment
        fields = ['id', 'post', 'tags', 'content', 'created_by', 'created_at', 'updated_at', 'is_updated']
        read_only_fields = ['id', 'updated_at', 'created_at']

    
    def create(self, validated_data):
        if 'tags' not in validated_data:
            return Comment.objects.create(**validated_data)

        tag_data = validated_data.pop('tags')
        
        comment = Comment.objects.create(**validated_data)
        for tag in tag_data:
            tag = tag['name']
            tag = tag.strip()
            if tag is None:
                continue

            if Tag.objects.filter(name=tag):
                _tag = Tag.objects.get(name=tag)
                comment.tags.add(_tag)
            else:                
                _tag = Tag(name=tag)
                _tag.save()
                comment.tags.add(_tag)
        return comment

    def update(self, instance, validated_data):

        instance.content = validated_data.get('content', instance.content)
        instance.updated_at = validated_data.get('updated_at', instance.updated_at)
        instance.is_updated = validated_data.get('is_updated', instance.is_updated)
        tag_data = validated_data.get('tags', [])
        
        if tag_data:
            instance.tags.clear()
            for tag in tag_data:
                tag = tag['name']
                tag = tag.strip()
                if tag is None:
                    continue

                if Tag.objects.filter(name=tag):
                    _tag = Tag.objects.get(name=tag)
                    instance.tags.add(_tag)
                else:                
                    _tag = Tag(name=tag)
                    _tag.save()
                    instance.tags.add(_tag)
        instance.save()
        views.TagCheck()
        return instance



class PostSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True)
    created_by = serializers.StringRelatedField()
    #tags = serializers.CharField(max_length=200)
    tags = TagSerializer(many=True)
    
    class Meta:
        model = Post
        fields = ['id', 'title', 'description', 'tags', 'comments', 'created_by', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

    def create(self, validated_data):
        if 'tags' not in validated_data:
            return super().create(**validated_data)

        tag_data = validated_data.pop('tags')
        
        post = Post.objects.create(**validated_data)
        for tag in tag_data:
            tag = tag['name']
            tag = tag.strip()
            if tag is None:
                continue

            if Tag.objects.filter(name=tag):
                _tag = Tag.objects.get(name=tag)
                post.tags.add(_tag)
            else:                
                _tag = Tag(name=tag)
                _tag.save()
                post.tags.add(_tag)
        return post

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)
        instance.updated_at = validated_data.get('updated_at', instance.updated_at)
        tag_data = validated_data.get('tags', [])
        if tag_data:
            instance.tags.clear()
            for tag in tag_data:
                tag = tag['name']
                tag = tag.strip()
                if tag is None:
                    continue

                if Tag.objects.filter(name=tag):
                    _tag = Tag.objects.get(name=tag)
                    instance.tags.add(_tag)
                else:                
                    _tag = Tag(name=tag)
                    _tag.save()
                    instance.tags.add(_tag)
        instance.save()
        views.TagCheck()
        return instance


    # id = serializers.IntegerField(read_only=True)
    # title = serializers.CharField(max_length=30)
    # description = serializers.CharField(max_length=300)
    # created_at = serializers.DateTimeField(read_only=True)
    # updated_at = serializers.DateTimeField(read_only=True)
    
    # def create(self, validated_data):
    #     validated_data['created_at'] = timezone.datetime.now()
    #     validated_data['updated_at'] = timezone.datetime.now()
        
    #     return Post.objects.create(**validated_data)
