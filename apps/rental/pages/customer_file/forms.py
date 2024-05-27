from django import forms
from rental.models.customer import CustomerDocument

class CustomerDocumentForm(forms.ModelForm):
    class Meta:
        model = CustomerDocument
        fields = ['name', 'file']
