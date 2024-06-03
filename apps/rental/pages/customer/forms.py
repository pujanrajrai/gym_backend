from django import forms
from rental.models.customer import Customer, CustomerDocument


class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['name', 'phone_number',
                  'secondary_phone_number', 'email', 'address']

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control col-6', 'placeholder': 'Enter Name'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Phone Number'}),
            'secondary_phone_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Phone Number'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter Email'}),
            'address': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your Address'}),
        }


class CustomerDocumentForm(forms.ModelForm):
    class Meta:
        model = CustomerDocument
        fields = ['customer', 'name', 'file']
        widgets = {
            'customer': forms.Select(attrs={'class': 'form-control col-6'}),
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter File Name'}),
        }

    def __init__(self, customer, *args, **kwargs):

        super().__init__(*args, **kwargs)
        if customer:
            self.fields['customer'].queryset = Customer.objects.filter(
                id=customer)
            self.fields['customer'].initial = customer
            # Makes the field read-only
            self.fields['customer'].widget.attrs['readonly'] = True
