from django.conf import settings
from django.dispatch import receiver
from django.contrib.auth.models import (
    AbstractUser,
)
from django.contrib.auth import (
    get_user_model,
)
from django.db import models
from django.utils.translation import (
    gettext_lazy as _,
)
from django.contrib.auth.models import (
    BaseUserManager,
)
from phonenumber_field.modelfields import (
    PhoneNumberField,
)
from tutor_khata.common.utils import LazyProxy


class UserManager(BaseUserManager):
    def create_user(self, phone_number, password=None, **extra_fields):
        if not phone_number:
            raise ValueError("The Phone Number field is required")
        user = self.model(phone_number=phone_number, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(phone_number, password, **extra_fields)

class UserModel(AbstractUser):
    USERNAME_FIELD = "phone_number"
    REQUIRED_FIELDS = []

    objects = UserManager()
    first_name = None
    last_name = None
    username = None
    email = None

    name = models.CharField(
        _("Name"), max_length=255, blank=True, help_text=_("Name of the user")
    )
    phone_number = PhoneNumberField(
        _("Phone Number"),
        unique=True,
        help_text=_("Phone number of the user")
    )
    phone_number_verified = models.BooleanField(
        _("Phone Number Verified"),
        default=False,
        help_text=_("Phone number of the user"),
    )
    avatar = models.ImageField(
        _("Avatar"),
        upload_to="uploads/avatars/",
        max_length=100,
        blank=True,
        help_text=_("Avatar (or profile pic) of the user"),
    )

    class Meta:
        db_table = "users"

    def __str__(self):
        return self.name or str(self.phone_number)

User: UserModel = LazyProxy(get_user_model)
