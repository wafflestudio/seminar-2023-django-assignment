from rest_framework import generics, status
from rest_framework.response import Response
from .models import Character, Chat
from .serializers import CharacterSerializer, ChatSerializer
from .openai_utils import generate_openai_response


# Character List는 오직 GET 요청만 받음
class CharacterListView(generics.ListAPIView):
    def get(self, request, *args, **kwargs):
        queryset = Character.objects.all()
        serializer = CharacterSerializer(queryset, many=True)

        # Extract the first item from the serialized data
        character_data = serializer.data[0] if serializer.data else {}

        return Response(character_data)


# GET과 POST를 한 url에서 처리하기 위한 view 구현
class ChatListCreateView(generics.ListCreateAPIView):
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer

    def get(self, request, *args, **kwargs):
        if not Chat.objects.exists():
            initial_openai_response = generate_openai_response("자기소개 해줘.")

            initial_serializer = self.get_serializer(data={'role': 'assistant', 'content': initial_openai_response})
            initial_serializer.is_valid(raise_exception=True)
            initial_serializer.save()

            self.queryset = Chat.objects.all()

        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        user_input = request.data.get('content', '')

        openai_response = generate_openai_response(user_input)

        user_serializer = self.get_serializer(data={'role': 'user', 'content': user_input})
        user_serializer.is_valid(raise_exception=True)
        user_serializer.save()

        assistant_serializer = self.get_serializer(data={'role': 'assistant', 'content': openai_response})
        assistant_serializer.is_valid(raise_exception=True)
        assistant_serializer.save()

        # POST 요청의 response body로 받기 위한 데이터 지정
        assistant_response = Chat.objects.latest('created_at')
        assistant_response_data = self.get_serializer(assistant_response).data

        return Response(assistant_response_data, status=status.HTTP_201_CREATED)


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
