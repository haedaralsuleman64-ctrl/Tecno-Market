from django.contrib import admin
from .models import SocialAccount
from django.contrib.auth import get_user_model
from django.utils.html import format_html

# Register your models here.
User = get_user_model()

@admin.register(SocialAccount)
class SocialAccountAdmin(admin.ModelAdmin):
    list_display = ['user_full_name', 'user_email', 'provider', 'provider_id', 'created_at', 'profile_picture']
    list_filter = ['provider', 'created_at']
    search_fields = ['user__username', 'user__first_name', 'user__last_name', 'user__email', 'name', 'provider_id']
    readonly_fields = ['created_at', 'updated_at', 'profile_picture']
    fieldsets = (
        ('معلومات المستخدم', {
            'fields': ('user', )
        }),
        ('معلومات الحساب الاجتماعي', {
            'fields': ('provider', 'provider_id', 'name', 'email', 'picture_url', 'profile_picture')
        }),
        ('معلومات التوكن', {
            'fields': ('access_token', 'refresh_token', 'expires_at'),
            'classes': ('collapse',)
        }),
        ('معلومات إضافية', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def user_full_name(self, obj):
        return obj.user.get_full_name() or obj.user.username
    user_full_name.short_description = 'الاسم الكامل'
    user_full_name.admin_order_field = 'user__first_name'

    def user_email(self, obj):
        return obj.user.email
    user_email.short_description = 'البريد الإلكتروني'
    user_email.admin_order_field = 'user__email'

    def profile_picture(self, obj):
        """عرض صورة الملف الشخصي إذا كانت موجودة"""
        if obj.picture_url:
            return format_html('<img src="{}" width="50" height="50" style="border-radius: 50%;" />', obj.picture_url)
        return "لا توجد صورة"
    profile_picture.short_description = 'صورة الملف'

    def get_readonly_fields(self, request, obj=None):
        if obj:  # عند التعديل على عنصر موجود
            return self.readonly_fields + ['user', 'provider', 'provider_id']
        return self.readonly_fields