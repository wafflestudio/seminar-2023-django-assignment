from rest_framework import serializers
from .models import Post, Comment, Tag
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['content']

    def to_internal_value(self, data):
        # data가 문자열인 경우, 새로운 Tag 객체를 생성
        if isinstance(data, str):
            tag, created = Tag.objects.get_or_create(content=data)
            return tag

        # data가 딕셔너리인 경우, 기본 처리를 그대로 수행
        return super().to_internal_value(data)


class CommentSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)
    tags = TagSerializer(many=True)

    class Meta:
        model = Comment
        fields = ['id', 'description', 'post', 'created_at', 'updated_at', 'created_by', 'is_updated', 'tags']
        read_only_fields = ['post']

    def create(self, validated_data):
        tags_data = validated_data.pop('tags')
        post_id = self.context['view'].kwargs['post_id']

        post_instance = Post.objects.get(pk=post_id)
        validated_data['post'] = post_instance

        comment = Comment.objects.create(**validated_data)

        for tag_data in tags_data:
            tag, created = Tag.objects.get_or_create(content=tag_data)
            comment.tags.add(tag)

        return comment


class PostListSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)
    truncated_description = serializers.SerializerMethodField()
    comments = CommentSerializer(many=True, read_only=True)
    tags = TagSerializer(many=True)

    class Meta:
        model = Post
        fields = ['id', 'title', 'truncated_description', 'created_at', 'updated_at', 'created_by', 'comments', 'tags']

    def get_truncated_description(self, obj):
        # description이 300자를 넘으면 최대 300자까지 반환
        return obj.description[:300]


class PostCreateSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)
    comments = CommentSerializer(many=True, read_only=True)
    tags = TagSerializer(many=True)

    class Meta:
        model = Post
        fields = ['id', 'title', 'description', 'created_at', 'updated_at', 'created_by', 'comments', 'tags']

    def create(self, validated_data):
        tags_data = validated_data.pop('tags')
        post = Post.objects.create(**validated_data)

        for tag_data in tags_data:
            tag, created = Tag.objects.get_or_create(content=tag_data)
            post.tags.add(tag)

        return post


class PostDetailSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)
    comments = CommentSerializer(many=True, read_only=True)
    tags = TagSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'title', 'description', 'created_at', 'updated_at', 'created_by', 'comments', 'tags']
