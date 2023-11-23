from .models import User, Post, Comment, Tag

from django.contrib.auth import get_user_model
from django.core.validators import MaxLengthValidator, MinLengthValidator

from rest_framework import serializers
from rest_framework.validators import UniqueValidator, UniqueTogetherValidator
from rest_framework.serializers import ValidationError

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
   password = serializers.CharField(write_only=True)

   class Meta:
      model = User
      fields = ('username', 'password', 'email')
      extra_kwargs = {'password': {'write_only': True}}

   def create(self, validated_data):
      user = User.objects.create_user(
         username=validated_data['username'],
         email=validated_data['email'],
         password=validated_data['password']
      )
      return user

   def update(self, instance, validated_data):
      password = validated_data.pop('password', None)
      instance = super().update(instance, validated_data)

      if password:
         instance.set_password(password)
         instance.save()
      return instance

class LoginSerializer(serializers.Serializer):
   username = serializers.CharField()
   password = serializers.CharField(write_only=True)

class PostSerializer(serializers.ModelSerializer):
   content_preview = serializers.SerializerMethodField()
   tag = serializers.CharField(max_length=100, required=False)  

   class Meta:
      model = Post
      fields = ['id', 'title', 'comments', 'content', 'content_preview','author', 'dt_created', 'dt_modified', 'tag']
      read_only_fields = ['comments', 'dt_created', 'dt_modified', 'author', 'tag']
        
   def get_content_preview(self, obj):
      return obj.content[:300]
    
   def create(self, validated_data):
      tag_name = validated_data.pop('tag', None)  
      post = Post.objects.create(**validated_data) 

      if tag_name:
         tag, created = Tag.objects.get_or_create(name=tag_name)  
         post.tag = tag  
         post.save()
      return post
    
   def update(self, instance, validated_data):
      tag_name = validated_data.pop('tag', None)

      instance = super().update(instance, validated_data)

      if tag_name:
         tag, created = Tag.objects.get_or_create(name=tag_name)
         instance.tag = tag
         instance.save()
      return instance

class CommentSerializer(serializers.ModelSerializer):
   tag = serializers.CharField(max_length=100, required=False)  

   class Meta:
      model = Comment
      fields = ['id', 'content', 'tag', 'post', 'author', 'dt_created', 'dt_updated', 'is_updated', 'tag']
      read_only_fields = ['dt_created', 'dt_updated', 'is_updated', 'author', 'tag']
        
   def create(self, validated_data):
      tag_name = validated_data.pop('tag', None)  
      comment = Comment.objects.create(**validated_data) 

      if tag_name:
         tag, created = Tag.objects.get_or_create(name=tag_name)  
         comment.tag = tag  
         comment.save()
      return comment