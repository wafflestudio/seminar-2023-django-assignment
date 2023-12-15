from django.shortcuts import redirect

from rest_framework.generics import ListCreateAPIView, RetrieveAPIView, CreateAPIView, DestroyAPIView
from rest_framework.response import Response
from rest_framework import status

from .services import Chatgpt
from .models import Chat, Character
from .serializers import ChatSerializer, CharacterSerializer


class CharacterRetrieveView(RetrieveAPIView):
    serializer_class = CharacterSerializer
    queryset = Character.objects.first()

    def retrieve(self, request, *args, **kwargs):
        instance = Character.objects.first()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

class ChatListView(ListCreateAPIView):
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer
    chatgpt = Chatgpt()

    def get(self, request, *args, **kwargs):
        if not self.get_queryset().exists():
            Chat.objects.create(
                role='assistant',
                content=Character.objects.first().get_first_message(),
            )
        return self.list(request, *args, **kwargs)

    def perform_create(self, serializer):
        user_query = self.request.data.get('content')
        serializer.save(role='user')

        gpt_serializer = ChatSerializer(data={'role': 'assistant', 'content': self.chatgpt.ask(user_query)})

        if gpt_serializer.is_valid():
            gpt_serializer.save(role='assistant')


class ChatDeleteView(DestroyAPIView, CreateAPIView):
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer

    def post(self, request, *args, **kwargs):
        return self.delete(self, request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        self.get_queryset().delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

def go_to_character_info(request):
    return redirect('character-info')