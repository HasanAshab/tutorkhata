from django.contrib import admin
from .models import (
    Plan,
    Price,
    Subscription,
    PlanFeature,
    FeatureUsage,
    Feature,
)


admin.site.register(Plan)
admin.site.register(Price)
admin.site.register(Subscription)
admin.site.register(PlanFeature)
admin.site.register(FeatureUsage)
admin.site.register(Feature)
