from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import User, Post, Comment, Tag
from django.core.validators import MaxLengthValidator, MinLengthValidator
from rest_framework.validators import UniqueValidator
from rest_framework.validators import UniqueTogetherValidator
from rest_framework.serializers import ValidationError

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
        # tag 필드를 별도로 처리하고, 나머지 필드는 기본 로직을 사용
        tag_name = validated_data.pop('tag', None)
        
        # 부모 클래스의 update 메소드를 사용하여 나머지 필드를 업데이트
        instance = super().update(instance, validated_data)

        # tag 필드만 별도로 처리
        if tag_name:
            tag, created = Tag.objects.get_or_create(name=tag_name)
            instance.tag = tag
            instance.save()

        return instance
    # movie_reviews = serializers.PrimaryKeyRelatedField(source='reviews', many=True, read_only=True)
    # actors = serializers.StringRelatedField(many=True, read_only=True)
    # overview = serializers.CharField(validators=[MinLengthValidator(limit_value=10), MaxLengthValidator(limit_value=300)])
    # name = serializers.CharField(validators=[UniqueValidator(
    #     queryset= Movie.objects.all(),
    #     message='이미 존재하는 영화 이름입니다.',
    # )])
    
    # def validate(self, attrs):
    #     if 10 > len(attrs['overview']) or len(attrs['overview']) > 300:
    #         raise ValidationError('영화 소개는 10자 이상, 300자 이하로 작성해주세요.')
    #     if len(attrs['name']) > 50:
    #         raise ValidationError('영화 이름은 50자 이하로 작성해주세요.')
    #     return attrs


    

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


