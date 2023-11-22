from django.core.exceptions import ValidationError

def validate_for_symbols(text):
   if("#" in text) or ("@" in text) or ('&' in text):
      raise ValidationError('#, @, &를 적는 것 따윈 소용없어.', code='symbol Error')