from .services import gpt
from .serializers import CharacterSerializer, ChatSerializer
from .models import Character, Chat

from rest_framework.views import APIView
from rest_framework.response import Response

class CharacterInfoAPI(APIView):
    def get(self, request):
        serializer = CharacterSerializer(Character.objects.first())
        return Response(serializer.data)

