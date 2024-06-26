from django import forms
from rental.models import CustomerProperty, UnconfirmInvoice


class CustomForm(forms.Form):
    INCLUDE_EXCLUDE_CHOICES = [
        ('include', 'Include'),
        ('exclude', 'Exclude'),
    ]

    SELECTION_TYPE_CHOICES = [
        ('all', 'All'),
        ('single', 'Single'),
        ('multiple', 'Multiple'),
    ]

    type1 = forms.ChoiceField(
        choices=INCLUDE_EXCLUDE_CHOICES,
        label="Include or Exclude",
        widget=forms.Select(attrs={'class': 'ui fluid search dropdown'}),
    )

    type2 = forms.ChoiceField(
        choices=SELECTION_TYPE_CHOICES,
        label="Selection Type",
        widget=forms.Select(
            attrs={'class': 'ui fluid search dropdown', 'id': 'id_type2'}),
    )
    month = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control", })
    )

    # Get choices from CustomerProperty model
    customer_properties = CustomerProperty.objects.filter(is_terminated=False)
    properties_choices = [(cp.myproperty.id, cp.myproperty.name)
                          for cp in customer_properties]
    print(properties_choices)
    type3 = forms.MultipleChoiceField(
        choices=properties_choices,
        widget=forms.SelectMultiple(
            attrs={'class': 'ui fluid search dropdown', 'id': 'id_type3', 'type': 'hidden', 'style': 'display:hidden;'}),
        label="Select Multiple Properties",
        required=False
    )
    type4 = forms.ChoiceField(
        choices=properties_choices,
        label="Select a Single Property",
        widget=forms.Select(attrs={
                            'class': 'ui fluid search dropdown', 'id': 'id_type4', 'style': 'display:hidden;'}),
        required=False
    )


class IssueInvoiceForm(forms.ModelForm):
    class Meta:
        model = UnconfirmInvoice
        fields = [
            'customer',
            'myproperty',
            'month_name',
            'property_rent',
            'last_electricity_unit_reading',
            'current_electricity_unit_reading',
            'total_electricity_unit',
            'total_electricity_amount',
            'total_water_unit',
            'total_water_amount',
            'total_garbage_amount',
            'miscellaneous_amount',
            'total_price',
            'remarks'
        ]
        widgets = {
            'month_name': forms.TextInput(attrs={"class": "form-control"}),
            'property_rent': forms.NumberInput(attrs={"class": "form-control"}),
            'total_electricity_unit': forms.NumberInput(attrs={"class": "form-control", 'readonly': 'readonly'}),
            'last_electricity_unit_reading': forms.NumberInput(attrs={"class": "form-control"}),
            'current_electricity_unit_reading': forms.NumberInput(attrs={"class": "form-control"}),
            'total_water_unit': forms.NumberInput(attrs={"class": "form-control"}),
            'miscellaneous_amount': forms.NumberInput(attrs={"class": "form-control"}),
            'total_garbage_amount': forms.NumberInput(attrs={"class": "form-control"}),
            'remarks': forms.Textarea(attrs={"class": "form-control", "rows": "2"}),
            'customer': forms.Select(attrs={"class": "form-control"}),
            'myproperty': forms.Select(attrs={"class": "form-control"}),
            'total_electricity_amount': forms.NumberInput(attrs={"class": "form-control", 'readonly': 'readonly'}),
            'total_water_amount': forms.NumberInput(attrs={"class": "form-control", 'readonly': 'readonly'}),
            'total_price': forms.NumberInput(attrs={"class": "form-control", 'readonly': 'readonly'}),
        }
