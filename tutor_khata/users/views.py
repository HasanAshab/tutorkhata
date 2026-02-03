from rest_framework.permissions import (
    IsAuthenticated,
)
from rest_framework.generics import (
    ListAPIView,
    RetrieveDestroyAPIView,
)
from rest_framework import filters
from .models import User
from .permissions import DeleteUserPermission
from .serializers import (
    UserListSerializer,
    UserDetailsSerializer,
)
from .pagination import UserCursorPagination


class UsersView(ListAPIView):
    permission_classes = (IsAuthenticated,)
    filter_backends = (filters.SearchFilter,)
    queryset = User.objects.all()
    serializer_class = UserListSerializer
    # pagination_class = UserCursorPagination
    search_fields = ("name", "phone_number")


class UserDetailsView(RetrieveDestroyAPIView):
    permission_classes = (IsAuthenticated, DeleteUserPermission)
    queryset = User.objects.all()
    lookup_field = "id"
    serializer_class = UserDetailsSerializer
