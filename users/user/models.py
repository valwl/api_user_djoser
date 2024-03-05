from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from . manager import CustomUserManager


class CustomUser(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)

    email = models.EmailField(null=True, blank=True, unique=True)
    phone_number = models.CharField(max_length=255, null=True, blank=True, unique=True)
    create = models.DateTimeField(auto_now_add=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    objects = CustomUserManager()

    def __str__(self):
        return f'{self.first_name}, {self.pk}'
