from django.shortcuts import render ,redirect
from django.contrib.auth import authenticate, login , logout
from django.contrib import messages
from .forms import CustomUserCreationForm
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from social_auth.models import SocialAccount
from orders.models import Order  
from products.models import Product 
from .models import CustomUser

#Create your views here.

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect(reverse('products:product_list'))  # غير 'home' لصفحة الوجهة المطلوبة
        else:
            messages.error(request, 'اسم المستخدم أو كلمة المرور غير صحيحة')
            return redirect('accounts:login/')
    
    return render(request, 'accounts/login.html')

def logout_view(request):
    logout(request)
    return redirect(reverse('products:product_list'))   # أو أي صفحة تريد التوجيه لها بعد تسجيل الخروج

def signup_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'تم إنشاء حسابك بنجاح!')
            return redirect(reverse('products:product_list'))  # غير 'home' لصفحة الوجهة المطلوبة
        else:
            # عرض الأخطاء إذا كان النموذج غير صالح
            for error in form.errors:
                messages.error(request, form.errors[error])
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'accounts/signup.html', {'form': form}) 

@login_required
def profile_view(request):
    """عرض صفحة الملف الشخصي للمستخدم"""
    user = request.user
    social_accounts = SocialAccount.objects.filter(user=user)
    orders_count = Order.objects.filter(user=user).count()
    products_count = Product.objects.filter(owner=user).count()
    reviews_count = 0 

    context = {
        'user': user,
        'social_accounts': social_accounts,
        'orders_count': orders_count,
        'products_count': products_count,
        'reviews_count': reviews_count,
    }
    return render(request, 'accounts/profile.html', context)


@login_required
def update_profile(request):
    """تحديث معلومات الملف الشخصي"""
    if request.method == 'POST':
        user = request.user
        
        # تحديث المعلومات الأساسية
        user.first_name = request.POST.get('first_name', '')
        user.last_name = request.POST.get('last_name', '')
        user.email = request.POST.get('email', '')
        user.username = request.POST.get('username', '')
        
        # التحقق من كلمة المرور الحالية إذا تم تقديم كلمة مرور جديدة
        new_password = request.POST.get('new_password', '')
        if new_password:
            current_password = request.POST.get('current_password', '')
            if not user.check_password(current_password):
                messages.error(request, 'Current password is incorrect.')
                return redirect('accounts:profile')
            
            user.set_password(new_password)
        
        user.save()
        messages.success(request, 'Profile updated successfully!')
        
        # إعادة تسجيل الدخول إذا تم تغيير كلمة المرور
        if new_password:
            from django.contrib.auth import login
            login(request, user)
        
        return redirect('accounts:profile')
    
    return redirect('accounts:profile')

