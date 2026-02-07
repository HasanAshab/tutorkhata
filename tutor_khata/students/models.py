from django.db import models
from phonenumber_field.modelfields import (
    PhoneNumberField,
)
from tutor_khata.teachers.models import Teacher


class Grade(models.Model):
    slug = models.SlugField(unique=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Batch(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    grade = models.ForeignKey(Grade, on_delete=models.PROTECT)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class GuardianDevice(models.Model):
    owner_name = models.CharField(max_length=100)
    phone_number = PhoneNumberField()
    os_name = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.owner_name


class Student(models.Model):
    guardian_device = models.ForeignKey(
        GuardianDevice, on_delete=models.PROTECT
    )
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    phone_number = PhoneNumberField()
    # avatar

    def __str__(self):
        return self.name
