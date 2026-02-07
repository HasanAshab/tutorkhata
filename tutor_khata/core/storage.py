"""
Custom storage backend for ImgBB image hosting service.
"""

import base64
import requests
from django.core.files.storage import Storage
from django.core.files.base import ContentFile
from django.conf import settings
from django.utils.deconstruct import deconstructible


@deconstructible
class ImgBBStorage(Storage):
    """
    Custom storage backend that uploads images to ImgBB.com via their API.

    Settings required:
        IMGBB_API_KEY: Your ImgBB API key from https://api.imgbb.com/

    Optional settings:
        IMGBB_EXPIRATION: Default expiration time in seconds (60-15552000)
    """

    def __init__(self, **kwargs):
        self.api_key = kwargs.get("api_key") or getattr(
            settings, "IMGBB_API_KEY", None
        )
        self.api_url = kwargs.get("api_url") or getattr(
            settings, "IMGBB_API_URL", "https://api.imgbb.com/1/upload"
        )
        self.expiration = kwargs.get("expiration") or getattr(
            settings, "IMGBB_EXPIRATION", None
        )

        if not self.api_key:
            raise ValueError(
                "IMGBB_API_KEY is required."
                "Get your API key from https://api.imgbb.com/"
            )

        # Cache for storing uploaded image metadata
        self._uploaded_files = {}

    def _save(self, name, content):
        """
        Save the file to ImgBB and return the name/identifier.
        """
        # Read file content and encode to base64
        content.seek(0)
        image_data = base64.b64encode(content.read()).decode("utf-8")

        # Prepare request data
        data = {
            "key": self.api_key,
            "image": image_data,
            "name": name,
        }

        if self.expiration:
            data["expiration"] = self.expiration

        # Upload to ImgBB
        try:
            response = requests.post(self.api_url, data=data, timeout=30)
            response.raise_for_status()

            result = response.json()

            if not result.get("success"):
                error_msg = result.get("error", {}).get(
                    "message", "Unknown error"
                )
                raise Exception(f"ImgBB upload failed: {error_msg}")

            image_data = result.get("data", {})
            image_id = image_data.get("id")

            if not image_id:
                raise Exception("No image ID returned from ImgBB")

            # Cache the image metadata
            self._uploaded_files[image_id] = {
                "url": image_data.get("url"),
                "display_url": image_data.get("display_url"),
                "url_viewer": image_data.get("url_viewer"),
                "thumb_url": image_data.get("thumb", {}).get("url"),
                "medium_url": image_data.get("medium", {}).get("url"),
                "delete_url": image_data.get("delete_url"),
                "filename": image_data.get("image", {}).get("filename"),
                "size": image_data.get("size"),
                "width": image_data.get("width"),
                "height": image_data.get("height"),
                "mime": image_data.get("image", {}).get("mime"),
                "extension": image_data.get("image", {}).get("extension"),
            }

            return image_id

        except requests.exceptions.RequestException as e:
            raise Exception(f"Failed to upload to ImgBB: {str(e)}")

    def _open(self, name, mode="rb"):
        """
        Retrieve the file from ImgBB.
        """
        url = self.url(name)

        try:
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            return ContentFile(response.content, name=name)
        except requests.exceptions.RequestException as e:
            raise Exception(f"Failed to retrieve file from ImgBB: {str(e)}")

    def exists(self, name):
        """
        Check if a file exists.
        """
        if name in self._uploaded_files:
            return True

        url = self.url(name)
        try:
            response = requests.head(url, timeout=10)
            return response.status_code == 200
        except requests.exceptions.RequestException:
            return False

    def url(self, name):
        """
        Return the URL where the file can be accessed.
        """
        if name in self._uploaded_files:
            return self._uploaded_files[name].get(
                "display_url"
            ) or self._uploaded_files[name].get("url")

        # If not cached, we can't construct the URL without the full data
        # ImgBB uses hash-based URLs
        return f"https://i.ibb.co/{name}"

    def get_direct_url(self, name):
        """
        Get the direct image URL.
        """
        if name in self._uploaded_files:
            return self._uploaded_files[name].get("url")
        return None

    def get_thumbnail_url(self, name):
        """
        Get the thumbnail URL.
        """
        if name in self._uploaded_files:
            return self._uploaded_files[name].get("thumb_url")
        return None

    def get_medium_url(self, name):
        """
        Get the medium size URL.
        """
        if name in self._uploaded_files:
            return self._uploaded_files[name].get("medium_url")
        return None

    def get_delete_url(self, name):
        """
        Get the delete URL for the image.
        """
        if name in self._uploaded_files:
            return self._uploaded_files[name].get("delete_url")
        return None

    def delete(self, name):
        """
        Delete a file from storage.
        Note: ImgBB provides delete URLs but requires visiting them.
        This method removes from cache only.
        """
        if name in self._uploaded_files:
            del self._uploaded_files[name]

    def size(self, name):
        """
        Return the size of the file.
        """
        if name in self._uploaded_files:
            return self._uploaded_files[name].get("size", 0)

        url = self.url(name)
        try:
            response = requests.head(url, timeout=10)
            return int(response.headers.get("Content-Length", 0))
        except Exception:
            return 0

    def get_available_name(self, name, max_length=None):
        """
        Return a filename that's available.
        """
        return name

    def get_valid_name(self, name):
        """
        Return a valid filename for ImgBB.
        """
        return name
