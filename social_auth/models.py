from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model
from django.utils.html import format_html

class SocialAccount(models.Model):
    PROVIDER_CHOICES = [
        ('google', 'Google'),
    ]
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='social_accounts')
    provider = models.CharField(max_length=20, choices=PROVIDER_CHOICES)
    provider_id = models.CharField(max_length=255)
    email = models.EmailField()
    name = models.CharField(max_length=255)
    picture_url = models.URLField(blank=True, null=True)
    access_token = models.TextField()
    refresh_token = models.TextField(blank=True, null=True)
    expires_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['provider', 'provider_id']
        verbose_name = 'Social account'
        verbose_name_plural = 'Social accounts'

    def __str__(self):
        return f"{self.user.get_full_name() or self.user.username} - {self.get_provider_display()}"

    def get_user_full_name(self):
        """الحصول على الاسم الكامل للمستخدم"""
        return self.user.get_full_name() or self.user.username
    
    def get_user_email(self):
        """الحصول على البريد الإلكتروني للمستخدم"""
        return self.user.email
    
    def profile_picture(self):
        """عرض صورة الملف الشخصي"""
        if self.picture_url:
            return format_html('<img src="{}" width="50" height="50" style="border-radius: 50%;" />', self.picture_url)
        return "لا توجد صورة"