from django import forms
from rental.models import Payment


class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ['customer', 'amount']
        widgets = {
            'customer': forms.Select(attrs={'class': 'form-control'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control'}),
        }
