from django import forms
from rental.models.myproperty import Property

class PropertyForm(forms.ModelForm):
    class Meta:
        model = Property
        fields = ['name', 'address', 'price_per_month', 'garbage_cost_per_month', 'electricity_per_unit_price', 'water_per_unit_price']


        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control col-6', 'placeholder': 'Enter Name'}),
            'address': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Adress'}),
            'price_per_month': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter Price Per Month'}),
            'garbage_cost_per_month': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter Garbage Cost Per Month'}),
            'electricity_per_unit_price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter Electricity Per Unit Price'}),
            'water_per_unit_price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter Water Per Unit Price'}),
        }