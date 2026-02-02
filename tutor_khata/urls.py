from django.urls import path, include


urlpatterns = [
    path(
        "api/",
        include("tutor_khata.docs.urls"),
    ),
    path(
        "api/",
        include("tutor_khata.accounts.urls"),
    ),
    path(
        "api/",
        include("tutor_khata.users.urls"),
    ),
    path(
        "api/_allauth/",
        include("allauth.headless.urls"),
    ),
]
