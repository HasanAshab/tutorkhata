from django.db import models


class AppSettings(models.Model):
    key = models.CharField(max_length=255, unique=True)
    value = models.TextField()
    modified = models.DateTimeField(auto_now=True)

    @staticmethod
    def get(key, default=None):
        #TODO : Add cache
        try:
            return AppSettings.objects.get(key=key).value
        except AppSettings.DoesNotExist:
            return default

    @staticmethod
    def set(key, value):
        try:
            settings = AppSettings.objects.get(key=key)
            settings.value = value
            settings.save()
        except AppSettings.DoesNotExist:
            AppSettings.objects.create(key=key, value=value)

        return value
