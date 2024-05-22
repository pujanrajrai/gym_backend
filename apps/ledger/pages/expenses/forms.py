from ledger.models import Ledger
from django import forms
from accounts.models.users import User
from django import forms


class ExpensesForm(forms.Form):
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
    expenses_date = forms.DateField(
        widget=forms.DateInput(
            attrs={'class': 'form-control mt-2 mb-2', 'type': 'date'}),
        required=False
    )

    entry_type = forms.ChoiceField(
        choices=[('Expenses', 'Expenses')],
        widget=forms.Select(attrs={'class': 'form-control mt-2 mb-2'}),
        initial='Invoice'  # Set default value if needed
    )


class ExpensesFilterForm(forms.Form):
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