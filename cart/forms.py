from django import forms
from django.contrib import messages

PRODUCT_QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 21)]

class CartAddProductForm(forms.Form):
    quantity = forms.TypedChoiceField(
        choices = PRODUCT_QUANTITY_CHOICES,
        coerce = int,
        label = "quantity"
    )
    override = forms.BooleanField(
        required = False,
        initial = False,
        widget = forms.HiddenInput
    )

    def clean_quantity(self):
        quantity = self.cleaned_data['quantity']
        if quantity <= 0:
            messages.success( 'الكمية يجب أن تكون أكبر من الصفر')
        return quantity