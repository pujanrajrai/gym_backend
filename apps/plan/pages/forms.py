from django import forms
from accounts.models.users import User

class SearchCustomerForm(forms.Form):
    user = forms.ModelChoiceField(
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'Search Customer'}),
        queryset=User.objects.all(),
        to_field_name='phone_number',
        required=False
    )

    # def __init__(self, *args, **kwargs):
    #     super(SearchCustomerForm, self).__init__(*args, **kwargs)
    #     self.fields['user'].label_from_instance = self.label_from_instance

    # def label_from_instance(self, obj):
    #     return f"{obj.name} - {obj.phone_number}"
