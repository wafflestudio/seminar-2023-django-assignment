from rest_framework import serializers
from .models import Chat, Character

class CharacterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Character
        fields = ['id', 'image', 'first_name', 'last_name']
        read_only_fields = ['image']

class ChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chat
        fields = ['id', 'role', 'content', 'created_at']
        read_only_fields = ['role']