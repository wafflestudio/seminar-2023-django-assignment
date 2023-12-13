from django.shortcuts import render

import openai

from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Character, Chat
from .serializers import CharacterSerializer, ChatSerializer
# Create your views here.


openai.api_key = "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"

def getAIResponse(content):
    resposnse = openai.chat.completetions.create(
        model="gpt-3.5-turbo",
          messages=[
            {"role": "system","content": "You are Ash in Pokemon."},
            {"role": "user","content": content},
        ],
    )
    return resposnse.choices[0].message.content



@api_view(['GET'])
def getcharacter(request):
    character = Character.objects.first()
    if character is None:
        character = Character.objects.create(
            first_name="Ash",
            last_name="Ketchum",
            image="https://upload.wikimedia.org/wikipedia/en/e/e4/Ash_Ketchum_Journeys.png",
            first_message="Hello, I'm Ash. I'm a Pokemon trainer."
        )
    serializer = CharacterSerializer(character)
    return Response(serializer.data)


@api_view(['GET', 'POST'])
def chatmanager(request):
    if request.method == 'GET':
        chats = Chat.objects.all()
        serializer = ChatSerializer(chats, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        content = request.data['content']
        chat_user = Chat.objects.create(
            role="user",
            content=content
        )
        user_serializer = ChatSerializer(chat_user)
        response = mycharacter.getAIResponse(content)
        chat_assistant = Chat.objects.create(
            role="assistant",
            content=response
        )
        assistant_serializer = ChatSerializer(chat_assistant)
        return Response({
            'user': user_serializer.data,
            'assistant': assistant_serializer.data,
        })


@api_view(['POST', 'DELETE'])
def chatdestroyer(request):
    if request.method == 'POST':
        Chat.objects.all().delete()
        return Response(status=204)
    elif request.method == 'DELETE':
        Chat.objects.all().delete()
        return Response(status=204)
