from ledger.models import Ledger
from django import forms
from accounts.models.users import User
from django import forms


class LedgerForm(forms.Form):
    userss = User.objects.filter(role="staff")

    user_choices = [(user.phone_number, user.phone_number) for user in userss]

    user = forms.ChoiceField(
        choices=[('', 'Select user')] + user_choices,
        widget=forms.Select(
            attrs={'class': 'form-control mt-2 mb-2', 'data-live-search': 'true'})
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
        choices=[('Salary', 'Salary')],
        widget=forms.Select(attrs={'class': 'form-control mt-2 mb-2'}),
        initial='Invoice'  # Set default value if needed
    )


class LedgerFilterForm(forms.Form):
    # user = forms.ModelChoiceField(
    #     queryset=user.objects.all(),  # Replace with your actual queryset
    #     widget=forms.Select(attrs={'class': 'form-control mt-2 mb-2'}),
    #     empty_label='Select user',
    #     required=False

    # )
    userss = User.objects.filter(role="staff")

    user_choices = [(user.phone_number, user.phone_number) for user in userss]

    user = forms.ChoiceField(
        choices=[('', 'Select user')] + user_choices,
        widget=forms.Select(
            attrs={'class': 'form-control mt-2 mb-2', 'data-live-search': 'true'}),
        required=False
    )

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
    # from_date = forms.DateField(required=False,
    #                             widget=forms.DateInput(
    #                                 attrs={'type': 'date'}))
    # to_date = forms.DateField(required=False, widget=forms.DateInput(
    #     attrs={'type': 'date'}))
