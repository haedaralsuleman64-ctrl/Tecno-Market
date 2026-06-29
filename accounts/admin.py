from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, UserProfile
from social_auth.models import SocialAccount

# Register your models here.

class SocialAccountInline(admin.TabularInline):
    model = SocialAccount
    extra = 0
    readonly_fields = ['provider', 'provider_id', 'email', 'name', 'created_at' ]
    can_delete = False

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    inlines = [SocialAccountInline]
    list_display = ['username', 'email', 'first_name', 'last_name', 'plain_password' ,'is_active', 'is_staff', 'social_accounts_count', 'date_joined']
    list_filter = ['is_active', 'is_staff', 'is_superuser', 'date_joined']
    
    fieldsets = UserAdmin.fieldsets + (
        ('معلومات إضافية', {
            'fields': ('phone_number', 'plain_password' ,'address', 'date_of_birth', 'profile_image')
        }),
    )
    readonly_fields = ['plain_password']