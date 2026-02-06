from rest_framework.permissions import (
    IsAuthenticated,
)
from rest_framework.generics import (
    ListAPIView,
    RetrieveAPIView,
    RetrieveUpdateAPIView,
)
from rest_framework import filters
from .models import Teacher
from .serializers import (
    TeacherListSerializer,
    TeacherDetailsSerializer,
    SelfTeacherDetailsSerializer
)


class TeachersView(ListAPIView):
    permission_classes = (IsAuthenticated,)
    filter_backends = (filters.SearchFilter,)
    queryset = Teacher.objects.all()
    serializer_class = TeacherListSerializer
    search_fields = ("name",)


class TeacherDetailsView(RetrieveAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Teacher.objects.all()
    lookup_field = "id"
    serializer_class = TeacherDetailsSerializer


class SelfTeacherDetailsView(RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = SelfTeacherDetailsSerializer

    def get_object(self):
        return self.request.user.teacher
