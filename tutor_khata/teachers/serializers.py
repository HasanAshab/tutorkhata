from django.urls import reverse
from rest_framework import serializers
from drf_spectacular.utils import extend_schema_field, inline_serializer
from tutor_khata.accounts.models import User
from .models import Teacher
from .mixins import TeacherAvatarLinkSerializerMixin
from .utils import is_day_available_for_fee


class TeacherListSerializer(
    TeacherAvatarLinkSerializerMixin,
    serializers.ModelSerializer,
):
    class Meta:
        model = Teacher
        fields = (
            "id",
            "name",
            "links",
        )

    @extend_schema_field(
        inline_serializer(
            name="TeacherListLinks",
            fields={
                "self": serializers.URLField(),
                "avatar": serializers.URLField(allow_null=True),
            },
        )
    )
    def get_links(self, teacher):
        profile_url = reverse(
            "teacher_details", kwargs={"id": teacher.id}
        )

        return {
            **super().get_links(teacher),
            "self": profile_url,
        }


class TeacherDetailsSerializer(
    TeacherAvatarLinkSerializerMixin,
    serializers.ModelSerializer,
):
    class Meta:
        model = Teacher
        fields = (
            "id",
            "name",
            "links",
        )



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "phone_number",
            "phone_number_verified",
        )


class SelfTeacherDetailsSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Teacher
        fields = (
            "id",
            "name",
            "avatar",
            "fee_day",
            "sms_tokens_count",
            "free_sms_tokens_count",
            "user",
        )
        read_only_fields = (
            "sms_tokens_count",
            "free_sms_tokens_count",
        )

    def validate_fee_day(self, value):
        if not is_day_available_for_fee(value):
            raise serializers.ValidationError("Huge number of teachers are taking fees on this day! Please choose another day.")
        return value
