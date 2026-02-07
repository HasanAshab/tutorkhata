from rest_framework import serializers
from .models import (
    Plan,
    Price,
    PlanFeature,
    Feature,
    Subscription,
    FeatureUsage,
)


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
    plan = PlanListSerializer(read_only=True)
    price = PriceSerializer(read_only=True)

    class Meta:
        model = Subscription
        fields = (
            "id",
            "plan",
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
    plan_id = serializers.IntegerField()
    price_id = serializers.IntegerField()

    def validate(self, data):
        try:
            plan = Plan.objects.get(id=data["plan_id"])
        except Plan.DoesNotExist:
            raise serializers.ValidationError({"plan_id": "Plan not found"})

        try:
            price = Price.objects.get(
                id=data["price_id"], plan=plan, is_active=True
            )
        except Price.DoesNotExist:
            raise serializers.ValidationError(
                {"price_id": "Price not found or not active for this plan"}
            )

        data["plan"] = plan
        data["price"] = price
        return data


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
        teacher = obj.teacher
        if hasattr(teacher, "subscription"):
            plan_feature = PlanFeature.objects.filter(
                plan=teacher.subscription.plan, feature=obj.feature
            ).first()
            return plan_feature.monthly_limit if plan_feature else None
        return None

    def get_remaining(self, obj):
        monthly_limit = self.get_monthly_limit(obj)
        if monthly_limit is None:
            return None
        return max(0, monthly_limit - obj.used)


class FeatureCheckSerializer(serializers.Serializer):
    feature_code = serializers.CharField()

    def validate_feature_code(self, value):
        try:
            Feature.objects.get(code=value)
        except Feature.DoesNotExist:
            raise serializers.ValidationError("Feature not found")
        return value
