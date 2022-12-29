from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh_token': str(refresh),
        'access_token': str(refresh.access_token),
    }


def get_new_access_token(refresh_token):
    refresh = RefreshToken(token=refresh_token)
    return str(refresh.access_token)


def get_user_from_token(token):
    token = RefreshToken(token=token)
    try:
        return User.objects.get(id=token.get("user_id"))
    except User.DoesNotExist:
        return None