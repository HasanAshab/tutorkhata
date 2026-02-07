from django.urls import path
from .views import (
    PlansView,
    PlanDetailView,
    MySubscriptionView,
    SubscriptionCreateView,
    SubscriptionUpdateView,
    SubscriptionCancelView,
    SubscriptionRenewView,
    FeatureUsageListView,
    FeatureUsageDetailView,
    FeatureCheckView,
)


urlpatterns = [
    # Plan Management
    path("plans/", PlansView.as_view(), name="plans"),
    path("plans/<int:pk>/", PlanDetailView.as_view(), name="plan-detail"),
    # Subscription Management
    path(
        "subscriptions/me/",
        MySubscriptionView.as_view(),
        name="my-subscription",
    ),
    path(
        "subscriptions/",
        SubscriptionCreateView.as_view(),
        name="subscription-create",
    ),
    path(
        "subscriptions/me/update/",
        SubscriptionUpdateView.as_view(),
        name="subscription-update",
    ),
    path(
        "subscriptions/cancel/",
        SubscriptionCancelView.as_view(),
        name="subscription-cancel",
    ),
    path(
        "subscriptions/renew/",
        SubscriptionRenewView.as_view(),
        name="subscription-renew",
    ),
    # Feature Usage
    path("usage/", FeatureUsageListView.as_view(), name="feature-usage-list"),
    path(
        "usage/<str:feature_code>/",
        FeatureUsageDetailView.as_view(),
        name="feature-usage-detail",
    ),
    path("usage/check/", FeatureCheckView.as_view(), name="feature-check"),
]
