from rest_framework.pagination import (
    CursorPagination,
)


class UserCursorPagination(CursorPagination):
    ordering = ("-rank", "date_joined")
