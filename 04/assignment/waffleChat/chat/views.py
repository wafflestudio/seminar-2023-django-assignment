from rest_framework import generics, status
from rest_framework.response import Response
from openai import OpenAI
from .models import Character, Chat
from .serializers import CharacterSerializer, ChatSerializer
from django.conf import settings



# Character List는 오직 GET 요청만 받음
class CharacterListView(generics.ListAPIView):
    queryset = Character.objects.all()
    serializer_class = CharacterSerializer


# GET과 POST를 한 url에서 처리하기 위한 view 구현
class ChatListCreateView(generics.ListCreateAPIView):
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer

    def post(self, request, *args, **kwargs):
        user_input = request.data.get('content', '')

        openai_response = self.generate_openai_response(user_input)

        serializer = self.get_serializer(data={'role': 'user', 'content': user_input})
        serializer.is_valid(raise_exception=True)
        serializer.save()

        assistant_serializer = self.get_serializer(data={'role': 'assistant', 'content': openai_response})
        assistant_serializer.is_valid(raise_exception=True)
        assistant_serializer.save()

        return Response({'message': 'ok'}, status=status.HTTP_201_CREATED)

    def generate_openai_response(self, user_input):
        client = OpenAI(
            api_key = settings.OPENAI_API_KEY,
        )
        response = client.chat.completions.create(
            messages=[
                {
                    'role': 'user',
                    'content': user_input,
                }
            ],
            model='gpt-3.5-turbo',
        )
        return response.choices[0].message.content


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
