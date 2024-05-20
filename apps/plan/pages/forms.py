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

# class LedgerFilterForm(forms.Form):
#     user = forms.ModelChoiceField(queryset=User.objects.all(
#     ), label="User", required=False, widget=forms.Select(attrs={'class': 'ui fluid search dropdown clearable'}))
#     from_date = forms.DateField(label="From Date", required=False, widget=forms.DateInput(
#         attrs={'class': 'form-control', 'type': 'date'}))
#     to_date = forms.DateField(label="To Date", required=False, widget=forms.DateInput(
#         attrs={'class': 'form-control', 'type': 'date'}))


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
