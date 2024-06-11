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



class DateRangeForm(forms.Form):
    TODAY = 'today'
    YESTERDAY = 'yesterday'
    THIS_WEEK = 'this_week'
    THIS_MONTH = 'this_month'
    LAST_MONTH = 'last_month'
    LAST_THREE_MONTHS = 'last_three_months'
    THIS_YEAR = 'this_year'
    CUSTOM = 'custom'

    DATE_CHOICES = (
        (TODAY, 'Today'),
        (YESTERDAY, 'Yesterday'),
        (THIS_WEEK, 'This Week'),
        (THIS_MONTH, 'This Month'),
        (LAST_MONTH, 'Last Month'),
        (LAST_THREE_MONTHS, 'Last Three Months'),
        (THIS_YEAR, 'This Year'),
        (CUSTOM, 'Custom'),
    )
    user_choices = [('All', 'All')] + [(customer.id, customer.phone_number)
                                          for customer in Customer.objects.all()]

    user = forms.ChoiceField(
        choices=user_choices,
        label='Customer',
        required=False,
        widget=forms.Select(attrs={'class': 'ui fluid search dropdown', }),
    )  # Change to ChoiceField
    date_range = forms.ChoiceField(
        choices=DATE_CHOICES,
        label='Date Range',
        initial=TODAY,
        widget=forms.Select(
            attrs={'class': 'ui fluid search dropdown', 'id': 'date_range'}),
        required=False
    )

    from_date = forms.DateField(
        label='From Date',
        required=False,
        widget=forms.DateInput(
            attrs={'type': 'date', 'class': 'form-control', 'id': 'from_date'})
    )
    to_date = forms.DateField(
        label='To Date',
        required=False,
        widget=forms.DateInput(
            attrs={'type': 'date', 'class': 'form-control', 'id': 'to_date'})
    )

    def clean(self):
        cleaned_data = super().clean()
        from_date = cleaned_data.get('from_date')
        to_date = cleaned_data.get('to_date')
        date_range = cleaned_data.get('date_range')

        if date_range == self.CUSTOM:
            if not from_date or not to_date:
                raise forms.ValidationError(
                    "From Date and To Date are required for custom date range.")
            if from_date > to_date:
                raise forms.ValidationError(
                    "From Date cannot be greater than To Date.")

        return cleaned_data
