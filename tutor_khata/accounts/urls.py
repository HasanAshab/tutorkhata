from django.urls import path
from .views import (
    ProfileView,
    PhoneNumberView,
)


urlpatterns = [
    path(
        "account/",
        ProfileView.as_view(),
        name="profile",
    ),
    path(
        "account/phone_number/",
        PhoneNumberView.as_view(),
        name="phone_number",
    ),
]
