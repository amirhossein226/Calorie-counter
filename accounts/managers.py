from django.contrib.auth.models import UserManager
from django.db import IntegrityError


class CustomUserManager(UserManager):
    def create_user(self, email, password, **extra_fields):
        if not email or not password:
            raise ValueError("Email/Password required!")

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)

        try:
            user.save()
        except IntegrityError:
            raise ValueError("The user with this information already exist!")
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields["is_staff"] is not True:
            raise ValueError("Superuser must have the is_staff = True!")
        if extra_fields["is_superuser"] is not True:
            raise ValueError("Superuser must have the is_superuser = True!")

        return self.create_user(email, password, **extra_fields)
