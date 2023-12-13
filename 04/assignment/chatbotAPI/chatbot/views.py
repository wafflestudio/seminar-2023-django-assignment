from rest_framework.generics import ListCreateAPIView, DestroyAPIView, RetrieveAPIView, CreateAPIView

from .models import Chat, Character
from .serializers import ChatSerializer, CharacterSerializer
from .chatgpt import Chatgpt


class CharacterRetrieveAPI(RetrieveAPIView):
    #만들어둔 캐릭터 retrieve
    queryset = Character.objects.first()
    serializer_class = CharacterSerializer


class ChatListCreateAPI(ListCreateAPIView):
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer
    chatgpt = Chatgpt()

    def get(self, request, *args, **kwargs):
        #채팅 기록이 없으면 캐릭터의 first message 보여주기
        if not self.queryset.exists():
            Chat.objects.create(
                role='assistant',
                content=Character.objects.first().get_first_message(),
            )
        return self.list(request, *args, **kwargs)

    def perform_create(self, serializer):
        user_query = serializer.save(role='user')
        serializer.save(content=self.chatgpt.ask(user_query))


class ChatDeleteAPI(DestroyAPIView):
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer

    def post(self, request, *args, **kwargs):
        self.delete(self, request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        self.queryset.delete()
        return self.destroy(request, *args, **kwargs)

