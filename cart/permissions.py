from rest_framework import permissions

class IsCartOwner(permissions.BasePermission):
    """
    صلاحية تسمح لمالك العربة فقط بالوصول
    """
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user


class CanModifyCart(permissions.BasePermission):
    """
    صلاحية للتعديل على العربة (للمستخدمين المسجلين فقط)
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated