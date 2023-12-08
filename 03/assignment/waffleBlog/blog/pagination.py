from rest_framework.pagination import CursorPagination


class CustomCursorPagination(CursorPagination):
    ordering = '-created_at'
    page_size = 10