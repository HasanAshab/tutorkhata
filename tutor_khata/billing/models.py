from django.utils.translation import gettext_lazy as _
from django.db import models
from tutor_khata.teachers.models import Teacher


class Plan(models.Model):
    code = models.CharField(
        _("Code"),
        max_length=50,
        unique=True,
        help_text=_("Unique code for the plan"),
    )
    name = models.CharField(
        _("Name"),
        max_length=100,
        help_text=_("Name of the plan"),
    )
    description = models.TextField(
        _("Description"),
        blank=True,
        help_text=_("Description of the plan"),
    )
    trial_months = models.PositiveSmallIntegerField(
        _("Trial Months"),
        default=0,
        help_text=_("Number of trial months for the plan"),
    )

    def __str__(self):
        return self.name


class Feature(models.Model):
    code = models.CharField(
        _("Code"),
        max_length=100,
        unique=True,
        help_text=_("Unique code for the feature"),
    )
    name = models.CharField(
        _("Name"),
        max_length=100,
        help_text=_("Name of the feature"),
    )

    def __str__(self):
        return self.name


class PlanFeature(models.Model):
    plan = models.ForeignKey(
        Plan,
        on_delete=models.CASCADE,
        verbose_name=_("Plan"),
        help_text=_("Plan associated with this feature"),
    )
    feature = models.ForeignKey(
        Feature,
        on_delete=models.CASCADE,
        verbose_name=_("Feature"),
        help_text=_("Feature included in the plan"),
    )
    monthly_limit = models.PositiveIntegerField(
        _("Monthly Limit"),
        null=True,
        blank=True,
        help_text=_("Monthly usage limit for this feature"),
    )

    class Meta:
        unique_together = ("plan", "feature")

    def __str__(self):
        return f"{self.plan.name}::{self.feature.name}"


class FeatureUsage(models.Model):
    teacher = models.ForeignKey(
        Teacher,
        on_delete=models.CASCADE,
        verbose_name=_("Teacher"),
        help_text=_("Teacher using the feature"),
    )
    feature = models.ForeignKey(
        Feature,
        on_delete=models.CASCADE,
        verbose_name=_("Feature"),
        help_text=_("Feature being tracked"),
    )
    used = models.PositiveIntegerField(
        _("Used"),
        default=0,
        help_text=_("Number of times the feature has been used"),
    )
    last_reset_at = models.DateTimeField(
        _("Last Reset At"),
        help_text=_("Last time the usage counter was reset"),
    )

    class Meta:
        unique_together = ("teacher", "feature")

    def __str__(self):
        return f"{self.teacher}'s {self.feature} usage is {self.used}"


class Price(models.Model):
    plan = models.ForeignKey(
        Plan,
        on_delete=models.CASCADE,
        verbose_name=_("Plan"),
        help_text=_("Plan associated with this price"),
    )
    amount = models.PositiveIntegerField(
        _("Amount"),
        help_text=_("Price amount"),
    )
    currency = models.CharField(
        _("Currency"),
        max_length=10,
        default="BDT",
        help_text=_("Currency code"),
    )
    duration_months = models.PositiveSmallIntegerField(
        _("Duration Months"),
        help_text=_("Duration of the subscription in months"),
    )
    is_active = models.BooleanField(
        _("Is Active"),
        default=True,
        help_text=_("Whether this price is currently active"),
    )


class Subscription(models.Model):
    class Status(models.TextChoices):
        TRIAL = "trial", _("Trial")
        ACTIVE = "active", _("Active")
        EXPIRED = "expired", _("Expired")

    teacher = models.OneToOneField(
        Teacher,
        on_delete=models.CASCADE,
        related_name="subscription",
        verbose_name=_("Teacher"),
        help_text=_("Teacher who owns this subscription"),
    )
    plan = models.ForeignKey(
        Plan,
        on_delete=models.PROTECT,
        verbose_name=_("Plan"),
        help_text=_("Subscription plan"),
    )
    price = models.ForeignKey(
        Price,
        on_delete=models.PROTECT,
        verbose_name=_("Price"),
        help_text=_("Price for this subscription"),
    )

    trial_ends_at = models.DateTimeField(
        _("Trial Ends At"),
        null=True,
        blank=True,
        help_text=_("Date and time when the trial period ends"),
    )
    ends_at = models.DateTimeField(
        _("Ends At"),
        null=True,
        blank=True,
        help_text=_("Date and time when the subscription ends"),
    )

    status = models.CharField(
        _("Status"),
        max_length=20,
        choices=Status,
        help_text=_("Current status of the subscription"),
    )

    auto_renew = models.BooleanField(
        _("Auto Renew"),
        default=True,
        help_text=_("Whether the subscription should auto-renew"),
    )

    created = models.DateTimeField(
        _("Created"),
        auto_now_add=True,
        help_text=_("Date and time when the subscription was created"),
    )
    modified = models.DateTimeField(
        _("Modified"),
        auto_now=True,
        help_text=_("Date and time when the subscription was last modified"),
    )

    def __str__(self):
        return f"{self.teacher} subscribed to {self.plan}"
