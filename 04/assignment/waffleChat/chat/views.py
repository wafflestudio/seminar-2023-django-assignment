from rest_framework import generics, status
from rest_framework.response import Response
from .models import Character, Chat
from .serializers import CharacterSerializer, ChatSerializer


# Character List는 오직 GET 요청만 받음
class CharacterListView(generics.ListAPIView):
    queryset = Character.objects.all()
    serializer_class = CharacterSerializer


# GET과 POST를 한 url에서 처리하기 위한 view 구현
class ChatListCreateView(generics.ListCreateAPIView):
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer


# POST와 DELETE을 한 url에서 처리하기 위한 view 구현
class ChatDeleteAllView(generics.GenericAPIView):
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer

    def post(self, request, *args, **kwargs):
        Chat.objects.all().delete()
        return Response({'message': 'ok'}, status=status.HTTP_201_CREATED)

    def delete(self, request, *args, **kwargs):
        Chat.objects.all().delete()
        return Response({'message': 'ok'}, status=status.HTTP_204_NO_CONTENT)
