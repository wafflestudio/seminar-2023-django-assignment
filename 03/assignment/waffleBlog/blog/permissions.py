from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # 읽기 권한은 모든 요청에 허용
        if request.method in permissions.SAFE_METHODS:
            return True

        # 쓰기 권한은 해당 객체를 만든 사용자에게만 허용(수정, 삭제)
        return obj.created_by == request.user


class IsAdminOrOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # Allow read-only permissions for any request
        if request.method in permissions.SAFE_METHODS:
            return True

        # Allow admins to perform any action
        if request.user and request.user.is_staff:
            return True

        # Check if the user is the owner of the post or comment
        return obj.created_by == request.user
