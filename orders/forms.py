from django import forms
from .models import Order

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = [
            'first_name', 
            'last_name', 
            'email', 
            'address', 
            'postal_code', 
            'city', 
            'phone',
            'notes'
        ]
        widgets = {
            'notes': forms.Textarea(attrs={'rows': 4}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # جعل الحقول مطلوبة
        for field in self.fields:
            self.fields[field].required = True
            self.fields[field].widget.attrs['class'] = 'form-control'