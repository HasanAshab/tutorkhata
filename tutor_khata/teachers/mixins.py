from rest_framework import serializers
from drf_spectacular.utils import extend_schema_field, inline_serializer


class TeacherAvatarLinkSerializerMixin(metaclass=serializers.SerializerMetaclass):
    links = serializers.SerializerMethodField()

    @extend_schema_field(
        inline_serializer(
            name="TeacherAvatarLink",
            fields={
                "avatar": serializers.URLField(allow_null=True),
            },
        )
    )
    def get_links(self, teacher):
        return {
            "avatar": teacher.avatar if teacher.avatar else None,
        }
