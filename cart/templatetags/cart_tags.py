from django import template
from cart.forms import CartAddProductForm

register = template.Library()

@register.inclusion_tag('cart/add_form.html')
def cart_add_form(product_id = None):
    """
    يعرض نموذج اضافة المنتج الي السلة 
    """
    return {
        'form': CartAddProductForm(),
        'product_id': product_id
    }

@register.simple_tag
def get_cart_form():
    """
   render إرجاع نموذج السلة فقط بدون 
    """
    return CartAddProductForm()