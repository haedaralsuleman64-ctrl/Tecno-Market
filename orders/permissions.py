from rest_framework import permissions

class IsOrderOwnerOrAdmin(permissions.BasePermission):
    """
    صلاحية تسمح لمالك الطلب أو المسؤولين بالوصول
    """
    def has_object_permission(self, request, view, obj):
        # المسؤولون يمكنهم الوصول إلى جميع الطلبات
        if request.user and request.user.is_staff:
            return True
        
        # المستخدم العادي يمكنه الوصول فقط إلى طلباته
        return obj.user == request.user


class CanChangeOrderStatus(permissions.BasePermission):
    """
    صلاحية لتغيير حالة الطلب (للموظفين المصرح لهم)
    """
    def has_permission(self, request, view):
        return request.user.has_perm('orders.change_order_status')