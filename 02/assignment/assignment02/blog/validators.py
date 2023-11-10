import string
from django.core.exceptions import ValidationError


def contains_special_character(value):
    for char in value:
        if char in string.punctuation:
            return True
    return False

class PasswordValidator:
    def validate(self, password, user=None):
        if len(password) < 8:
            raise ValidationError("Password length should be over 8")

    def get_help_text(self):
        return "Enter password"
        

def validate_no_special_characters(value):
    if contains_special_character(value):
        raise ValidationError("No special character allowed")


def title_validator(value):
    if len(value) == 0:
        raise ValidationError("Title must include at least one character")
    
def content_validator(value):
    if len(value) == 0:
        raise ValidationError("Content must include at least one character")