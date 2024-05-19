from ledger.models import Ledger
from django import forms
from accounts.models.users import User
from django import forms


class SalaryForm(forms.Form):
    user = forms.ModelChoiceField(queryset=User.objects.filter(role="staff"
                                                               ), label="User", required=False, widget=forms.Select(attrs={'class': 'ui fluid search dropdown clearable'}))

    amount = forms.DecimalField(
        widget=forms.NumberInput(attrs={'class': 'form-control mt-2 mb-2'}),
        max_digits=10,
        decimal_places=2,
        min_value=0  # Set minimum value if needed
    )

    remarks = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control mt-2 mb-2'}),
        required=False  # Set to True if remarks are required
    )

    entry_type = forms.ChoiceField(
        choices=[('Salary', 'Salary')],
        widget=forms.Select(attrs={'class': 'form-control mt-2 mb-2'}),
        initial='Invoice'  # Set default value if needed
    )


class SalaryFilterForm(forms.Form):
    user = forms.ModelChoiceField(queryset=User.objects.filter(role="staff"
                                                               ), label="User", required=False, widget=forms.Select(attrs={'class': 'ui fluid search dropdown clearable'}))

    from_date = forms.DateField(
        widget=forms.DateInput(
            attrs={'class': 'form-control mt-2 mb-2', 'type': 'date'}),
        required=False
    )
    to_date = forms.DateField(
        widget=forms.DateInput(
            attrs={'class': 'form-control mt-2 mb-2', 'type': 'date'}),
        required=False
    )
