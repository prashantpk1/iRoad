from datetime import timedelta
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone


class UserManager(BaseUserManager):
    def create_user(self, email, username, password=None, **extra_fields):
        """
        Creates and saves a User with the given email, username and password.
        """
        if not email:
            raise ValueError('The Email must be set')
        if not username:
            raise ValueError('The Username must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, username, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email



class VerificationCode(models.Model):
    OTP_PURPOSE_CHOICES = [
        ('password_reset', 'Password Reset'),
        ('email_verification', 'Email Verification'),
        ('two_factor', 'Two Factor Authentication'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='verification_codes')
    code = models.CharField(max_length=20)
    purpose = models.CharField(max_length=20, choices=OTP_PURPOSE_CHOICES, default='password_reset')
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    is_used = models.BooleanField(default=False)
    attempts = models.IntegerField(default=0)  # Track failed verification attempts
    max_attempts = models.IntegerField(default=5)  

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', 'is_used', 'expires_at']),
            models.Index(fields=['code', 'is_used']),
        ]
    
    def save(self, *args, **kwargs):
        # Set expiration time (10 minutes from creation)
        if not self.expires_at:
            self.expires_at = timezone.now() + timedelta(minutes=2)
        super().save(*args, **kwargs)
    
    def is_expired(self):
        """Check if OTP has expired"""
        return timezone.now() > self.expires_at
    
    def is_valid(self):
        """Check if OTP is valid (not used, not expired, attempts not exceeded)"""
        return not self.is_used and not self.is_expired() and self.attempts < self.max_attempts
    
    def increment_attempts(self):
        """Increment failed verification attempts"""
        self.attempts += 1
        self.save()
    
    def mark_as_used(self):
        """Mark OTP as used"""
        self.is_used = True
        self.save()
    
    def __str__(self):
        return f'VerificationCode(code={self.code}, user={self.user.email}, purpose={self.purpose})'


class OTPResendLog(models.Model):
    """Track OTP resend requests for rate limiting"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='otp_resend_logs')
    purpose = models.CharField(max_length=20, choices=VerificationCode.OTP_PURPOSE_CHOICES)
    requested_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-requested_at']
        indexes = [
            models.Index(fields=['user', 'purpose', 'requested_at']),
        ]
    
    @classmethod
    def can_resend(cls, user, purpose, cooldown_minutes=2):
        """
        Check if user can request another OTP
        Returns (can_resend: bool, seconds_remaining: int)
        """
        cooldown_time = timezone.now() - timedelta(minutes=cooldown_minutes)
        recent_request = cls.objects.filter(
            user=user,
            purpose=purpose,
            requested_at__gte=cooldown_time
        ).first()
        
        if recent_request:
            time_diff = timezone.now() - recent_request.requested_at
            seconds_remaining = (cooldown_minutes * 60) - int(time_diff.total_seconds())
            return False, max(0, seconds_remaining)
        
        return True, 0
    
    @classmethod
    def log_resend(cls, user, purpose):
        """Log an OTP resend request"""
        return cls.objects.create(user=user, purpose=purpose)
    
    def __str__(self):
        return f'OTPResendLog(user={self.user.email}, purpose={self.purpose}, requested_at={self.requested_at})'