from django import forms
from accounts.models.users import User
from plan.models import Plan

class SearchCustomerForm(forms.Form):
    user = forms.ModelChoiceField(
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'Search Customer'}),
        queryset=User.objects.all(),
        to_field_name='phone_number',
        required=False
    )




class CreatePlanForm(forms.ModelForm):
    class Meta:
        model = Plan
        fields = [
            'name',
            'price',
            "default_month",
            'description',
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control col-6', 'placeholder': 'Enter Plan Name'}),
            'price': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Price'}),
            'default_month': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Default Month'}),
            'description': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Description'}),
        }
