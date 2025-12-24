from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.db.utils import IntegrityError
from django.contrib import messages

def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            try:
                user = form.save()
                login(request, user)
                messages.success(request, f'Welcome {user.username}! Your account has been created successfully.')
                return redirect('home') # Assuming 'home' is the name of the home view URL
            except IntegrityError:
                messages.error(request, 'Username already exists. Please choose a different one.')
    else:
        form = CustomUserCreationForm()
    return render(request, 'user_auth/register.html', {'form': form})

class CustomLoginView(LoginView):
    template_name = 'user_auth/login.html'
    next_page = 'home' # Assuming 'home' is the name of the home view URL

class CustomLogoutView(LogoutView):
    next_page = 'home' # Assuming 'home' is the name of the home view URL
