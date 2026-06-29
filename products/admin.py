from django.contrib import admin
from .models import Category, Product
from django.contrib.auth.models import Group, User

# Register your models here.


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name_ar', 'name_en', 'slug', 'display_order']
    prepopulated_fields = {'slug': ('name',)}
    list_per_page = 20
    search_fields = ['name_ar', 'name_en']

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'price', 'available', 'created']
    list_filter = ['available', 'created', 'category']
    list_editable = ['price', 'available']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name', 'description' , 'owner__username']
    list_per_page = 20
    actions = ['approve_products', 'disapprove_products']

    def approve_products(self, request, queryset):
        queryset.update(is_approved=True)
        self.message_user(request, 'تمت الموافقة على المنتجات المحددة')
    approve_products.short_description = 'الموافقة على المنتجات المحددة'

    def disapprove_products(self, request, queryset):
        queryset.update(is_approved=False)
        self.message_user(request, 'تم رفض المنتجات المحددة')
    disapprove_products.short_description = 'رفض المنتجات المحددة'


# @admin.register(Group)
# class GroupAdmin(admin.ModelAdmin):
#     list_display = ['name', 'get_permissions_count']
    
#     def get_permissions_count(self, obj):
#         return obj.permissions.count()
#     get_permissions_count.short_description = 'عدد الصلاحيات'