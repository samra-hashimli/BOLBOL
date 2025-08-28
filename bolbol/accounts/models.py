from django.db import models
from .validators import validate_phone_number
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _


class UserManager(BaseUserManager):
    """
    Custom user manager where phone_number is the unique identifier
    for authentication instead of usernames.
    """

    use_in_migrations = True

    def create_user(self, phone_number, password=None, **extra_fields):
        if not phone_number:
            raise ValueError("The Phone number must be set")

        user = self.model(phone_number=phone_number, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number, email=None, password=None, **extra_fields):
        if not email:
            raise ValueError("Superuser must have an email address")

        extra_fields.setdefault("email", email) 
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(phone_number, password, **extra_fields)


class User(AbstractUser):
    first_name = None
    last_name = None
    username = None

    phone_number = models.CharField(
        max_length=18,
        unique=True,
        null=True,
        blank=True,
        validators=[validate_phone_number]
    )
    full_name = models.CharField(
        max_length=50,
        blank=True, 
        null=True
    )
    email = models.EmailField(
        "email address", 
        blank=True, 
        null=True, 
        unique=True
    )

    USERNAME_FIELD = "phone_number"
    REQUIRED_FIELDS = ["email"]

    objects = UserManager()
