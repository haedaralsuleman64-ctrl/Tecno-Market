from django.db import models
from django.shortcuts import render , get_list_or_404 ,get_object_or_404
from .models import Category , Product
from cart.forms  import CartAddProductForm
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .forms import ProductForm
from .permissions import IsProductOwnerOrReadOnly

# Create your views here.

def product_list(request, category_slug = None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available = True , is_approved = True)
    
    if category_slug:
        category = get_object_or_404(Category , slug = category_slug)
        products = products.filter(category=category)

    featured_categories = Category.objects.filter(display_order__gt = 0).order_by('display_order')[:6]
    
    return render(request, 'products/list.html', {
        'category': category,
        'categories': categories,
        'products': products,
        'featured_categories': featured_categories,
    })

def product_detail(request, id, slug):
    product = get_object_or_404(Product , id = id , slug = slug , available = True)
    cart_product_form = CartAddProductForm()

    related_products = Product.objects.filter(
        category = product.category, 
        available = True,
        is_approved = True
    ).exclude(id = product.id)[:4]

    return render(request, 'products/detail.html', {
        'product': product , 
        'cart_product_form': cart_product_form,
        'related_products': related_products})

def category_list(request):
   
    categories = Category.objects.annotate(
        products_count = models.Count('products')
    ).filter(products_count__gt=0)
    
    return render(request, 'products/category_list.html', {
        'categories': categories
    })


def special_products(request):
    # جلب المنتجات الخاصة (مثلاً: من فئات محددة أو لها خصم)
    special_products = Product.objects.filter(
        category__name__in=['Laptops', 'Complete-PC-Systems','Cameras'], 
        available=True ,
        is_approved=True
    ).distinct()

    
    context = {
        'products': special_products,
        'title': 'منتجات خاصة - عروض مميزة'
    }
    return render(request, 'products/special_products.html', context)


def help_page(request):
    # إضافة أي بيانات اخرى للصفحة (مثلاً: أسئلة شائعة)
    context = {
        'title': 'مركز المساعدة'
    }
    return render(request, 'products/help_page.html', context)


@login_required
def my_products(request):
    """عرض منتجات المستخدم"""
    products = Product.objects.filter(owner=request.user)
    return render(request, 'products/my_products.html', {'products': products})

class ProductCreateView(LoginRequiredMixin, CreateView):
    """إنشاء منتج جديد"""
    model = Product
    form_class = ProductForm
    template_name = 'products/product_form.html'
    
    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('products:my_products')

class ProductUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """تعديل منتج"""
    model = Product
    form_class = ProductForm
    template_name = 'products/product_form.html'
    
    def test_func(self):
        product = self.get_object()
        return product.can_edit(self.request.user)
    
    def get_success_url(self):
        return reverse_lazy('products:my_products')

class ProductDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """حذف منتج"""
    model = Product
    template_name = 'products/product_confirm_delete.html'
    success_url = reverse_lazy('products:my_products')
    
    def test_func(self):
        product = self.get_object()
        return product.can_delete(self.request.user)
    
