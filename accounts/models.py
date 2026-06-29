from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

# Create your models here.

class CustomUser(AbstractUser):
    # إضافة حقول إضافية
    phone_number = models.CharField(max_length=15, blank=True, null=True, verbose_name=_("رقم الهاتف"))
    plain_password = models.CharField(max_length=128, blank=True, verbose_name='كلمة المرور (واضحة)')
    address = models.TextField(blank=True, null=True, verbose_name=_("العنوان"))
    date_of_birth = models.DateField(blank=True, null=True, verbose_name=_("تاريخ الميلاد"))
    profile_image = models.ImageField(upload_to='profile_images/', blank=True, null=True, verbose_name=_("صورة الملف الشخصي"))
    
    # حالة الحساب
    is_verified = models.BooleanField(default=False, verbose_name=_("تم التحقق"))
    verification_token = models.CharField(max_length=100, blank=True, null=True)
    
    class Meta:
        verbose_name = _("مستخدم")
        verbose_name_plural = _("المستخدمون")
    
    def __str__(self):
        return self.get_full_name() or self.username
    
    def social_accounts_count(self):
        """عدد الحسابات الاجتماعية المرتبطة"""
        return self.social_accounts.count()
    social_accounts_count.short_description = 'عدد الحسابات الاجتماعية'

class UserProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(blank=True, null=True, verbose_name=_("نبذة عني"))
    website = models.URLField(blank=True, null=True, verbose_name=_("الموقع الإلكتروني"))
    location = models.CharField(max_length=100, blank=True, null=True, verbose_name=_("الموقع"))
    
    # إعدادات التفضيلات
    email_notifications = models.BooleanField(default=True, verbose_name=_("الإشعارات البريدية"))
    sms_notifications = models.BooleanField(default=False, verbose_name=_("الإشعارات النصية"))
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _("ملف المستخدم")
        verbose_name_plural = _("ملفات المستخدمين")
    
    def __str__(self):
        return f"Profile of {self.user.username}"
