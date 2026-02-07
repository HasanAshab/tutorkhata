"""
Custom model fields that use ImgBB storage.
"""

from django.db import models
from .storage import ImgBBStorage


class ImgBBImageField(models.ImageField):
    """
    ImageField that automatically uses ImgBB storage.

    Usage:
        class MyModel(models.Model):
            photo = ImgBBImageField(upload_to='photos/')
    """

    def __init__(self, *args, **kwargs):
        kwargs["storage"] = ImgBBStorage()
        super().__init__(*args, **kwargs)
