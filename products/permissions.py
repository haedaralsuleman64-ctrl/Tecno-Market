from rest_framework import permissions

class IsAdminOrReadOnly(permissions.BasePermission):
    """
    صلاحية تسمح للمسؤولين بالتعديل والقراءة للجميع
    """
    def has_permission(self, request, view):
        # السماح بطلبات القراءة للجميع (GET, HEAD, OPTIONS)
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # السماح بطلبات الكتابة للمسؤولين فقط
        return request.user and request.user.is_staff


class IsProductOwnerOrReadOnly(permissions.BasePermission):
    """
    صلاحية تسمح لملاك المنتجات بالتعديل والقراءة للجميع
    """
    def has_object_permission(self, request, view, obj):
        # السماح بطلبات القراءة للجميع
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # السماح بطلبات الكتابة لمالك المنتج فقط
        return obj.owner == request.user


class CanManageInventory(permissions.BasePermission):
    """
    صلاحية للتحكم في المخزون (للمديرين وموظفي المخازن)
    """
    def has_permission(self, request, view):
        return request.user.has_perm('products.manage_inventory')