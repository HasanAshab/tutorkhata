from django.urls import path
from .views import (
    TeachersView,
    TeacherDetailsView,
)


urlpatterns = [
    path(
        "teachers/",
        TeachersView.as_view(),
        name="teachers",
    ),
    path(
        "teachers/<int:id>/",
        TeacherDetailsView.as_view(),
        name="teacher_details",
    ),
]
