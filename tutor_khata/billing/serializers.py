from rest_framework import serializers
from .models import (
    Plan,
    Price,
    PlanFeature,
    Feature,
    Subscription,
    FeatureUsage,
)
from .utils import get_feature_monthly_limit, get_feature_remaining


class FeatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feature
        fields = (
            "id",
            "code",
            "name",
        )


class PlanFeatureSerializer(serializers.ModelSerializer):
    feature = FeatureSerializer(read_only=True)

    class Meta:
        model = PlanFeature
        fields = (
            "id",
            "feature",
            "monthly_limit",
        )


class PriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Price
        fields = (
            "id",
            "amount",
            "currency",
            "duration_months",
            "is_active",
        )


class PlanListSerializer(serializers.ModelSerializer):
    prices = PriceSerializer(many=True, read_only=True, source="price_set")
    features = PlanFeatureSerializer(
        many=True, read_only=True, source="planfeature_set"
    )

    class Meta:
        model = Plan
        fields = (
            "id",
            "code",
            "name",
            "description",
            "trial_months",
            "prices",
            "features",
        )


class PlanDetailSerializer(serializers.ModelSerializer):
    prices = PriceSerializer(many=True, read_only=True, source="price_set")
    features = PlanFeatureSerializer(
        many=True, read_only=True, source="planfeature_set"
    )

    class Meta:
        model = Plan
        fields = (
            "id",
            "code",
            "name",
            "description",
            "trial_months",
            "prices",
            "features",
        )


class SubscriptionSerializer(serializers.ModelSerializer):
    price = PriceSerializer(read_only=True)

    class Meta:
        model = Subscription
        fields = (
            "id",
            "plan_id",
            "price",
            "trial_ends_at",
            "ends_at",
            "status",
            "auto_renew",
            "created",
            "modified",
        )
        read_only_fields = (
            "id",
            "trial_ends_at",
            "ends_at",
            "status",
            "created",
            "modified",
        )


class SubscriptionCreateSerializer(serializers.Serializer):
    price = serializers.PrimaryKeyRelatedField(
        queryset=Price.objects.select_related("plan").filter(is_active=True)
    )


class SubscriptionUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = ("auto_renew",)


class FeatureUsageSerializer(serializers.ModelSerializer):
    feature = FeatureSerializer(read_only=True)
    monthly_limit = serializers.SerializerMethodField()
    remaining = serializers.SerializerMethodField()

    class Meta:
        model = FeatureUsage
        fields = (
            "id",
            "feature",
            "used",
            "monthly_limit",
            "remaining",
            "last_reset_at",
        )

    def get_monthly_limit(self, obj):
        return get_feature_monthly_limit(obj.teacher, obj.feature)

    def get_remaining(self, obj):
        return get_feature_remaining(obj.teacher, obj.feature)


class FeatureCheckSerializer(serializers.Serializer):
    feature_code = serializers.CharField()

    def validate_feature_code(self, value):
        try:
            Feature.objects.get(code=value)
        except Feature.DoesNotExist:
            raise serializers.ValidationError("Feature not found")
        return value
