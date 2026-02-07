from rest_framework.generics import (
    ListAPIView,
)
from .models import Plan
from .serializers import (
    PlanListSerializer,
)


class PlansView(ListAPIView):
    queryset = Plan.objects.prefetch_related(
        "price_set", "planfeature_set__feature"
    ).all()
    serializer_class = PlanListSerializer
