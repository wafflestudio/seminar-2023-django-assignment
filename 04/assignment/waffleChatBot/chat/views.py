from rest_framework import status
from rest_framework.generics import ListCreateAPIView,RetrieveUpdateDestroyAPIView, CreateAPIView, UpdateAPIView, DestroyAPIView, ListAPIView, GenericAPIView
from rest_framework.response import Response
from .models import Character, Chat
from .openai import create_openai_response
from .serializers import CharacterSerializer, ChatSerializer

class CharacterList(ListAPIView):
    queryset = Character.objects.all()
    serializer_class = CharacterSerializer        
        
class ChatListCreateView(ListCreateAPIView):
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer
    
    def get_queryset(self):
        # Check if there are any chat messages
        if not Chat.objects.exists():
            # Create an initial response from the chatbot
            initial_openai_response = create_openai_response('당신은 누구십니까?')

            # Save the initial chatbot response to the database
            Chat.objects.create(
                role='assistant',
                content=initial_openai_response
            )

        # Return all chat messages ordered by creation time
        return Chat.objects.all().order_by('created_at')
        
    def perform_create(self, serializer):
        user_query = self.request.data.get('content')
        serializer.save(role='user')
        
        chatbot_response_content = create_openai_response(user_query)
        Chat.objects.create(role='assistant', content=chatbot_response_content)
        # assistant_serializer = self.get_serializer(data={'role': 'assistant', 'content': chatbot_response_content})
        # if assistant_serializer.is_valid():
        #     assistant_serializer.save(role='assistant')
        
class ChatDeleteView(GenericAPIView):
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer

    def post(self, request, *args, **kwargs):
        # This method will handle POST requests and delete all chats
        return self.delete_all(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        # Delete all chat records
        self.get_queryset().delete()
        return Response(status=status.HTTP_204_NO_CONTENT)