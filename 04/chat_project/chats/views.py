from .services import gpt
from .serializers import CharacterSerializer, ChatSerializer
from .models import Character, Chat

from rest_framework.views import APIView
from rest_framework import generics, status
from rest_framework.response import Response

from django.shortcuts import redirect


class CharacterInfoAPI(APIView):
    def get(self, request):
        serializer = CharacterSerializer(Character.objects.first())
        return Response(serializer.data)


class ChatListCreateAPI(generics.ListCreateAPIView):
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer

    def get(self, request, *args, **kwargs):
        if not Chat.objects.exists():
            Chat.objects.create(role="assistant", content=Character.objects.first().first_message)
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        Chat.objects.create(role="user", content=request.data.get('content'))
        Chat.objects.create(role="assistant", content=gpt.make_response())
        serializer = ChatSerializer(Chat.objects.latest('created_at'))
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class ChatDestroyAPI(APIView):
    def delete(self, request):
        while Chat.objects.exists():
            Chat.objects.first().delete()
        return Response({'message': 'ok'}, status=status.HTTP_200_OK)

    def get(self, request):
        self.delete(request)
        return Response({'message': 'ok'}, status=status.HTTP_200_OK)


def go_to_character_info(request):
    return redirect('character-info')
