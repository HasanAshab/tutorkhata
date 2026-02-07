from .models import Feature, PlanFeature, FeatureUsage


def get_feature_monthly_limit(teacher, feature):
    """Get the monthly limit for a feature
    based on teacher's subscription plan."""
    if hasattr(teacher, "subscription"):
        plan_feature = PlanFeature.objects.filter(
            plan=teacher.subscription.plan, feature=feature
        ).first()
        return plan_feature.monthly_limit if plan_feature else None
    return None


def get_feature_usage(teacher, feature):
    """Get current usage count for a feature."""
    usage = FeatureUsage.objects.filter(
        teacher=teacher, feature=feature
    ).first()
    return usage.used if usage else 0


def get_feature_remaining(teacher, feature):
    """Get remaining usage for a feature."""
    monthly_limit = get_feature_monthly_limit(teacher, feature)
    if monthly_limit is None:
        return None
    used = get_feature_usage(teacher, feature)
    return max(0, monthly_limit - used)


def can_use_feature(teacher, feature_code):
    """
    Check if a teacher can use a specific feature.

    Returns:
        dict: {
            "can_use": bool,
            "reason": str,
            "feature": str,
            "used": int (optional),
            "limit": int or None (optional),
            "remaining": int or None (optional),
        }
    """
    try:
        feature = Feature.objects.get(code=feature_code)
    except Feature.DoesNotExist:
        return {
            "can_use": False,
            "reason": "Feature not found",
            "feature": feature_code,
        }

    # Check if teacher has subscription
    if not hasattr(teacher, "subscription"):
        return {
            "can_use": False,
            "reason": "No active subscription",
            "feature": feature_code,
        }

    # Check if feature is in plan
    plan_feature = PlanFeature.objects.filter(
        plan=teacher.subscription.plan, feature=feature
    ).first()

    if not plan_feature:
        return {
            "can_use": False,
            "reason": "Feature not included in your plan",
            "feature": feature_code,
        }

    # Check usage limit
    if plan_feature.monthly_limit is None:
        return {
            "can_use": True,
            "reason": "Unlimited usage",
            "feature": feature_code,
            "used": 0,
            "limit": None,
        }

    # Get current usage
    used = get_feature_usage(teacher, feature)

    if used >= plan_feature.monthly_limit:
        return {
            "can_use": False,
            "reason": "Monthly limit reached",
            "feature": feature_code,
            "used": used,
            "limit": plan_feature.monthly_limit,
            "remaining": 0,
        }

    return {
        "can_use": True,
        "reason": "Within usage limit",
        "feature": feature_code,
        "used": used,
        "limit": plan_feature.monthly_limit,
        "remaining": plan_feature.monthly_limit - used,
    }


def get_feature_usage_details(teacher, feature):
    """
    Get detailed usage information for a feature.

    Returns:
        dict: {
            "feature": Feature object,
            "used": int,
            "monthly_limit": int or None,
            "remaining": int or None,
            "last_reset_at": datetime or None,
        }
    """
    usage = FeatureUsage.objects.filter(
        teacher=teacher, feature=feature
    ).first()
    monthly_limit = get_feature_monthly_limit(teacher, feature)

    if usage:
        return {
            "feature": feature,
            "used": usage.used,
            "monthly_limit": monthly_limit,
            "remaining": (
                max(0, monthly_limit - usage.used) if monthly_limit else None
            ),
            "last_reset_at": usage.last_reset_at,
        }

    return {
        "feature": feature,
        "used": 0,
        "monthly_limit": monthly_limit,
        "remaining": monthly_limit,
        "last_reset_at": None,
    }
