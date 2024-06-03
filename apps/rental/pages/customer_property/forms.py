from django import forms
from rental.models import Customer, Property, CustomerProperty


class CustomerPropertyForms(forms.ModelForm):
    class Meta:
        model = CustomerProperty
        fields = ['customer', 'myproperty']
        widgets = {
            'customer': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Select Customer'}),
            'myproperty': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Select Property'}),
        }


class CustomerPropertyUpdateForms(forms.ModelForm):
    class Meta:
        model = CustomerProperty
        fields = ['customer', 'myproperty', 'is_terminated']
        widgets = {
            'customer': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Select Customer'}),
            'myproperty': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Select Property'}),
        }
