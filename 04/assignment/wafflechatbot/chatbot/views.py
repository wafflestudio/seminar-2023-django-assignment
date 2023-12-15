from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.http import JsonResponse
from django.shortcuts import redirect
from drf_yasg.utils import swagger_auto_schema

from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, ListCreateAPIView, RetrieveAPIView
from rest_framework.response import Response
from rest_framework import status

from .services import chatgpt
from .models import Chat, Character
from .serializers import ChatSerializer, CharacterSerializer

from openai import OpenAI

class ChatListView(ListCreateAPIView):
    
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer
    
    def get(self, request, *args, **kwargs):
        if not Chat.objects.exists():
            Chat.objects.create(role='assistant',
                                content=Character.objects.first().first_message)
        
        return self.list(request, *args, **kwargs)

    def post(self, request):
        
        serializer = ChatSerializer(data=request.data)
        
        if serializer.is_valid(raise_exception=True):
            serializer.save(role='user')
            serializer.save()

            response = ChatSerializer(data={
                'content': chatgpt.make_response(serializer.data['content'])
            })
            if response.is_valid(raise_exception=True):
                response.save(role='assistant')
                return Response(response.data, 200)
            return Response(response.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CharacterInfoView(RetrieveAPIView):
    
    serializer_class = CharacterSerializer
    queryset = Character.objects.first()

    def retrieve(self, request, *args, **kwargs):
        instance = Character.objects.first()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

class ChatDeleteView(APIView):
    def post(self, request):
        Chat.objects.all().delete()
        return Response({'message' : 'ok'})

    def delete(self, request):
        Chat.objects.all().delete()
        return Response({'message' : 'ok'})

def go_to_character_info(request):
    return redirect('character-info')