from rest_framework import serializers
from .models import User, Post, Comment, Tag


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'
        extra_kwargs={
            'content':{"validators":[]},
        }
    

class UserSerializer(serializers.ModelSerializer):
    posts = serializers.StringRelatedField(many=True, read_only=True)
    comments = serializers.StringRelatedField(many=True, read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']
        extra_kwargs = {
            'password': {'write_only':True},
        }

class PostSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)
    tags = TagSerializer(many=True)
    comments = serializers.StringRelatedField(many=True, read_only=True)

    class Meta:
        model = Post
        fields = '__all__'
        read_only_fields = ['dt_created', 'dt_updated']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        view_type = self.context.get('view').__class__.__name__
        if view_type=='PostListView':
            representation['content'] = instance.content[:300] if instance.content else ''
            representation.pop('dt_created', None)
            representation.pop('dt_updated', None)
            representation.pop('comments', None)
        else:
            representation['content'] = instance.content
        return representation

class PostCreateSerializer(serializers.ModelSerializer):
    tags = serializers.ListField(child=serializers.CharField(max_length=20),
                                 required=False, write_only=True)
    class Meta:
        model=Post
        fields = ['title','content','tags']
        read_only_fields = ['dt_created', 'dt_updated', 'author']

    def create(self, validated_data):
        tags_data = validated_data.pop('tags', [])
        post = Post.objects.create(**validated_data)

        tags = [Tag.objects.get_or_create(content=tag.lower())[0] for tag in tags_data]
        post.tags.set(tags)
        return post

class PostUpdateSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, required=False)
    
    class Meta:
        model = Post
        fields = ['title', 'content', 'tags']
        read_only_fields = ['dt_created', 'dt_updated', 'author']

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.content = validated_data.get('content', instance.content)
        instance.save()

        tags_data = validated_data.pop('tags', None)

        if tags_data is not None:
            instance.tags.clear()
            tags = [Tag.objects.get_or_create(content=tag['content'].lower())[0] for tag in tags_data]
            instance.tags.set(tags)

        instance.save()
        return instance

class CommentSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)
    post = serializers.StringRelatedField()
    tags = serializers.PrimaryKeyRelatedField(queryset=Tag.objects.all(), many=True)

    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ['dt_created', 'dt_updated', 'is_updated']

class CommentCreateSerializer(serializers.ModelSerializer):
    tags = serializers.ListField(child=serializers.CharField(max_length=20),
                                 required=False, write_only=True)
    class Meta:
        model = Comment
        fields = ['content', 'tags']
        read_only_fields = ['dt_created', 'dt_updated', 'post', 'author']

    def create(self, validated_data):
        tags_data = validated_data.pop('tags', [])
        comment = Comment.objects.create(**validated_data)

        tags = [Tag.objects.get_or_create(content=tag.lower())[0] for tag in tags_data]
        comment.tags.set(tags)
        return comment

class CommentUpdateSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, required=False)

    class Meta:
        model = Comment
        fields = ['content', 'tags']
        read_only_fields = ['dt_created', 'dt_updated', 'is_updated', 'author', 'post']

    def update(self, instance, validated_data):
        tags_data = validated_data.pop('tags', None)
        instance.content = validated_data.get('content', instance.content)

        if tags_data is not None:
            instance.tags.clear()
            tags = [Tag.objects.get_or_create(content=tag['content'].lower())[0] for tag in tags_data]
            instance.tags.set(tags)

        instance.save()
        return instance
