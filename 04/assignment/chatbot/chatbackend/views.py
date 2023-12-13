from django.shortcuts import render
from .models import Character, Chat
from .serializer import CharacterSerializer, ChatSerializer
from rest_framework.response import Response
from rest_framework.views    import APIView
from rest_framework import status
import openai
import os

openai.api_key = "비공개"

class characterView(APIView):
    def get(self, request):
        object = Character.objects.get(pk=1)
        serializer = CharacterSerializer(object)
        return Response(serializer.data)

class chatView(APIView):
    def get(self, request):
        object = Chat.objects.all()
        serializer = ChatSerializer(object, many = True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = ChatSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(role = 'user')
            
            completion = openai.ChatCompletion.create(
                model = "gpt-3.5-turbo",
                messages = [
                    {"role": "system", "content": "넌 쿠로미야! 대답은 길고 반말로 감성적으로 해야 해"},
                    {"role":"user", "content":request.data['content']}
                ]
            )
            
            content = completion.choices[0].message.content         
            newchat = Chat.objects.create(role = 'assistant', content = content)
            newchat.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class chatDeleteView(APIView):
    def delete(self, request):
        Chat.objects.all().delete()
        content = '안녕 난 쿠로미야'         
        newchat = Chat.objects.create(role = 'assistant', content = content)
        newchat.save()
        return Response(status=status.HTTP_200_OK)
    
    def post(self, request):
        Chat.objects.all().delete()
        content = '안녕 난 쿠로미야'         
        newchat = Chat.objects.create(role = 'assistant', content = content)
        newchat.save()
        return Response(status=status.HTTP_200_OK)

