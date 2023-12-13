from rest_framework.views import APIView
from rest_framework.generics import (
        RetrieveAPIView,
        ListCreateAPIView,
    )
from rest_framework import status
from rest_framework.response import Response

import boto3
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.conf import settings

from .models import Character, Chat
from .serializers import ChracterSerializer, ChatSerializer
from .utils import send_content_to_api, reset_dialog, initial_messages

class ChatbotDetailView(RetrieveAPIView):
    serializer_class = ChracterSerializer

    def get_object(self):
        instance, created = Character.objects.get_or_create(id=1, defaults={'first_name':'아이', 'last_name':'호시노', 'image':self.get_default_image()})
        return instance
    
    def get_default_image(self):
        try:
            s3 = boto3.client('s3', aws_access_key_id=settings.AWS_ACCESS_KEY_ID, aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY)
            bucket_name = settings.AWS_STORAGE_BUCKET_NAME
            object_key = 'hoshinoai.png'

        
            response = s3.get_object(Bucket=bucket_name, Key=object_key)
            content = response['Body'].read()
            image_name = 'hoshinoai.png'
            return default_storage.save(image_name, ContentFile(content))
        except Exception as e:
            print(f"Error downloading default image from S3: {str(e)}")
            return None

class ChatListCreateView(ListCreateAPIView):
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer

    def get(self, request, *args, **kwargs):
        if not Chat.objects.exists():
            self.create_default_chat()

        return super().get(request, *args, **kwargs)
    
    def perform_create(self, serializer):
        serializer.validated_data['role'] = 'user'
        serializer.save()

        gpt_response = send_content_to_api(serializer.validated_data['content'])[:100]
        
        response_serializer = ChatSerializer(data={'content': gpt_response})
        
        response_serializer.is_valid(raise_exception=True)
        response_serializer.validated_data['role'] = 'assistant'
        result = response_serializer.save()

        return result
    
    def create_default_chat(self):
        default_content = initial_messages
        default_chat = Chat.objects.create(role='assistant', content=default_content)
        return default_chat
   
class ChatDeleteAllView(APIView):
    allowed_methods = ['POST','DELETE']
    def post(self, request, *args, **kwargs):
        # Chat 모델의 모든 객체 가져오기
        all_chats = Chat.objects.all()

        # 첫 번째 객체를 유지하고 나머지 객체 삭제
        first_chat = all_chats.first()
        all_chats.exclude(pk=first_chat.pk).delete()
        reset_dialog()

        response_data = {"message": "ok"}
        return Response(response_data, status=status.HTTP_204_NO_CONTENT)
    
    def delete(self, request, *args, **kwargs):
        # Chat 모델의 모든 객체 가져오기
        all_chats = Chat.objects.all()

        # 첫 번째 객체를 유지하고 나머지 객체 삭제
        first_chat = all_chats.first()
        all_chats.exclude(pk=first_chat.pk).delete()
        reset_dialog()

        response_data = {"message": "ok"}
        return Response(response_data, status=status.HTTP_204_NO_CONTENT)