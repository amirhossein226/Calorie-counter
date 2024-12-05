from django.db import models
from django.contrib.auth.models import AbstractUser
from accounts.constants import ACTIVITY_LEVEL
from .managers import CustomUserManager
# Create your models here.


class User(AbstractUser):
    username = models.CharField(
        max_length=50, unique=False, blank=True, null=True)
    email = models.EmailField(
        max_length=254, unique=True, null=False, blank=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]
    objects = CustomUserManager()

    def __str__(self):
        return self.email

    def full_name(self):
        return f"{self.first_name} {self.last_name}"


class Profile(models.Model):
    name = models.CharField(max_length=50, blank=True)
    user_id = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="profile")

    age = models.PositiveIntegerField(null=True, blank=True)
    weight = models.PositiveIntegerField(null=True, blank=True)
    height = models.PositiveIntegerField(null=True, blank=True)
    daily_calorie_goal = models.PositiveIntegerField(null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    activity_level = models.IntegerField(choices=ACTIVITY_LEVEL, null=True)
    picture = models.ImageField(null=True, blank=True)

    def __str__(self):
        return self.name
