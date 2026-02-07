from django.utils import timezone
from datetime import timedelta
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_spectacular.utils import extend_schema

from .models import Plan, Subscription, FeatureUsage, Feature
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
from .utils import can_use_feature, get_feature_usage_details


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

    @extend_schema(
        responses={
            status.HTTP_200_OK: SubscriptionSerializer,
            status.HTTP_404_NOT_FOUND: None,
        }
    )
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

    @extend_schema(
        request=SubscriptionCreateSerializer,
        responses={
            status.HTTP_201_CREATED: SubscriptionSerializer,
            status.HTTP_400_BAD_REQUEST: None,
        },
    )
    def post(self, request):
        # Check if teacher already has a subscription
        if hasattr(request.user.teacher, "subscription"):
            return Response(
                {"detail": "You already have an active subscription"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = SubscriptionCreateSerializer(data=request.data)
        if serializer.is_valid():
            price = serializer.validated_data["price"]
            plan = price.plan

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

    @extend_schema(
        request=SubscriptionUpdateSerializer,
        responses={
            status.HTTP_200_OK: SubscriptionSerializer,
            status.HTTP_400_BAD_REQUEST: None,
        },
    )
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

    @extend_schema(
        responses={
            status.HTTP_200_OK: None,
            status.HTTP_404_NOT_FOUND: None,
        }
    )
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
                "at the end of the current period"
            }
        )


class SubscriptionRenewView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        responses={
            status.HTTP_200_OK: None,
            status.HTTP_404_NOT_FOUND: None,
        }
    )
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
            usage_details = get_feature_usage_details(
                request.user.teacher, feature
            )
            return Response(
                {
                    "feature": FeatureSerializer(feature).data,
                    "used": usage_details["used"],
                    "monthly_limit": usage_details["monthly_limit"],
                    "remaining": usage_details["remaining"],
                    "last_reset_at": usage_details["last_reset_at"],
                }
            )


class FeatureCheckView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = FeatureCheckSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )

        feature_code = serializer.validated_data["feature_code"]
        result = can_use_feature(request.user.teacher, feature_code)

        return Response(result)
