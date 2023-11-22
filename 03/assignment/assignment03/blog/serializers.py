from rest_framework import serializers
from .models import User, Post, Comment, Tag


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username"]


class CreateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "password"]
    
    def validate_username(self, value):
        if len(value) < 4:
            raise serializers.ValidationError("Username should be at least 4 characters")
        return value
    
    def validate_password(self, value):
        if len(value) < 8:
            raise serializers.ValidationError("Password should be at least 8 characters")
        return value


class LoginUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "password"]
    

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['content']

    
    def run_validation(self, data):
        print(data)
        try:
            (is_empty_value, data) = self.validate_empty_values(data)
            if is_empty_value:
                return data
            value = self.to_internal_value(data)
            self.run_validators(value)
        except:
            value = Tag.objects.get(pk=data['content'])
        return value


class PostSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True)
    class Meta:
        model = Post
        fields = ['id', 'created_by', 'created_at', 'updated_at', 'title', 'description', 'tags']
        extra_kwargs = {"id" : {"read_only" : True}, "created_by" : {"read_only" : True}}
    
    def check_tags(self):
            for tag in Tag.objects.all():
                if Post.objects.filter(tags=tag).count() + Comment.objects.filter(tags=tag).count() == 0:
                    tag.delete()

    def create(self, validated_data):
        tags = validated_data.pop('tags')
        post = Post.objects.create(**validated_data)
        for tag in tags:
            if isinstance(tag, Tag):
                post.tags.add(tag)
            else:
                tag = Tag.objects.create(pk=tag['content'])
                post.tags.add(tag)
        return post
    
    def update(self, instance, validated_data):
        tags = validated_data.pop('tags')
        for key in validated_data:
            try:
                setattr(instance, key, validated_data[key])
            except KeyError:
                pass
        if tags:
            for tag in Tag.objects.filter(posts=instance):
                instance.tags.remove(tag)
            for tag in tags:
                if isinstance(tag, Tag):
                    instance.tags.add(tag)
                else:
                    tag = Tag.objects.create(pk=tag['content'])
                    instance.tags.add(tag)
        self.check_tags()
        return instance


class PostCreateSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True)
    class Meta:
        model = Post
        fields = ['title', 'description', 'tags']
    
    
class CommentSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True)
    class Meta:
        model = Comment
        fields = ['id', 'post', 'created_by', 'created_at', 'updated_at', 'content', 'is_updated', 'tags']
        extra_kwargs = {"id" : {"read_only" : True}, "post" : {"read_only" : True}, "created_by" : {"read_only" : True}, "is_updated" : {"read_only" : True}}
    
    def check_tags(self):
            for tag in Tag.objects.all():
                if Post.objects.filter(tags=tag).count() + Comment.objects.filter(tags=tag).count() == 0:
                    tag.delete()

    def create(self, validated_data):
        tags = validated_data.pop('tags')
        comment = Comment.objects.create(**validated_data)
        for tag in tags:
            if isinstance(tag, Tag):
                comment.tags.add(tag)
            else:
                tag = Tag.objects.create(pk=tag['content'])
                comment.tags.add(tag)
        return comment

    def update(self, instance, validated_data):
        tags = validated_data.pop('tags')
        for key in validated_data:
            try:
                setattr(instance, key, validated_data[key])
            except KeyError:
                pass
        if tags:
            for tag in Tag.objects.filter(comments__id=instance.id):
                instance.tags.remove(tag)
            for tag in tags:
                if isinstance(tag, Tag):
                    instance.tags.add(tag)
                else:
                    tag = Tag.objects.create(pk=tag['content'])
                    instance.tags.add(tag)
        self.check_tags()
        return instance
        

class CommentCreateSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True)
    class Meta:
        model = Comment
        fields = ['content', 'tags']


