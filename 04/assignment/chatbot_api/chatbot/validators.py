from rest_framework.serializers import ValidationError
from .models import Character


def character_input_validator(value):
    if not Character.objects.filter(name=value).exists():
        raise ValidationError('존재하지 않는 캐릭터명입니다.')
    return value
