from django import forms
from django.core.exceptions import ValidationError
from App.models import *
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
class VerifyOtpForm(forms.Form):
    otp_code = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control', 
            'placeholder': 'Enter 6-digit OTP code',
            'maxlength': '6',
            'pattern': '[0-9]{6}'
        }), 
        label="OTP Code", 
        max_length=6,
        min_length=6
    )

    def __init__(self, user=None, purpose='password_reset', *args, **kwargs):
        self.user = user
        self.purpose = purpose
        super().__init__(*args, **kwargs)

    def clean_otp_code(self):
        otp_code = self.cleaned_data.get('otp_code')

        if not self.user:
            raise ValidationError("User not found.")

        try:
            verification_entry = VerificationCode.objects.get(
                user=self.user, 
                code=otp_code, 
                purpose=self.purpose,
                is_used=False,
                expires_at__gt=timezone.now()
            )
            
            # Check if max attempts exceeded
            if verification_entry.attempts >= verification_entry.max_attempts:
                raise ValidationError("Maximum verification attempts exceeded. Please request a new OTP.")
            
        except VerificationCode.DoesNotExist:
            # Increment attempts for any existing valid OTP
            existing_otp = VerificationCode.objects.filter(
                user=self.user,
                purpose=self.purpose,
                is_used=False,
                expires_at__gt=timezone.now()
            ).first()
            
            if existing_otp:
                existing_otp.increment_attempts()
            
            raise ValidationError("Invalid or expired OTP code.")

        # Mark OTP as used
        verification_entry.mark_as_used()

        return otp_code


class ResendOtpForm(forms.Form):
    """Form for resending OTP with rate limiting"""
    
    def __init__(self, user=None, purpose='password_reset', *args, **kwargs):
        self.user = user
        self.purpose = purpose
        super().__init__(*args, **kwargs)
    
    def clean(self):
        cleaned_data = super().clean()
        
        if not self.user:
            raise ValidationError("User not found.")
        
        # Check resend cooldown (2 minutes)
        can_resend, seconds_remaining = OTPResendLog.can_resend(
            self.user, 
            self.purpose, 
            cooldown_minutes=2
        )
        
        if not can_resend:
            minutes = seconds_remaining // 60
            seconds = seconds_remaining % 60
            raise ValidationError(
                f"Please wait {minutes}m {seconds}s before requesting another OTP."
            )
        
        return cleaned_data