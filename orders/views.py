from django.shortcuts import render , get_object_or_404 , redirect
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from .models import Order , OrderItem 
from .forms import OrderForm
from django.http import HttpResponseForbidden
from django.contrib import messages
from cart.models import Cart ,CartItem

# Create your views here.

@login_required
def order_create(request):
    """إنشاء طلب جديد من محتويات العربة"""
    try:
        # استخدام get_cart بدلاً من الاستعلام المباشر للتعامل مع الحالات المختلفة
        cart = get_cart(request)
    except Cart.DoesNotExist:
        messages.error(request, 'عربة التسوق فارغة')
        return redirect('cart:cart_detail')
    
    if not cart.items.exists():
        messages.error(request, 'عربة التسوق فارغة')
        return redirect('cart:cart_detail')
    
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.total = cart.total_price
            order.save()
            
            # حفظ عناصر الطلب
            for item in cart.items.all():
                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    price=item.product.price,
                    quantity=item.quantity
                )
            
            # تفريغ العربة بعد إنشاء الطلب
            cart.items.all().delete()
            messages.success(request, 'تم إنشاء الطلب بنجاح! رقم الطلب: #{}'.format(order.id))
            return redirect('orders:order_detail', order_id=order.id)
        else:
            messages.error(request, 'يرجى تصحيح الأخطاء في النموذج')
    else:
        # تعبئة النموذج ببيانات المستخدم
        initial_data = {}
        if request.user.is_authenticated:
            user = request.user
            initial_data = {
                'first_name': user.first_name or '',
                'last_name': user.last_name or '',
                'email': user.email,
            }
        form = OrderForm(initial=initial_data)
    
    return render(request, 'orders/order_create.html', {
        'form': form,
        'cart': cart
    })

@login_required
def order_list(request):
    """قائمة الطلبات مع ترتيب زمني"""
    if request.user.is_staff:
        orders = Order.objects.all().order_by('-created')
    else:
        orders = Order.objects.filter(user=request.user).order_by('-created')
    
    return render(request, 'orders/order_list.html', {
        'orders': orders,
        'title': 'طلباتي' if not request.user.is_staff else 'جميع الطلبات'
    })

@login_required
def order_detail(request, order_id):
    """تفاصيل الطلب مع تحسين التحقق من الصلاحية"""
    order = get_object_or_404(Order, id=order_id)
   
    status_order_1 = ('confirmed', 'shipped', 'delivered')
    status_order_2 = ('shipped', 'delivered')

    # التحقق من الصلاحية باستخدام permission class
    if not (request.user.is_staff or order.user == request.user):
        return HttpResponseForbidden("ليس لديك صلاحية لعرض هذا الطلب")
    
    return render(request, 'orders/order_detail.html', {
        'order': order,
        'can_edit_status': request.user.is_staff,
        'status_options': status_order_1 or status_order_2 ,
    })

@staff_member_required
def order_update_status(request, order_id):
    """تحديث حالة الطلب (للموظفين فقط)"""
    order = get_object_or_404(Order, id=order_id)
    
    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status in dict(Order.STATUS_CHOICES).keys():
            order.status = new_status
            order.save()
            messages.success(request, 'تم تحديث حالة الطلب بنجاح')
            return redirect('orders:order_detail', order_id=order.id)
        else:
            messages.error(request, 'حالة الطلب غير صالحة')
    
    return render(request, 'orders/order_status_form.html', {
        'order': order,
        'status_choices': Order.STATUS_CHOICES
    })

# دالة مساعدة للحصول على العربة
def get_cart(request):
    """الحصول على عربة المستخدم أو إنشاء جديدة"""
    cart_id = request.session.get('cart_id')
    if cart_id:
        try:
            return Cart.objects.get(id=cart_id)
        except Cart.DoesNotExist:
            pass
    
    # إنشاء عربة جديدة
    cart = Cart.objects.create(session_key=request.session.session_key)
    if request.user.is_authenticated:
        cart.user = request.user
        cart.save()
    request.session['cart_id'] = cart.id
    return cart

