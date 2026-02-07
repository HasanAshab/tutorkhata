from django.utils.translation import gettext_lazy as _
from django.db import models
from tutor_khata.teachers.models import Teacher


class Plan(models.Model):
    code = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    trial_months = models.PositiveSmallIntegerField(default=0)

    def __str__(self):
        return self.name


class Feature(models.Model):
    code = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class PlanFeature(models.Model):
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE)
    feature = models.ForeignKey(Feature, on_delete=models.CASCADE)
    monthly_limit = models.PositiveIntegerField(null=True, blank=True)

    class Meta:
        unique_together = ("plan", "feature")

    def __str__(self):
        return f"{self.plan.name}::{self.feature.name}"


class FeatureUsage(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    feature = models.ForeignKey(Feature, on_delete=models.CASCADE)
    used = models.PositiveIntegerField(default=0)
    last_reset_at = models.DateTimeField()

    class Meta:
        unique_together = ("teacher", "feature")

    def __str__(self):
        return f"{self.teacher}'s {self.feature} usage is {self.used}"


class Price(models.Model):
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE)
    amount = models.PositiveIntegerField()
    currency = models.CharField(max_length=10, default="BDT")
    duration_months = models.PositiveSmallIntegerField()
    is_active = models.BooleanField(default=True)


class Subscription(models.Model):
    class Status(models.TextChoices):
        TRIAL = "trial", _("Trial")
        ACTIVE = "active", _("Active")
        EXPIRED = "expired", _("Expired")

    teacher = models.OneToOneField(
        Teacher, on_delete=models.CASCADE, related_name="subscription"
    )
    plan = models.ForeignKey(Plan, on_delete=models.PROTECT)
    price = models.ForeignKey(Price, on_delete=models.PROTECT)

    trial_ends_at = models.DateTimeField(null=True, blank=True)
    ends_at = models.DateTimeField(null=True, blank=True)

    status = models.CharField(
        max_length=20,
        choices=Status,
    )

    auto_renew = models.BooleanField(default=True)

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.teacher} subscribed to {self.plan}"
