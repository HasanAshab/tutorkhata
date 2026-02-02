from django.urls import path, include


urlpatterns = [
    path(
        "api/",
        include("tutor_khata.docs.urls"),
    ),
    path(
        "api/",
        include("tutor_khata.authentication.urls"),
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
        "api/",
        include("tutor_khata.recent_searches.urls"),
    ),
    path(
        "api/",
        include("tutor_khata.level_titles.urls"),
    ),
    path(
        "api/",
        include("tutor_khata.difficulties.urls"),
    ),
    path(
        "api/",
        include("tutor_khata.challenges.urls"),
    ),
]
