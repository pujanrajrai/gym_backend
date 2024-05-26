from django import forms
from rental.models.customer import Customer

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['name', 'phone_number', 'secondary_phone_number', 'email', 'address']

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control col-6', 'placeholder': 'Enter Name'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Phone Number'}),
            'secondary_phone_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Phone Number'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter Email'}),
            'address': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your Address'}),
        }