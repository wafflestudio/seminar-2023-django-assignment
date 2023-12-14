from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import ListCreateAPIView, DestroyAPIView, RetrieveAPIView, CreateAPIView

from .models import Chat, Character
from .serializers import ChatSerializer, CharacterSerializer
from .chatgpt import Chatgpt


class CharacterRetrieveAPI(RetrieveAPIView):
    #만들어둔 캐릭터 retrieve
    queryset = Character.objects.all()
    serializer_class = CharacterSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_queryset().first()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class ChatListCreateAPI(ListCreateAPIView):
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer
    chatgpt = Chatgpt()

    def get(self, request, *args, **kwargs):
        #채팅 기록이 없으면 캐릭터의 first message 보여주기
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

    # def delete(self, request, *args, **kwargs):
    #     self.get_queryset().delete()
    #     return self.list(request, *args, **kwargs)


class ChatDeleteAPI(DestroyAPIView, CreateAPIView):
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer

    def post(self, request, *args, **kwargs):
        return self.delete(self, request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        self.get_queryset().delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

