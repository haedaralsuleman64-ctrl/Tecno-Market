from django.db import models
from django.conf import settings
from products.models import Product

# Create your models here.

class Cart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL , on_delete = models.CASCADE , null = True , blank = True)
    session_key = models.CharField(max_length = 40 , null = False , blank = True)
    created_date = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        if self.user:
            return f"cart of : {self.user.username}"
        return f"cart (..): {self.session_key}"
    
    @property
    def total_price(self):
        return sum(item.total_price for item in self.items.all())

    @property
    def total_items(self):
        return sum(item.quantity for item in self.items.all())
    
    @property
    def is_empty(self):
        return f"items = {self.total_items == 0} , price = {self.total_price == 0}"
#========================================================

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='items', on_delete = models.CASCADE)
    product = models.ForeignKey(Product, on_delete = models.CASCADE)
    quantity = models.PositiveIntegerField(default = 0)

    def __str__(self):
        return f"{self.quantity} X {self.product.name}"

    @property
    def total_price(self):
        return self.quantity * self.product.price