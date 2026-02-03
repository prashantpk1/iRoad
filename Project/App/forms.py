from django import forms
from django.core.exceptions import ValidationError
from App.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.password_validation import validate_password


class PasswordResetForm(forms.Form): # Capitalized class name (PEP 8)
   
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter new password'}), 
        label="New Password", 
        max_length=128,
        min_length=8 # Security best practice
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm your password'}), 
        label="Confirm Password", 
        max_length=128
    )

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        # 1. Run Django's built-in security validators
        if password:
            try:
                validate_password(password)
            except ValidationError as e:
                self.add_error('password', e)

        # 2. Check if passwords match
        if password and confirm_password and password != confirm_password:
            self.add_error('confirm_password', "Passwords do not match.")

        # 3. Always return cleaned_data
        return cleaned_data
        
    def save(self, user):
        user.set_password(self.cleaned_data["password"])
        user.save()