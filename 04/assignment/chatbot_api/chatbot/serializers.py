from .models import Chat, Character
from .validators import character_input_validator
from rest_framework import serializers


class CharacterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Character
        fields = ['id', 'first_name', 'last_name', 'image', 'first_message']
        read_only_fields = ['id', 'first_name', 'last_name', 'image', 'first_message']


class ChatSerializer(serializers.ModelSerializer):

    class Meta:
        model = Chat
        fields = ['id', 'role', 'content', 'dt_created']
        read_only_fields = ['id', 'role', 'dt_created']

