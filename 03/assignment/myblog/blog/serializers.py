from rest_framework import serializers
from .models import Post, Comment, Tag

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['content']

class CommentSerializer(serializers.ModelSerializer):
    #tag_list = serializers.ListField(write_only=True, required=False, allow_empty=True)
    tags = TagSerializer(many=True, read_only=True)
    class Meta:
        model = Comment
        fields = ['post', 'author', 'content', 'created_at', 'updated_at', 'tags']
        read_only_fields = ['post', 'author', 'created_at', 'updated_at']
    def create(self, validated_data):
        return Comment.objects.create(**validated_data)


class PostSerializer(serializers.ModelSerializer):
    #tag_list = serializers.ListField(write_only=True, required=False, allow_empty=True)
    tags = TagSerializer(many=True, read_only = True)
    #comments = serializers.StringRelatedField(many=True)
    comments = CommentSerializer(many=True, read_only=True)
    class Meta:
        model = Post
        fields = ['title', 'content', 'comments', 'author', 'dt_created', 'dt_updated', 'tags']
        read_only_fields = ['author', 'dt_created', 'dt_updated']
    #title = serializers.CharField()
    #content = serializers.CharField()
    #author = serializers.CharField()
    #dt_created = serializers.DateField()
    #dt_updated = serializers.DateField()

    def create(self, validated_data):
        return Post.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.content = validated_data.get('content', instance.content)
        instance.author = validated_data.get('author', instance.author)
        instance.dt_created = validated_data.get('dt_created', instance.dt_created)
        instance.dt_updated = validated_data.get('dt_updated', instance.dt_updated)
        instance.save()
        return instance
