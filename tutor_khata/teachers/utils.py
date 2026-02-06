from django.conf import settings
from django.db.models import Count


def get_available_fee_days():
    from .models import Teacher
    from tutor_khata.core.models import AppSettings

    teacher_capacity_per_day = AppSettings.get_number("teacher_capacity_per_day", None)

    # If no capacity limit is set, all days are available
    if not teacher_capacity_per_day:
        return range(1, settings.MAX_FEE_DAY + 1)

    # Count teachers per fee_day
    day_counts = (
        Teacher.objects
        .values("fee_day")
        .annotate(total=Count("id"))
    )

    # Build a lookup: {day: count}
    used_capacity = {item["fee_day"]: item["total"] for item in day_counts}

    available_days = []

    for day in range(1, settings.MAX_FEE_DAY + 1):
        if used_capacity.get(day, 0) < teacher_capacity_per_day:
            available_days.append(day)

    return available_days

def get_best_fee_day():
    return min(get_available_fee_days())

def is_day_available_for_fee(day):
    return day in get_available_fee_days()
