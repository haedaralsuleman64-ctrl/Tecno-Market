from django.db import models
from django.conf import settings
from products.models import Product



# Create your models here.

class Order(models.Model):
    STATUS_ORDER = (
        ('On hold' , 'On hold') ,    
        ('Confirmed' , 'Confirmed') ,       
        ('Shipped' , 'Shipped') ,       
        ('Delevered' , 'Delevered') ,   
        ('Cancelled' , 'Cancelled') ,       
    ) 
    user = models.ForeignKey(settings.AUTH_USER_MODEL , on_delete = models.CASCADE , related_name = 'oreder')
    first_name = models.CharField(max_length = 50 , verbose_name = "first name")
    last_name = models.CharField(max_length = 50 , verbose_name = "last name")
    email = models.EmailField(verbose_name = "E-mail")
    address = models.CharField(max_length = 100 , verbose_name = "address")
    postal_code = models.CharField(max_length = 20 , verbose_name = "postal code")
    city = models.CharField(max_length= 50 , verbose_name = "city")
    phone = models.CharField(max_length = 15 , verbose_name = "namber phone")
    created = models.DateTimeField(auto_now_add = True , verbose_name = "created")
    updated = models.DateTimeField(auto_now = True , verbose_name = "updated")
    paid = models.BooleanField(default = False, verbose_name = "payment verification")
    status = models.CharField(max_length = 10 , choices = STATUS_ORDER , default = 'Pending', verbose_name = "status order")
    notes = models.TextField(blank = True , verbose_name = "notes")

    class Meta:
        ordering = ('-created',)
        verbose_name = "order"
        verbose_name_plural = "orders"

    def __str__(self):
        return f"order #{self.id}"
    
    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())
    
#=====================================================

class OrderItem(models.Model):
    order = models.ForeignKey(Order , related_name = 'items' , on_delete = models.CASCADE)
    product = models.ForeignKey(Product , related_name = 'order_item' , on_delete = models.CASCADE)
    price = models.DecimalField(max_digits = 10 , decimal_places = 2 , verbose_name = 'price')
    quantity = models.PositiveIntegerField(default = 1 , verbose_name = 'quantity')

    def __str__(self):
        return str(self.id)
    
    def get_cost(self):
        return self.price * self.quantity
    

        
