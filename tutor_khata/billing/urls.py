from django.urls import path
from .views import PlansView


urlpatterns = [
    path(
        "plans/",
        PlansView.as_view(),
        name="plans",
    ),
]
