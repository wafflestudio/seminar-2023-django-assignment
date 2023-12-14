from rest_framework import serializers

from .models import Chat, Character


class ChatSerializer(serializers.ModelSerializer):

    class Meta:
        model = Chat
        fields = '__all__'

        read_only_fields = [
            'id',
            'role',
            'created_at',
        ]


class CharacterSerializer(serializers.ModelSerializer):

    class Meta:
        model = Character
        fields = '__all__'

        read_only_fields = [
            'id',
            'image',
        ]
