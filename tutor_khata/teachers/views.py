from rest_framework.permissions import (
    IsAuthenticated,
)
from rest_framework.generics import (
    ListAPIView,
    RetrieveAPIView,
    RetrieveUpdateAPIView,
)
from rest_framework import filters
from rest_framework.views import APIView
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema

from .utils import get_available_fee_days
from .models import Teacher
from .serializers import (
    TeacherListSerializer,
    TeacherDetailsSerializer,
    SelfTeacherDetailsSerializer,
    AvailableFeeDaysSerializer,
)


class TeachersView(ListAPIView):
    permission_classes = (IsAuthenticated,)
    filter_backends = (filters.SearchFilter,)
    queryset = Teacher.objects.all()
    serializer_class = TeacherListSerializer
    search_fields = ("name",)


class SelfTeacherDetailsView(RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = SelfTeacherDetailsSerializer

    def get_object(self):
        return self.request.user.teacher


class AvailableFeeDaysView(APIView):
    permission_classes = (IsAuthenticated,)

    @extend_schema(
        responses=AvailableFeeDaysSerializer
    )
    def get(self, request):
        return Response({
            "days": list(get_available_fee_days())
        })


   
class TeacherDetailsView(RetrieveAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Teacher.objects.all()
    lookup_field = "id"
    serializer_class = TeacherDetailsSerializer
