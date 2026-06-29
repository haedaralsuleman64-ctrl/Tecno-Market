import requests
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth import get_user_model
from django.conf import settings
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json
from .models import SocialAccount
import urllib.parse
import secrets
from django.core.cache import cache
from django.views.decorators.csrf import csrf_protect

# Create your views here.

def generate_state_parameter():
    """إنشاء state parameter فريد لـ CSRF protection"""
    state = secrets.token_urlsafe(16)
    # حفظ state في cache لمدة 10 دقائق
    cache.set(f'oauth_state_{state}', True, timeout=600)
    return state

def validate_state_parameter(state):
    """التحقق من صحة state parameter"""
    if not state:
        return False
    return cache.get(f'oauth_state_{state}') is not None


def google_login(request):
    """توجيه المستخدم إلى صفحة مصادقة Google"""
    try:
         # تحقق متقدم من الإعدادات
        if not settings.GOOGLE_CLIENT_ID or settings.GOOGLE_CLIENT_ID in ['', 'your_actual_google_client_id_here']:
            return render(request, 'social_auth/error.html', {
                'error_message': 'إعدادات المصادقة مع Google غير مضبوطة. يرجى الاتصال بمدير النظام.'
            })
        
        print("=== Google Login Started ===")
        print(f"GOOGLE_CLIENT_ID: {settings.GOOGLE_CLIENT_ID}")
        print(f"GOOGLE_REDIRECT_URI: {settings.GOOGLE_REDIRECT_URI}")

        base_url = "https://accounts.google.com/o/oauth2/v2/auth"
        state = generate_state_parameter()
        
        params = {
            'client_id': settings.GOOGLE_CLIENT_ID,
            'redirect_uri': settings.GOOGLE_REDIRECT_URI, 
            'response_type': 'code',
            'scope': 'openid email profile',
            'state': state,
            'access_type': 'online',
            'prompt': 'select_account',
        }
        auth_url = f"{base_url}?{urllib.parse.urlencode(params)}"
        print(f"Generated Auth URL: {auth_url}")
        return redirect(auth_url)
    
    except Exception as e:
        print(f"Google Login Error: {str(e)}")
        return render(request, 'social_auth/error.html', {
            'error_message': f'خطأ في المصادقة: {str(e)}'
        })


@require_http_methods(["GET"])
def google_callback(request):
    """معالجة استجابة Google بعد المصادقة"""
    try:
        code = request.GET.get('code')
        error = request.GET.get('error')
        state = request.GET.get('state')
        
        print(f"Google callback received. Code: {code}, Error: {error}, State: {state}")
        
        # التحقق من state parameter (أضف هذا التحقق)
        if not validate_state_parameter(state):
            return render(request, 'social_auth/error.html', {
                'error_message': 'معلمة التحقق غير صالحة أو منتهية الصلاحية'
            })
        
        if error:
            error_description = request.GET.get('error_description', '')
            return render(request, 'social_auth/error.html', {
                'error_message': f'فشل المصادقة مع Google: {error} - {error_description}'
            })
        
        if not code:
            return render(request, 'social_auth/error.html', {
                'error_message': 'لم يتم استلام رمز المصادقة من Google'
            })
        
        # استبدل code بـ access token
        token_url = "https://oauth2.googleapis.com/token"
        token_data = {
            'client_id': settings.GOOGLE_CLIENT_ID,
            'client_secret': settings.GOOGLE_CLIENT_SECRET,
            'redirect_uri': settings.GOOGLE_REDIRECT_URI,
            'code': code,
            'grant_type': 'authorization_code'
        }
        
        token_response = requests.post(token_url, data=token_data)
        
        print(f"Google token response status: {token_response.status_code}")
        print(f"Google token response content: {token_response.text}")
        
        if token_response.status_code != 200:
            return render(request, 'social_auth/error.html', {  # غير HttpResponse إلى render
                'error_message': f'فشل في الحصول على access token: {token_response.text}'
            })
        
        token_info = token_response.json()
        
        if 'access_token' not in token_info:
            return render(request, 'social_auth/error.html', {
                'error_message': 'لم يتم استلام access token من Google'
            })
        
        # الحصول على معلومات المستخدم
        user_info_url = "https://www.googleapis.com/oauth2/v3/userinfo"
        headers = {'Authorization': f'Bearer {token_info["access_token"]}'}
        
        user_response = requests.get(user_info_url, headers=headers)
        
        print(f"Google user info response status: {user_response.status_code}")
        print(f"Google user info content: {user_response.text}")
        
        if user_response.status_code != 200:
            return render(request, 'social_auth/error.html', {
                'error_message': f'فشل في الحصول على معلومات المستخدم: {user_response.text}'
            })
        
        user_info = user_response.json()
        print(f"User info: {user_info}")  # أضف هذا للسجل
        
        # البحث عن حساب موجود أو إنشاء حساب جديد
        try:
            social_account = SocialAccount.objects.get(
                provider='google', 
                provider_id=user_info['sub']
            )
            user = social_account.user
            login(request, user)
            return redirect('/')
            
        except SocialAccount.DoesNotExist:
            # إنشاء مستخدم جديد
            email = user_info.get('email')
            if not email:
                return render(request, 'social_auth/error.html', {
                    'error_message': 'لم يتم توفير بريد إلكتروني من Google'
                })
                
            username = f"google_{user_info['sub']}"
            
            # التأكد من أن اسم المستخدم فريد
            User = get_user_model()
            if User.objects.filter(username=username).exists():
                user = User.objects.get(email=email)
                print(f"User exists with different username: {user.username}")
            else:
                # إنشاء مستخدم جديد
                user = User.objects.create_user(
                    username=username,
                    email=email,
                    first_name=user_info.get('given_name', ''),
                    last_name=user_info.get('family_name', '')
                )
                print(f"New user created: {user.username}")
            
            # إنشاء حساب social
            social_account = SocialAccount.objects.create(
                user=user,
                provider='google',
                provider_id=user_info['sub'],
                email=email,
                name=user_info.get('name', ''),
                picture_url=user_info.get('picture', ''),
                access_token=token_info['access_token']
            )
            print(f"Social account created for: {user.username}")
        
        # تسجيل الدخول
        login(request, user)
        print(f"User {user.username} logged in successfully")
        
        # التوجيه إلى الصفحة الرئيسية
        return redirect('/')
        
    except Exception as e:
        print(f"Exception in google_callback: {str(e)}")
        import traceback
        traceback.print_exc()  # هذا سيطبع تتبع المكدس الكامل للخطأ
        return render(request, 'social_auth/error.html', {
            'error_message': f'خطأ في الخادم: {str(e)}'
        })
    
  
# الدوال القديمة (يمكن حذفها لاحقاً)
@csrf_exempt
@require_http_methods(["POST"])
def facebook_callback_old(request):
    """الإصدار القديم - يمكن حذفه"""
    return JsonResponse({'error': 'This endpoint is deprecated'}, status=410)

@csrf_exempt
@require_http_methods(["POST"])
def google_callback_old(request):
    """الإصدار القديم - يمكن حذفه"""
    return JsonResponse({'error': 'This endpoint is deprecated'}, status=410)