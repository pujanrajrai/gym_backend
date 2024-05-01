from django import forms
from accounts.models.users import User
from accounts.models.profiles import StaffProfile,UserProfile

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
    role = forms.ChoiceField(
        choices=role_choices,  # Correctly reference role_choices from your model
        required=True,
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = User
        fields = [
            'email',
            'phone_number',
            'password',
            'password2',
            'role'
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

        return cleaned_data



class CreateStaffForm(forms.ModelForm):
    
    phone_number = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={'class': 'form-control col-6'}),
    )
    email = forms.CharField(
        max_length=150,
        widget=forms.EmailInput(attrs={'class': 'form-control col-6'}),
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    

    class Meta:
        model = StaffProfile
        fields = [
            'phone_number',
            "password",
            'fullname',
            'address',
            'gender',
            'photo',
            'id_document',
        ]
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your Full Name'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your Phone Number'}),
            'address': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your Address'}),
            
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
        return 
        


class CreateUserForm(forms.ModelForm):
    
    phone_number = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={'class': 'form-control col-6'}),
    )
    email = forms.CharField(
        max_length=150,
        widget=forms.EmailInput(attrs={'class': 'form-control col-6'}),
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
            'photo',
        ]
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your Full Name'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your Phone Number'}),
            'address': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your Address'}),
            
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
            'full_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your Full Name'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your Phone Number'}),
            'address': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your Address'}),
            
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
            'full_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your Full Name'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your Phone Number'}),
            'address': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your Address'}),
            
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

  
        