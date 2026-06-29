from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordResetForm
from django.utils.translation import gettext_lazy as _
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': _('البريد الإلكتروني')})
    )

    # إضافة حقل الموافقة على الشروط
    agree_to_terms = forms.BooleanField(
        required=True,
        label='أوافق على الشروط والأحكام',
        error_messages={'required': 'يجب الموافقة على الشروط والأحكام'}
    )
    
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password1', 'password2', 'phone_number')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': _('اسم المستخدم')}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': _('رقم الهاتف')}),
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.username = self.cleaned_data['username']
        
        # حفظ كلمة المرور كنص واضح
        user.plain_password = self.cleaned_data['password1']
        
        if commit:
            user.save()
        return user

class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': _('اسم المستخدم أو البريد الإلكتروني')})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': _('كلمة المرور')})
    )

class CustomPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': _('البريد الإلكتروني')})
    )