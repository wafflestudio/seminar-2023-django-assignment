from rest_framework import serializers
from .models import Character, Chat

class ChracterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Character
        fields = '__all__'

class ChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chat
        fields = '__all__'
        read_only_fields = ['created_at', 'role']
