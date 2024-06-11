from django import forms
from rental.models import Customer, Property, CustomerProperty


class CustomerPropertyForms(forms.ModelForm):
    electricity_unit_reading = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'required': 'required',
        })
    )

    class Meta:
        model = CustomerProperty
        fields = ['customer', 'myproperty', 'electricity_unit_reading']
        widgets = {
            'customer': forms.Select(attrs={'class': 'ui fluid search dropdown clearable'}),
            'myproperty': forms.Select(attrs={'class': 'ui fluid search dropdown clearable'}),
            'electricity_unit_reading': forms.TextInput(attrs={'class': 'form-control'}),

        }


class CustomerPropertyUpdateForms(forms.ModelForm):
    electricity_unit_reading = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'required': 'required',
        })
    )

    class Meta:
        model = CustomerProperty
        fields = ['customer', 'myproperty',
                  'electricity_unit_reading', 'is_terminated']
        widgets = {
            'customer': forms.Select(attrs={'class': 'ui fluid search dropdown clearable'}),
            'myproperty': forms.Select(attrs={'class': 'ui fluid search dropdown clearable'}),
            'electricity_unit_reading': forms.TextInput(attrs={'class': 'form-control'}),

        }
