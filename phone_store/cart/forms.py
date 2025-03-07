from django import forms

from .models import Payment

INPUT_CLASSES = 'w-full py-4 px-6 rounded-xl border'

class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields=('first_name', 'last_name', 'address', 'card_number', 'expiration_date', 'cvv')

        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': INPUT_CLASSES
            }),
            'last_name': forms.TextInput(attrs={
                'class': INPUT_CLASSES
            }),
            'address': forms.TextInput(attrs={
                'class': INPUT_CLASSES
            }),
            'card_number': forms.TextInput(attrs={
                'class': INPUT_CLASSES
            }),
            'expiration_date': forms.DateInput(attrs={
                'class': INPUT_CLASSES
            }),
            'cvv': forms.NumberInput(attrs={
                'class': INPUT_CLASSES
            }),
        }