from django.utils import timezone
from datetime import timedelta
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_spectacular.utils import extend_schema

from .models import Plan, Subscription, FeatureUsage, Feature, PlanFeature
from .serializers import (
    PlanListSerializer,
    PlanDetailSerializer,
    SubscriptionSerializer,
    SubscriptionCreateSerializer,
    SubscriptionUpdateSerializer,
    FeatureUsageSerializer,
    FeatureCheckSerializer,
    FeatureSerializer,
)


class PlansView(ListAPIView):
    queryset = Plan.objects.prefetch_related(
        "price_set", "planfeature_set__feature"
    ).all()
    serializer_class = PlanListSerializer


class PlanDetailView(RetrieveAPIView):
    queryset = Plan.objects.prefetch_related(
        "price_set", "planfeature_set__feature"
    ).all()
    serializer_class = PlanDetailSerializer


class MySubscriptionView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(responses=SubscriptionSerializer)
    def get(self, request):
        try:
            subscription = (
                Subscription.objects.select_related("plan", "price")
                .prefetch_related(
                    "plan__price_set", "plan__planfeature_set__feature"
                )
                .get(teacher=request.user.teacher)
            )
            serializer = SubscriptionSerializer(subscription)
            return Response(serializer.data)
        except Subscription.DoesNotExist:
            return Response(
                {"detail": "No active subscription found"},
                status=status.HTTP_404_NOT_FOUND,
            )


class SubscriptionCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # Check if teacher already has a subscription
        if hasattr(request.user.teacher, "subscription"):
            return Response(
                {"detail": "You already have an active subscription"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = SubscriptionCreateSerializer(data=request.data)
        if serializer.is_valid():
            plan = serializer.validated_data["plan"]
            price = serializer.validated_data["price"]

            # Calculate trial and subscription end dates
            now = timezone.now()
            trial_ends_at = None
            ends_at = now + timedelta(days=price.duration_months * 30)

            if plan.trial_months > 0:
                trial_ends_at = now + timedelta(days=plan.trial_months * 30)
                subscription_status = Subscription.Status.TRIAL
            else:
                subscription_status = Subscription.Status.ACTIVE

            # Create subscription
            subscription = Subscription.objects.create(
                teacher=request.user.teacher,
                plan=plan,
                price=price,
                trial_ends_at=trial_ends_at,
                ends_at=ends_at,
                status=subscription_status,
            )

            response_serializer = SubscriptionSerializer(subscription)
            return Response(
                response_serializer.data, status=status.HTTP_201_CREATED
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SubscriptionUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request):
        try:
            subscription = Subscription.objects.get(
                teacher=request.user.teacher
            )
        except Subscription.DoesNotExist:
            return Response(
                {"detail": "No active subscription found"},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = SubscriptionUpdateSerializer(
            subscription, data=request.data, partial=True
        )
        if serializer.is_valid():
            serializer.save()
            response_serializer = SubscriptionSerializer(subscription)
            return Response(response_serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SubscriptionCancelView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            subscription = Subscription.objects.get(
                teacher=request.user.teacher
            )
        except Subscription.DoesNotExist:
            return Response(
                {"detail": "No active subscription found"},
                status=status.HTTP_404_NOT_FOUND,
            )

        subscription.auto_renew = False
        subscription.save()

        return Response(
            {
                "detail": "Subscription will be cancelled"
                " at the end of the current period"
            }
        )


class SubscriptionRenewView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            subscription = Subscription.objects.get(
                teacher=request.user.teacher
            )
        except Subscription.DoesNotExist:
            return Response(
                {"detail": "No active subscription found"},
                status=status.HTTP_404_NOT_FOUND,
            )

        if subscription.status == Subscription.Status.EXPIRED:
            # Renew expired subscription
            now = timezone.now()
            subscription.ends_at = now + timedelta(
                days=subscription.price.duration_months * 30
            )
            subscription.status = Subscription.Status.ACTIVE
            subscription.auto_renew = True
            subscription.save()

            return Response({"detail": "Subscription renewed successfully"})
        else:
            subscription.auto_renew = True
            subscription.save()
            return Response({"detail": "Auto-renewal enabled"})


class FeatureUsageListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        usage = FeatureUsage.objects.filter(
            teacher=request.user.teacher
        ).select_related("feature")
        serializer = FeatureUsageSerializer(usage, many=True)
        return Response(serializer.data)


class FeatureUsageDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, feature_code):
        try:
            feature = Feature.objects.get(code=feature_code)
        except Feature.DoesNotExist:
            return Response(
                {"detail": "Feature not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

        try:
            usage = FeatureUsage.objects.select_related("feature").get(
                teacher=request.user.teacher, feature=feature
            )
            serializer = FeatureUsageSerializer(usage)
            return Response(serializer.data)
        except FeatureUsage.DoesNotExist:
            return Response(
                {
                    "feature": FeatureSerializer(feature).data,
                    "used": 0,
                    "monthly_limit": self._get_monthly_limit(
                        request.user.teacher, feature
                    ),
                    "remaining": self._get_monthly_limit(
                        request.user.teacher, feature
                    ),
                    "last_reset_at": None,
                }
            )

    def _get_monthly_limit(self, teacher, feature):
        if hasattr(teacher, "subscription"):
            plan_feature = PlanFeature.objects.filter(
                plan=teacher.subscription.plan, feature=feature
            ).first()
            return plan_feature.monthly_limit if plan_feature else None
        return None


class FeatureCheckView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = FeatureCheckSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )

        feature_code = serializer.validated_data["feature_code"]
        feature = Feature.objects.get(code=feature_code)
        teacher = request.user.teacher

        # Check if teacher has subscription
        if not hasattr(teacher, "subscription"):
            return Response(
                {
                    "can_use": False,
                    "reason": "No active subscription",
                    "feature": feature_code,
                }
            )

        # Check if feature is in plan
        plan_feature = PlanFeature.objects.filter(
            plan=teacher.subscription.plan, feature=feature
        ).first()

        if not plan_feature:
            return Response(
                {
                    "can_use": False,
                    "reason": "Feature not included in your plan",
                    "feature": feature_code,
                }
            )

        # Check usage limit
        if plan_feature.monthly_limit is None:
            return Response(
                {
                    "can_use": True,
                    "reason": "Unlimited usage",
                    "feature": feature_code,
                    "used": 0,
                    "limit": None,
                }
            )

        # Get current usage
        usage = FeatureUsage.objects.filter(
            teacher=teacher, feature=feature
        ).first()
        used = usage.used if usage else 0

        if used >= plan_feature.monthly_limit:
            return Response(
                {
                    "can_use": False,
                    "reason": "Monthly limit reached",
                    "feature": feature_code,
                    "used": used,
                    "limit": plan_feature.monthly_limit,
                    "remaining": 0,
                }
            )

        return Response(
            {
                "can_use": True,
                "reason": "Within usage limit",
                "feature": feature_code,
                "used": used,
                "limit": plan_feature.monthly_limit,
                "remaining": plan_feature.monthly_limit - used,
            }
        )
