from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import authenticate, login, logout, get_user_model
from App.forms import *
from django.contrib.auth import update_session_auth_hash
# Create your views here.
from App.models import *
User = get_user_model()
import random
from django.core.mail import send_mail
from django.utils import timezone
from datetime import timedelta
from django.contrib import messages
import logging

logger = logging.getLogger(__name__)

def send_email_with_otp(user, purpose):
    """Generate and send OTP via email"""
    otp_code = str(random.randint(100000, 999999))
    expires_at = timezone.now() + timedelta(minutes=10)  # OTP valid for 10 minutes
    
    # Save OTP to database
    VerificationCode.objects.create(
        user=user,
        code=otp_code,
        purpose=purpose,
        expires_at=expires_at
    )
    
    # Customize email based on purpose
    if purpose == 'password_reset':
        subject = 'Password Reset OTP Code'
        message = f'Your password reset OTP code is {otp_code}. It is valid for 10 minutes.'
    elif purpose == 'two_factor':
        subject = 'Two-Factor Authentication Code'
        message = f'Your login verification code is {otp_code}. It is valid for 10 minutes.'
    else:
        subject = 'Your OTP Code'
        message = f'Your OTP code is {otp_code}. It is valid for 10 minutes.'

    try:
        send_mail(
            subject=subject,
            message=message,
            from_email=None,  # This correctly uses DEFAULT_FROM_EMAIL
            recipient_list=[user.email],
            fail_silently=False, # Set to False so we can catch the error
        )
    except Exception as e:
        # Log the error so you can debug it
        logger.error(f"Email failed for {user.email}: {str(e)}")
        return False
    return True

class UserLoginView(View):
    def get(self, request):
        # If user is already logged in and is a superuser, redirect to home
        if request.user.is_authenticated and request.user.is_superuser:
            return redirect('home')  # Change 'home' to your desired redirect
        return render(request, 'Auth/login.html')
    
    def post(self, request):
        email = request.POST.get('email')
        password = request.POST.get('password')


        print(email,password)
        print(authenticate(request, email=email,password=password))
        user=authenticate(request, email=email,password=password)
        if user is not None:
            try:
                print("asf",user.is_superuser)
                if user.is_superuser:
                    request.session['otp_email'] = user.email
                    request.session['otp_purpose'] = 'two_factor'
                    
                    # Send OTP
                    send_email_with_otp(user, 'two_factor')
                    messages.success(request, f'An OTP has been sent to your email ({user.email}).')
                    return redirect('verify_otp')
                else:
                    return ({'message': 'You are not authorized to access the admin dashboard.'})
            except Exception as e:
                print(e)
        else:  
            return render(request, 'Auth/login.html', {'error': 'Invalid email or password'})

class PasswordResetMail(View):
    def get(self, request):
      
        
      
        return render(request, 'Auth/password_reset_email.html')
    
    def post(self, request):
        email = request.POST.get('email')
        
        try:
            user = User.objects.get(email=email)
            
            # Store user email and purpose in session
            request.session['otp_email'] = user.email
            request.session['otp_purpose'] = 'password_reset'
            
            # Send OTP
            send_email_with_otp(user, 'password_reset')
            messages.success(request, f'An OTP has been sent to your email ({user.email}).')
            return redirect('verify_otp')
            
        except User.DoesNotExist:
            messages.error(request, 'No user found with this email.')
            return render(request, 'Auth/password_reset_email.html')

    

class VerifyOtpView(View):
    def get(self, request):
        if 'otp_email' not in request.session or 'otp_purpose' not in request.session:
            return redirect('login')
        
        form = VerifyOtpForm()
        return render(request, 'Auth/verify_otp.html', {'form': form})

    def post(self, request):
        email = request.session.get('otp_email')
        purpose = request.session.get('otp_purpose')
        
        if not email or not purpose:
            return redirect('login')
        
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return redirect('login')
        
        # Pass user and purpose to form
        form = VerifyOtpForm(user=user, purpose=purpose, data=request.POST)
        
        if form.is_valid():
            # Clear OTP session data
            del request.session['otp_email']
            del request.session['otp_purpose']
            
            # Redirect based on purpose
            if purpose == 'password_reset':
                # Store email for password reset form
                request.session['password_reset_email'] = email
                return redirect('password_reset')
            elif purpose == 'two_factor':
                # Complete login
                login(request, user)
                return redirect('home')
            else:
                return redirect('home')
        
        return render(request, 'Auth/verify_otp.html', {'form': form})
    

