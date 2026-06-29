from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.conf import settings

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length = 50  , db_index = True , verbose_name = 'title category')
    slug = models.SlugField(max_length = 200 , unique = True , verbose_name = 'link')
    name_ar = models.CharField(max_length = 200, verbose_name = "name in arabic", blank=True)
    name_en = models.CharField(max_length = 200, verbose_name = "name in english", blank=True)
    image = models.ImageField(upload_to ='categories/%Y/%m/%d', blank = True, null = True, verbose_name = "category photo")
    description = models.TextField(blank = True, verbose_name = "description")
    display_order = models.PositiveIntegerField(default = 0, verbose_name = "display order")

    class Meta:
        ordering = ('name',)
        verbose_name = 'category'
        verbose_name_plural = 'categorys'
        
    def __str__(self):
        return self.name_ar if self.name_ar else self.name    
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        if not self.name_ar:
            self.name_ar = self.name
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("products:product_list_by_category", args = {self.slug})
    
    def get_products_count(self):
        """الحصول على عدد المنتجات في هذه الفئة"""
        return self.products.count()

#====================================================        

class Product(models.Model):
    category = models.ForeignKey(Category , related_name= 'products' , on_delete = models.CASCADE , verbose_name = 'category')
    owner = models.ForeignKey(settings.AUTH_USER_MODEL , related_name = 'products', on_delete = models.CASCADE , null = True , blank = True , verbose_name = "owner")
    name = models.CharField(max_length = 30 , db_index = True , verbose_name = 'title product')
    slug = models.SlugField(max_length=200, db_index = True, verbose_name = 'link')
    description = models.TextField(blank = True , verbose_name = 'description')
    price = models.DecimalField(max_digits = 10 , decimal_places = 2 , verbose_name = 'price')
    available = models.BooleanField(default = True , verbose_name = 'available')
    created = models.DateTimeField(auto_now_add = True , verbose_name = 'created in ')
    updated = models.DateTimeField(auto_now = True , verbose_name = 'updated at')
    stock = models.PositiveIntegerField(default = 0 , verbose_name = 'quantity')
    image = models.ImageField(upload_to = 'photos/%y/%m/%d' , null = False , verbose_name = 'photo')
    is_approved = models.BooleanField(default = False, verbose_name = "تم الموافقة")
    image_url = models.URLField(blank=True, null=True, verbose_name="رابط الصورة الخارجي")
    
    class Meta:
        ordering = ('name',)
        indexes = [models.Index(fields=['id', 'slug'])]
        verbose_name = 'product'
        verbose_name_plural = 'products' 

    def __str__(self):
        return self.name 

    def get_absolute_url(self):
        return reverse('products:product_detail', args=[self.id , self.slug])
    
    def in_stock(self):
        return self.stock > 0
    
    def can_edit(self, user):
        """التحقق من إمكانية تعديل المنتج"""
        if user.is_staff:
            return True
        return self.owner == user
    
    def can_delete(self, user):
        """التحقق من إمكانية حذف المنتج"""
        return user.is_staff or (self.owner == user and not self.has_orders())
    
    def has_orders(self):
        """التحقق إذا كان المنتج موجود في أي طلبات"""
        return self.order_items.exists()   


