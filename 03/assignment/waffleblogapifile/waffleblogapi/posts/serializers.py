from rest_framework import serializers
from rest_framework.authtoken.models import Token
from .models import Post, Comment, Tag, User

class UserSerializer(serializers.ModelSerializer):
  class Meta:
    model = User
    fields = ['id', 'username', 'password']
    read_only_fields = ['id']

  def create(self, validated_data):
    new_user = User.objects.create(**validated_data)
    return new_user

class PostSerializer(serializers.ModelSerializer):
  class Meta:
    model = Post
    fields = ['id', 'title', 'tags', 'author', 'content', 'created_at', 'updated_at']
    read_only_fields = ['id', 'author', 'created_at', 'updated_at']

  def create(self, validated_data):
    if validated_data.tags is not None:
      for tag in validated_data.tags:
        if not Tag.objects.filter(content=tag.content).exists():
          Tag.objects.create(content=tag.content)
    return Post.objects.create(**validated_data)
  
  def update(self, instance, validated_data):
    instance.title = validated_data.get('title', instance.title)
    instance.tags = validated_data.get('tags', instance.tags)
    instance.content = validated_data.get('content', instance.content)
    instance.save()
    return instance
  

class CommentSerializer(serializers.ModelSerializer):
  class Meta:
    model = Comment
    fields = ['id', 'post', 'tags', 'author', 'updated', 'content', 'created_at', 'updated_at']
    read_only_fields = ['id', 'post', 'author', 'created_at', 'updated_at']

  def create(self, validated_data):
    if validated_data.tags is not None:
      for tag in validated_data.tags:
        if not Tag.objects.filter(content=tag.content).exists():
          Tag.objects.create(content=tag.content)
    return Comment.objects.create(**validated_data)
  
  def update(self, instance, validated_data):
    instance.post = validated_data.get('post', instance.post)
    instance.tags = validated_data.get('tags', instance.tags)
    instance.updated = True
    instance.content = validated_data.get('content', instance.content)
    instance.save()
    return instance