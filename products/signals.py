from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from .models import Product

@receiver(post_migrate)
def create_groups_and_permissions(sender, **kwargs):
    # إنشاء مجموعة للمسؤولين
    admins_group, created = Group.objects.get_or_create(name='Admins')
    
    # إنشاء مجموعة للبائعين
    vendors_group, created = Group.objects.get_or_create(name='Vendors')
    
    # إنشاء مجموعة للعملاء
    customers_group, created = Group.objects.get_or_create(name='Customers')
    
    # الحصول على نوع محتوى المنتج
    content_type = ContentType.objects.get_for_model(Product)
    
    # الحصول على جميع الصلاحيات المتعلقة بالمنتج
    permissions = Permission.objects.filter(content_type=content_type)
    
    # منح جميع صلاحيات المنتج للمسؤولين
    admins_group.permissions.set(permissions)
    
    # منح صلاحيات محدودة للبائعين
    vendor_permissions = permissions.filter(
        codename__in=['add_product', 'change_product', 'view_product']
    )
    vendors_group.permissions.set(vendor_permissions)
    
    # منح صلاحية العرض فقط للعملاء
    view_permission , created = permissions.get_or_create(codename='view_product' , defaults={'name': 'Can view product', 'content_type': content_type})
    customers_group.permissions.add(view_permission)