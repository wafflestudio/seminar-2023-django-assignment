from rest_framework import generics, status
from rest_framework.response import Response

from . import serializers
from .models import Character, Chat

from openai import OpenAI

from .secret_key import API_KEY
client = OpenAI(api_key=API_KEY)

class CharacterView(generics.GenericAPIView):
    serializer_class = serializers.CharacterSerializer
    def get(self, request):
        character = Character.objects.get(id=1)
        serializer = serializers.CharacterSerializer(character)
        data = serializer.data
        data["image"] = "https://assignment04-bucket.s3.ap-northeast-2.amazonaws.com/profile.png"
        return Response(data)


class ChatListView(generics.GenericAPIView):
    serializer_class = serializers.ChatCreateSerializer

    def get_queryset(self):
        return Chat.objects.all()

    def get(self, request):
        chats = self.get_queryset()
        serializer = serializers.ChatSerializer(chats, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        data = request.data
        data["role"] = "user"
        userSerializer = serializers.ChatSerializer(data=data)
        if userSerializer.is_valid():
            userSerializer.save()
        userContent = userSerializer.data["content"]

        responseContent = ""
        try:
            response = client.chat.completions.create(

                model="gpt-3.5-turbo", 
                messages=[{"role":"user", "content":userContent}],
                max_tokens=30
            )
            responseContent = response.choices[0].message.content
        except Exception as e:
            print(e)
        assistantSerializer = serializers.ChatSerializer(data={"content": responseContent + "! 보노보노!", "role":"assistant"})

        #print(responseContent)
        if assistantSerializer.is_valid():
            assistantSerializer.save()
        return Response(userSerializer.data, status=status.HTTP_201_CREATED)


class DeleteAllView(generics.GenericAPIView):
    serializer_class = serializers.ChatSerializer

    def post(self, request):
        return Response(status=status.HTTP_201_CREATED)
    
    def delete(self, request):
        chats = Chat.objects.all()
        for chat in chats:
            chat.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)