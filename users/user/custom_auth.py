from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth import get_user_model
User = get_user_model()


class CustomAuth(BaseAuthentication):
    def authenticate(self, request, login=None, password=None, **kwargs):
        try:
            user = User.objects.get(email=login)
        except User.DoesNotExist:
            try:
                phone_number = User.objects.phone_normalise(login)
                user = User.objects.get(phone_number=phone_number)
            except User.DoesNotExist:
                return None

        if user.check_password(password):
            return user
        else:
            raise AuthenticationFailed('the data is not correct')

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None