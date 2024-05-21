from django import forms
from accounts.models.users import User
from accounts.models.profiles import StaffProfile, UserProfile

role_choices = [
    ('admin', 'admin'),
    ('staff', 'staff'),
    ('user', 'user')
]


class CreateAdminForm(forms.ModelForm):
    password2 = forms.CharField(
        label="Password confirmation",
        widget=forms.PasswordInput(
            attrs={'class': 'form-control', 'placeholder': 'Confirm Password'}),
        required=True
    )
    
    class Meta:
        model = User
        fields = [
            'email',
            'phone_number',
            'password',
            'password2',
        ]

        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter Email'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Phone Number'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter password'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password2 = cleaned_data.get('password2')

        if password and password2 and password != password2:
            self.add_error('password2', 'Passwords do not match.')
        cleaned_data["password"] = password
        cleaned_data["role"] = "admin"
        return cleaned_data


    def save(self, commit=True):
        # Call the parent class's save method to save the form data
        instance = super().save(commit=False)
        
        # Set the role to 'admin' for the user instance
        instance.role = 'admin'
        
        if commit:
            instance.save()
        return instance

class CreateStaffForm(forms.ModelForm):

    phone_number = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={'class': 'form-control col-6'}),
    )
    email = forms.CharField(
        required=False,
        max_length=150,
        widget=forms.EmailInput(attrs={'class': 'form-control col-6'}),
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = StaffProfile
        fields = [
            'phone_number',
            'email',
            "password",
            'fullname',
            'address',
            'gender',
            'photo',
            'id_document',
        ]
        widgets = {
            'fullname': forms.TextInput(attrs={'class': 'form-control col-6', 'placeholder': 'Enter your Full Name'}),
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
            role='staff',
        )

        staff_profile = super().save(commit=False)
        staff_profile.user = user
        # add this line to save the area field

        if commit:
            staff_profile.save()

        return staff_profile

    def clean_phone_number(self):
        phone_number = self.cleaned_data['phone_number']
        if User.objects.filter(phone_number=phone_number).exists():
            raise forms.ValidationError("phone_number already exists.")
        return phone_number


class CreateUserForm(forms.ModelForm):

    phone_number = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={
                               'class': 'form-control', 'placeholder': 'Enter your Phone Number', "pattern": "\d*"}),
    )
    email = forms.CharField(
        required=False,
        max_length=150,
        widget=forms.EmailInput(attrs={'class': 'form-control col-6'}),
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = UserProfile
        fields = [
            'phone_number',
            'email',
            "password",
            'fullname',
            'address',
            'gender',
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


class StaffProfileUpdateForm(forms.ModelForm):

    phone_number = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={'class': 'form-control col-6'}),
    )
    email = forms.CharField(
        max_length=150,
        widget=forms.EmailInput(attrs={'class': 'form-control col-6'}),
    )

    class Meta:
        model = StaffProfile
        fields = [
            'phone_number',
            "email",
            'fullname',
            'address',
            'gender',
            'photo',
            'id_document',
        ]
        widgets = {
            'fullname': forms.TextInput(attrs={'class': 'form-control col-6', 'placeholder': 'Enter your Full Name'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your Phone Number'}),
            'address': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your Address'}),
            'gender': forms.Select(attrs={'class': 'form-control mt-2 mb-2', 'placeholder': 'Gender'}),

        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Get the instance associated with the form
        instance = kwargs.get('instance')
        # If instance exists and it has a related user
        if instance and instance.user:
            # Populate email and phone_number fields with user data
            self.fields['email'].initial = instance.user.email
            self.fields['phone_number'].initial = instance.user.phone_number

    def save(self, commit=True):
        instance = super().save(commit=False)

        if commit:
            instance.save()
        return instance


class AdminProfileUpdateForm(forms.ModelForm):

    phone_number = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={'class': 'form-control col-6'}),
    )
    email = forms.CharField(
        max_length=150,
        widget=forms.EmailInput(attrs={'class': 'form-control col-6'}),
    )

    class Meta:
        model = User
        fields = [
            'phone_number',
            "email",

        ]
        widgets = {
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your Phone Number'}),


        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Get the instance associated with the form
        instance = kwargs.get('instance')
        # If instance exists and it has a related user
        if instance:
            # Populate email and phone_number fields with user data
            self.fields['email'].initial = instance.email
            self.fields['phone_number'].initial = instance.phone_number

    def save(self, commit=True):
        instance = super().save(commit=False)

        if commit:
            instance.save()
        return instance


class UserProfileUpdateForm(forms.ModelForm):

    phone_number = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={'class': 'form-control col-6'}),
    )
    email = forms.CharField(
        max_length=150,
        widget=forms.EmailInput(attrs={'class': 'form-control col-6'}),
    )

    class Meta:
        model = UserProfile
        fields = [
            'phone_number',
            "email",
            'fullname',
            'address',
            'gender',
            'photo',

        ]
        widgets = {
            'fullname': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your Full Name'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your Phone Number'}),
            'address': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your Address'}),
            'gender': forms.Select(attrs={'class': 'form-control mt-2 mb-2', 'placeholder': 'Gender'}),

        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Get the instance associated with the form
        instance = kwargs.get('instance')
        # If instance exists and it has a related user
        if instance and instance.user:
            # Populate email and phone_number fields with user data
            self.fields['email'].initial = instance.user.email
            self.fields['phone_number'].initial = instance.user.phone_number

    def save(self, commit=True):
        instance = super().save(commit=False)

        if commit:
            instance.save()
        return instance




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
    user_choices = [('All', 'All')] + [(user.id, user.phone_number)
                                          for user in User.objects.all()]

    user = forms.ChoiceField(
        choices=user_choices,
        label='User',
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
