from rest_framework import serializers
from .models import Post, Comment, Tag


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)
    tags = serializers.StringRelatedField(many=True, read_only=True)
    tag_list = serializers.CharField(allow_blank=True, write_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'content', 'author', 'post', 'dt_created', 'dt_updated', 'is_updated', 'tags', 'tag_list']
        read_only_fields = ['id', 'author', 'post', 'dt_created', 'dt_updated', 'is_updated', 'tags']


class PostListSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)
    truncated_content = serializers.SerializerMethodField(method_name='get_truncated_content')
    comments = serializers.StringRelatedField(many=True, read_only=True)
    tags = serializers.StringRelatedField(many=True, read_only=True)
    tag_list = serializers.CharField(allow_blank=True, write_only=True)

    class Meta:
        model = Post
        fields = ['id', 'title', 'content', 'truncated_content', 'author', 'dt_created', 'dt_updated', 'comments', 'tags', 'tag_list']
        read_only_fields = ['id', 'author', 'dt_created', 'dt_updated', 'truncated_content', 'comments', 'tags']
        extra_kwargs = {
            'content': {'write_only': True}
        }

    def get_truncated_content(self, obj):
        return obj.content[:300]


class PostDetailSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)
    comments = CommentSerializer(many=True, read_only=True)
    tags = serializers.StringRelatedField(many=True, read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'title', 'content', 'author', 'dt_created', 'dt_updated', 'comments', 'tags']
        read_only_fields = ['id', 'author', 'dt_created', 'dt_updated', 'comments']
