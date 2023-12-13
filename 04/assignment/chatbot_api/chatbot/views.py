from django.shortcuts import render

from openai import OpenAI

from rest_framework.generics import RetrieveAPIView, ListCreateAPIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .models import Character, Chat
from .serializers import CharacterSerializer, ChatSerializer


# Create your views here.
@api_view(['GET'])
def character_view(request):
    character = Character.objects.all()[0]

    if request.method == 'GET':
        serializer = CharacterSerializer(character)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ChatListCreateAPIView(ListCreateAPIView):
    serializer_class = ChatSerializer
    queryset = Chat.objects.all()

    def get(self, request, *args, **kwargs):
        if not Chat.objects.all().exists():
            character = Character.objects.all()[0]
            Chat.objects.create(role='assistant', content=character.first_message)

        return super().get(request, *args, **kwargs)

    def perform_create(self, serializer):
        user_message = serializer.save(role='user')

        client = OpenAI()

        character = Character.objects.all()[0]

        chats = [{'role': chat.role, 'content': chat.content} for chat in Chat.objects.all()]
        chats.insert(0, {'role': 'assistant', 'content': character.first_message})
        chats.insert(0, {'role': 'system', 'content': '지금부터 말끝마다 "피카"를 붙여서 대답해야해'})
        chats.insert(0, {'role': 'system', 'content': '너의 캐릭터 이름은 '+character.first_name+character.last_name+'이야'})

        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=chats
        )

        new_chat = completion.choices[0].message
        Chat.objects.create(role=new_chat.role, content=new_chat.content)


#class ChatRetrieveUpdateDeleteAPIView(RetrieveUpdateDestroyAPIView):
#    serializer_class = ChatDetailSerializer
#    queryset = Chat.objects.all()

#    def perform_update(self, serializer):
#        content = serializer.validated_data.pop('content')

#        client = OpenAI()

#        messages = [{'role': message.role, 'content': message.content} for message in serializer.instance.messages.all()]
#        messages.insert(0, {'role': 'system', 'content': '너의 캐릭터 이름은 ' + serializer.instance.character.name + '이야'})
#        messages.append({'role': 'user', 'content': content})

#        completion = client.chat.completions.create(
#            model="gpt-3.5-turbo",
#            messages=messages
#        )

#        new_message = completion.choices[0].message
#        Message.objects.create(role='user', content=content, chat=serializer.instance)
#        Message.objects.create(role=new_message.role, content=new_message.content, chat=serializer.instance)


@api_view(['POST', 'DELETE'])
def chat_delete_all(request):
    chats = Chat.objects.all()
    if request.method == 'POST' or request.method == 'DELETE':
        for chat in chats:
            chat.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

