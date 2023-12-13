from rest_framework import serializers
from chatbackend.models import Character, Chat

class CharacterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Character
        fields = "__all__"
        read_only_fields = ['id', 'image']


class ChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chat
        fields = "__all__"
        read_only_fields = ['id', 'role', 'created_at']
        write_only_fields = ['user']
        required_fields = ['content']