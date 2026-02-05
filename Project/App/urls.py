from django.urls import path
from App.views import *
urlpatterns = [
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    # path('password-reset/', PasswordResetView.as_view(), name='password_reset'),
    path('password-reset/', PasswordResetMail.as_view(), name='password_reset_email'),
    path('password-reset/confirm/', PasswordResetView.as_view(), name='password_reset'),
    
    # OTP URLs
    path('verify-otp/', VerifyOtpView.as_view(), name='verify_otp'),
    path('resend-otp/', ResendOtpView.as_view(), name='resend_otp'),
    
 
]
