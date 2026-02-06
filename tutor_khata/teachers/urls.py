from django.urls import path
from .views import (
    TeachersView,
    TeacherDetailsView,
    SelfTeacherDetailsView,
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
    path(
        "teachers/me/",
        SelfTeacherDetailsView.as_view(),
        name="self_teacher_details",
    ),
]
