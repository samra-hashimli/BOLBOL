import re 

from django.core.exceptions import ValidationError


def validate_phone_number(value):
    """
    Validate Azerbaijani phone numbers in the format +994XXXXXXXXX
    (+994 followed by exactly 9 digits).
    """
    pattern = r'^\+994\d{9}$'

    if not re.match(pattern, value):
        raise ValidationError("Phone number must be in the format: +994XXXXXXXXX")
