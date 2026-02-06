from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.dispatch import receiver
from django.utils.translation import (
    gettext_lazy as _,
)
from tutor_khata.core.models import AppSettings
from .utils import get_best_fee_day

class Teacher(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    name = models.CharField(
        _("Name"), max_length=255, blank=True, help_text=_("Name of the teacher")
    )

    avatar = models.ImageField(
        _("Avatar"),
        upload_to="uploads/avatars/",
        max_length=100,
        blank=True,
        help_text=_("Avatar (or profile pic) of the teacher"),
    )

    fee_day = models.PositiveSmallIntegerField(
        _("Fee Day"),
        help_text=_("Day of the month to take the fee"),
        validators=[
            MinValueValidator(1),
            MaxValueValidator(25),
        ]
    )

    sms_tokens_count = models.PositiveSmallIntegerField(
        _("SMS Tokens Count"),
        help_text=_("Number of SMS tokens the teacher has"),
        default=0,
    )
    
    free_sms_tokens_count = models.PositiveSmallIntegerField(
        _("Free SMS Tokens Count"),
        help_text=_("Number of Free SMS tokens the teacher has"),
        default=0,
    )

    def __str__(self):
        return self.name


@receiver(
    models.signals.post_save,
    sender=settings.AUTH_USER_MODEL,
    dispatch_uid="create_teacher",
)
def create_teacher(sender, instance, created, **kwargs):
    if not created: return

    monthly_free_sms_tokens_count = AppSettings.get("monthly_free_sms_tokens_count", 0)
    Teacher.objects.create(
        user=instance,
        fee_day=get_best_fee_day(),
        free_sms_tokens_count=monthly_free_sms_tokens_count
    )
