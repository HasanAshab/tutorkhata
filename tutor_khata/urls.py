from django.urls import path, include


urlpatterns = [
    path(
        "api/",
        include("tutor_khata.docs.urls"),
    ),
    path(
        "api/",
        include("tutor_khata.teachers.urls"),
    ),
    path(
        "api/_allauth/",
        include("allauth.headless.urls"),
    ),
]
