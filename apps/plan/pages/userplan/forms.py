from django import forms
from accounts.models.users import User
from accounts.models.profiles import StaffProfile, UserProfile
from plan.models import Plan, UnConfirmUserPlanDetail


class SearchCustomerForm(forms.Form):
    customer = forms.ModelChoiceField(
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'Search Customer'}),
        queryset=User.objects.filter(role='user'),
        to_field_name='phone_no_1',
        required=False
    )

    def __init__(self, *args, **kwargs):
        super(SearchCustomerForm, self).__init__(*args, **kwargs)
        self.fields['customer'].label_from_instance = self.label_from_instance

    def label_from_instance(self, obj):
        return f"{obj.name} - {obj.phone_no_1}"


class CreateUserForm(forms.ModelForm):

    phone_number = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={'class': 'form-control col-6'}),
    )
    email = forms.CharField(
        max_length=150,
        widget=forms.EmailInput(attrs={'class': 'form-control col-6'}),
        required=False
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = UserProfile
        fields = [
            'phone_number',
            "password",
            'fullname',
            'address',
            'gender',
            'email',
            'photo',
        ]
        widgets = {
            'fullname': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your Full Name'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your Phone Number', "pattern": "\d*"}),
            'address': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your Address'}),
            'gender': forms.Select(attrs={'class': 'form-control mt-2 mb-2', 'placeholder': 'Gender'}),

        }

    def clean(self):
        cleaned_data = super().clean()
        phone_number = cleaned_data.get('phone_number')
        password = cleaned_data.get('password')
        return cleaned_data

    def save(self, commit=True):
        # Create a new User object with the form data
        user = User.objects.create_user(
            phone_number=self.cleaned_data['phone_number'],
            email=self.cleaned_data['email'],
            password=self.cleaned_data['password'],
            role='user',
        )

        user_profile = super().save(commit=False)
        user_profile.user = user
        # add this line to save the area field

        if commit:
            user_profile.save()

        return user_profile

    def clean_phone_number(self):
        phone_number = self.cleaned_data['phone_number']
        if User.objects.filter(phone_number=phone_number).exists():
            raise forms.ValidationError("phone_number already exists.")
        return phone_number


class UserPlanForm(forms.Form):
    def __init__(self, *args, userprofile=None, **kwargs):
        super().__init__(*args, **kwargs)
        if userprofile:
            self.fields['plan'].queryset = Plan.objects.exclude(
                id__in=UnConfirmUserPlanDetail.objects.filter(userplan__userprofile=userprofile).values_list(
                    'plan_id', flat=True)
            )
        self.userprofile = userprofile  # Store userprofile for later use

    plan = forms.ModelChoiceField(
        queryset=Plan.objects.all(),
        label="Plan",
        widget=forms.Select(attrs={'class': 'ui fluid search dropdown'})
    )
    starting_date = forms.DateField(
        label="Starting Date",
        widget=forms.DateInput(
            attrs={"class": "form-control", "type": "date"}),
        required=False
    )
