from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, BackgroundCheck
from django.core.exceptions import ValidationError
from django.forms import HiddenInput


class UserRegistrationForm(UserCreationForm):
    """Custom user registration form"""
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    phone_number = forms.CharField(max_length=15, required=True)
    address = forms.CharField(widget=forms.Textarea, required=True)
    date_of_birth = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), required=True)
    user_type = forms.ChoiceField(choices=User.USER_TYPE_CHOICES, required=True)
    profile_picture = forms.ImageField(required=False)

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'phone_number', 
                 'address', 'date_of_birth', 'user_type', 'profile_picture', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Username will be set from email; hide help and keep internal only
        self.fields['username'].help_text = None
        # Make username non-required and hidden since we derive it from email
        self.fields['username'].required = False
        self.fields['username'].widget = HiddenInput()
        self.fields['password1'].help_text = None
        self.fields['password2'].help_text = None

    def clean_username(self):
        # Username will mirror email; validation handled in clean_email/clean
        username = (self.cleaned_data.get('username') or '').strip()
        return username

    def clean_email(self):
        email = (self.cleaned_data.get('email') or '').strip().lower()
        if not email:
            raise ValidationError('Email is required.')
        if User.objects.filter(email__iexact=email).exists():
            raise ValidationError('An account with this email already exists.')
        return email

    def clean(self):
        cleaned = super().clean()
        email = cleaned.get('email')
        if email:
            # Force username to email for consistency
            cleaned['username'] = email
            # Also sync the bound field so save() receives it
            self.data = self.data.copy()
            self.data['username'] = email
        return cleaned

    def save(self, commit=True):
        user = super().save(commit=False)
        # Ensure username mirrors email
        user.username = self.cleaned_data['email']
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.phone_number = self.cleaned_data['phone_number']
        user.address = self.cleaned_data['address']
        user.date_of_birth = self.cleaned_data['date_of_birth']
        user.user_type = self.cleaned_data['user_type']
        if commit:
            user.save()
        return user


class UserUpdateForm(forms.ModelForm):
    """Form for updating user profile"""
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'phone_number', 'address', 
                 'date_of_birth', 'user_type', 'profile_picture')
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
            'address': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make user_type read-only for non-staff users
        if not self.instance.is_staff:
            self.fields['user_type'].widget.attrs['readonly'] = True
            self.fields['user_type'].widget.attrs['class'] = 'bg-gray-50'

    def clean_email(self):
        email = self.cleaned_data['email'].lower().strip()
        # Check if email is already taken by another user
        if User.objects.filter(email__iexact=email).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError("This email address is already registered.")
        return email


class BackgroundCheckForm(forms.ModelForm):
    """Form for background check submission"""
    class Meta:
        model = BackgroundCheck
        fields = ('check_type', 'verification_agency', 'reference_number', 
                 'conducted_date', 'expiry_date', 'notes', 'documents')
        widgets = {
            'conducted_date': forms.DateInput(attrs={'type': 'date'}),
            'expiry_date': forms.DateInput(attrs={'type': 'date'}),
            'notes': forms.Textarea(attrs={'rows': 3}),
        }
