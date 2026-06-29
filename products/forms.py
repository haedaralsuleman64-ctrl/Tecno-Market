from django import forms
from .models import Product, Category

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'category', 'description', 'price', 'image', 'stock', 'available']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # جعل الحقول أصدقاء للغة العربية
        self.fields['name'].label = 'اسم المنتج'
        self.fields['category'].label = 'الفئة'
        self.fields['description'].label = 'الوصف'
        self.fields['price'].label = 'السعر'
        self.fields['image'].label = 'صورة المنتج'
        self.fields['stock'].label = 'الكمية المتاحة'
        self.fields['available'].label = 'متوفر'