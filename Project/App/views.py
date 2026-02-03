from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import authenticate, login, logout, get_user_model
from App.forms import PasswordResetForm
from django.contrib.auth import update_session_auth_hash
# Create your views here.
User = get_user_model()

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
                    login(request, user)
                    return redirect('home')
                else:
                    return ({'message': 'You are not authorized to access the admin dashboard.'})
            except Exception as e:
                print(e)
        else:  
            return render(request, 'Auth/login.html', {'error': 'Invalid email or password'})

class PasswordResetView(View):
    def get(self, request):
        form = PasswordResetForm()
        return render(request, 'Auth/password_reset.html', {'form': form})

    def post(self, request):
        form = PasswordResetForm(request.POST)
        email = request.POST.get('email')
        try:
            user = User.objects.get(email=email)
            print(user)
        except User.DoesNotExist:
            return render(request, 'Auth/password_reset.html', {'form': form, 'error': 'No user found with this email.'})
        
        
        if form.is_valid():
            # Process the valid form data here
          
            form.save(user)
            update_session_auth_hash(request, user)
            # Update the user's password logic goes here
            return redirect('login')  # Redirect to login after password reset
        return render(request, 'Auth/password_reset.html', {'form': form})
    
class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('login')

class HomeView(View):
    def get(self, request):
        if not request.user.is_authenticated:
            return redirect('login')
        return render(request, 'home.html')