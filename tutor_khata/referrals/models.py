from django.db import models
from tutor_khata.teachers.models import Teacher


class ReferralCode(models.Model):
    teacher = models.OneToOneField(Teacher, on_delete=models.CASCADE)
    code = models.CharField(max_length=20, unique=True)


class Referral(models.Model):
    referrer = models.ForeignKey(
        Teacher, on_delete=models.CASCADE, related_name="referrals"
    )
    referred = models.OneToOneField(
        Teacher, on_delete=models.CASCADE, related_name="referred_by"
    )

    reward_months = models.PositiveSmallIntegerField(default=1)
    applied = models.BooleanField(default=False)
