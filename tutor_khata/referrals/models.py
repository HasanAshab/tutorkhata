from django.utils.translation import gettext_lazy as _
from django.db import models
from tutor_khata.teachers.models import Teacher


class ReferralCode(models.Model):
    teacher = models.OneToOneField(Teacher, on_delete=models.CASCADE)
    code = models.CharField(
        _("Code"),
        max_length=20,
        unique=True,
        help_text=_("Referral code"),
    )


class Referral(models.Model):
    referrer = models.ForeignKey(
        Teacher, on_delete=models.CASCADE, related_name="referrals"
    )
    referred = models.OneToOneField(
        Teacher, on_delete=models.CASCADE, related_name="referred_by"
    )

    reward_months = models.PositiveSmallIntegerField(
        _("Reward Months"),
        default=1,
        help_text=_("Number of months to reward"),
    )
    applied = models.BooleanField(
        _("Applied"),
        default=False,
        help_text=_("Whether the reward has been applied"),
    )
