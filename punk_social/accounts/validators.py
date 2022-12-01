from django.core.exceptions import ValidationError
from django.contrib.auth.models import User

def validate_email(value):
    if User.objects.filter(email = value).exists():
        raise ValidationError(
            ("An account exists with this email. Please enter a unique email."),
            params = {'value':value}
        )
