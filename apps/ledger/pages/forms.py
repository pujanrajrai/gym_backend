from ledger.models import Ledger
from django import forms
from accounts.models.users import User
from django import forms


class LedgerForm(forms.Form):
    user = forms.ModelChoiceField(queryset=User.objects.all(
    ), label="User", required=False, widget=forms.Select(attrs={'class': 'ui fluid search dropdown clearable'}))

    _type = forms.ChoiceField(
        choices=[('Debit', 'Debit'), ('Credit', 'Credit')],
        widget=forms.Select(attrs={'class': 'form-control mt-2 mb-2'}),
        initial='Debit'  # Set default value if needed
    )

    particular = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control mt-2 mb-2'}),
        max_length=255,
    )

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
        choices=[('Ledger Entry', 'Ledger Entry')],
        widget=forms.Select(attrs={'class': 'form-control mt-2 mb-2'}),
        initial='Invoice'  # Set default value if needed
    )


class LedgerFilterForm(forms.Form):
    user = forms.ModelChoiceField(queryset=User.objects.all(
    ), label="User", required=False, widget=forms.Select(attrs={'class': 'ui fluid search dropdown clearable'}))
    from_date = forms.DateField(label="From Date", required=False, widget=forms.DateInput(
        attrs={'class': 'form-control', 'type': 'date'}))
    to_date = forms.DateField(label="To Date", required=False, widget=forms.DateInput(
        attrs={'class': 'form-control', 'type': 'date'}))
