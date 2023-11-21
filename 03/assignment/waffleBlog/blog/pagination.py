from rest_framework.pagination import CursorPagination


class CustomCursorPagination(CursorPagination):
    ordering = '-created.at'
    page_size = 10