from django.db import models
from ..utils.validators import validate_phone_number
from accounts.models.user_manager import UserManager
from ..utils.masking import mask_fullname
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _


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

    @property
    def masked_fullname(self):
        return mask_fullname(self.full_name) if self.full_name else None
