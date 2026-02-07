from rest_framework import serializers
from .models import Plan, Price, PlanFeature, Feature


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


class PlanListSerializer(
    serializers.ModelSerializer,
):
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
