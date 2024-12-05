from django.contrib.auth.backends import ModelBackend
from .models import User
from django.contrib.auth import get_user_model


class EmailBackend(ModelBackend):
    model = get_user_model()

    def authenticate(self, request, username=None, password=None, **extra_fields):
        try:
            user = self.model.objects.get(email=username, **extra_fields)

            if user.check_password(password):
                return user
        except self.model.DoesNotExist:
            return None

        return None
