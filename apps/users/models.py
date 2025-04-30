from django.contrib.postgres.fields import ArrayField
from rest_framework_simplejwt.tokens import RefreshToken

from django.db import models

from django.contrib.auth.models import BaseUserManager, PermissionsMixin, AbstractBaseUser


class CustomUserManager(BaseUserManager):
    def create_user(self, number, password=None, **extra_fields):
        if not number:
            raise ValueError("Telefon raqam kiritilishi kerak")
        user = self.model(number=number, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, number, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser uchun is_staff=True bo'lishi kerak.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser uchun is_superuser=True bo'lishi kerak.")

        return self.create_user(number, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    username = None
    number = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=100)
    age = models.IntegerField(null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    arrived = models.BooleanField(default=False)
    hobbies = ArrayField(models.CharField(max_length=100), default=list)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'number'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.number

    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return dict(refresh=str(refresh), access=str(refresh.access_token))