class PasswordResetView(View):
    def get(self, request):
        # Check if email is in session (user should come from OTP verification)
        if 'password_reset_email' not in request.session:
            messages.error(request, 'Invalid password reset request.')
            return redirect('login')
        
        form = PasswordResetForm()
        return render(request, 'Auth/password_reset.html', {'form': form})

    def post(self, request):
        # Check if email is in session
        email = request.session.get('password_reset_email')
        if not email:
            messages.error(request, 'Invalid password reset request.')
            return redirect('login')
        
        form = PasswordResetForm(request.POST)
        
        if form.is_valid():
            try:
                user = User.objects.get(email=email)
                form.save(user)
                
                # Clear session data
                del request.session['password_reset_email']
                
                messages.success(request, 'Password has been reset successfully. Please login with your new password.')
                return redirect('login')
                
            except User.DoesNotExist:
                messages.error(request, 'User not found.')
                return redirect('login')
        
        return render(request, 'Auth/password_reset.html', {'form': form})
    

class VerifyOtpView(View):
    def get(self, request):
        # Check if OTP session data exists
        if 'otp_email' not in request.session or 'otp_purpose' not in request.session:
            messages.error(request, 'Invalid OTP verification request.')
            return redirect('login')
        
        form = VerifyOtpForm()
        purpose = request.session.get('otp_purpose')
        
        context = {
            'form': form,
            'purpose': purpose,
            'email': request.session.get('otp_email')
        }
        
        return render(request, 'Auth/verify_otp.html', context)

    def post(self, request):
        email = request.session.get('otp_email')
        purpose = request.session.get('otp_purpose')
        
        if not email or not purpose:
            messages.error(request, 'Invalid OTP verification request.')
            return redirect('login')
        
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            messages.error(request, 'User not found.')
            return redirect('login')
        
        # Pass user and purpose to form
        form = VerifyOtpForm(user=user, purpose=purpose, data=request.POST)
        
        if form.is_valid():
            # Clear OTP session data
            del request.session['otp_email']
            del request.session['otp_purpose']
            
            # Redirect based on purpose
            if purpose == 'password_reset':
                # Store email for password reset form
                request.session['password_reset_email'] = email
                messages.success(request, 'OTP verified successfully. Please set your new password.')
                return redirect('password_reset')
                
            elif purpose == 'two_factor':
                # Complete login
                login(request, user)
                messages.success(request, f'Welcome back, {user.email}!')
                return redirect('home')
            else:
                return redirect('home')
        
        context = {
            'form': form,
            'purpose': purpose,
            'email': email
        }
        return render(request, 'Auth/verify_otp.html', context)
    

class ResendOtpView(View):
    def get(self, request):
        email = request.session.get('otp_email')
        purpose = request.session.get('otp_purpose')
        
        # Check if session data exists
        if not email or not purpose:
            messages.error(request, 'Invalid OTP resend request.')
            return redirect('login')
        
        try:
            # Get the user
            user = User.objects.get(email=email)
            
            # Validate using ResendOtpForm (checks rate limiting)
            form = ResendOtpForm(user=user, purpose=purpose, data={})
            
            if form.is_valid():
                # Invalidate old OTPs for this user and purpose
                VerificationCode.objects.filter(
                    user=user,
                    purpose=purpose,
                    is_used=False
                ).update(is_used=True)
                
                # Log the resend request
                OTPResendLog.log_resend(user, purpose)
                
                # Send new OTP
                send_email_with_otp(user, purpose)
                
                messages.success(request, 'A new OTP has been sent to your email.')
            else:
                # Rate limit exceeded
                for error in form.non_field_errors():
                    messages.warning(request, error)
            
            return redirect('verify_otp')
            
        except User.DoesNotExist:
            # Clear invalid session data
            if 'otp_email' in request.session:
                del request.session['otp_email']
            if 'otp_purpose' in request.session:
                del request.session['otp_purpose']
            
            messages.error(request, 'User not found.')
            return redirect('login')
class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('login')

class HomeView(View):
    def get(self, request):
        if not request.user.is_authenticated:
            return redirect('login')
        return render(request, 'home.html')
    