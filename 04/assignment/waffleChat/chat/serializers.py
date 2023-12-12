from rest_framework import serializers
from .models import Character, Chat


class CharacterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Character
        fields = '__all__'


class ChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chat
        fields = '__all__'

    # def create(self, validated_data):
    #     role = self.context.get('role', 'user')
    #     validated_data['role'] = role
    #
    #     return super().create(validated_data)
