from django.urls import path
from .views import (
    TeachersView,
    SelfTeacherDetailsView,
    AvailableFeeDaysView,
    TeacherDetailsView,
)


urlpatterns = [
    path(
        "teachers/",
        TeachersView.as_view(),
        name="teachers",
    ),
    path(
        "teachers/me/",
        SelfTeacherDetailsView.as_view(),
        name="self_teacher_details",
    ),
    path(
        "teachers/available_fee_days/",
        AvailableFeeDaysView.as_view(),
        name="available_fee_days",
    ),
    path(
        "teachers/<int:id>/",
        TeacherDetailsView.as_view(),
        name="teacher_details",
    ),
]
