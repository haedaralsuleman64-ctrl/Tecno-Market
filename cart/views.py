from django.shortcuts import render , redirect , get_object_or_404
from django.views.decorators.http import require_POST
from django.conf import settings
from .models import Cart , CartItem
from products.models import Product
from .forms import CartAddProductForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
# Create your views here.

def get_cart(request):
    # تأكد من وجود session key
    if not request.session.session_key:
        request.session.create()

    cart_id = request.session.get('cart_id')
    if cart_id:
        try:
            cart = Cart.objects.get(id = cart_id)
        except Cart.DoesNotExist:
            cart = Cart.objects.create(session_key=request.session.session_key)
            if request.user.is_authenticated:
                cart.user = request.user
                cart.save()
            request.session['cart_id'] = cart.id
    else:
        cart = Cart.objects.create(session_key=request.session.session_key)
        if request.user.is_authenticated:
            cart.user = request.user
            cart.save()
        request.session['cart_id'] = cart.id
    return cart

def cart_detail(request):
    cart = get_cart(request)
    return render(request, 'cart/detail.html', {'cart': cart})

@login_required
@require_POST
def cart_add(request, product_id):
    cart = get_cart(request)
    product = get_object_or_404(Product, id = product_id)
    form = CartAddProductForm(request.POST)
    messages.success(request, 'تمت إضافة المنتج إلى العربة')

    if form.is_valid():
        cd = form.cleaned_data
        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            product=product,
            defaults={'quantity': cd['quantity']}
        )
        if not created:
            cart_item.quantity += cd['quantity']
            cart_item.save()
    
        return redirect('cart:cart_detail')
    else:
        # إعادة إلى صفحة المنتج مع رسالة خطأ
        return redirect(product.get_absolute_url())
    
def cart_remove(request, product_id):
    cart = get_cart(request)
    product = get_object_or_404(Product, id = product_id)
    try:
        cart_item = CartItem.objects.get(cart = cart, product = product)
        cart_item.delete()
        messages.success(request, 'تم حذف المنتج من العربة')
    except CartItem.DoesNotExist:
        """
        error 
        """
        pass
    return redirect('cart:cart_detail')