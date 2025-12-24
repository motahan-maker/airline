from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm
from django.contrib.auth.views import LoginView, LogoutView

def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home') # Assuming 'home' is the name of the home view URL
    else:
        form = CustomUserCreationForm()
    return render(request, 'user_auth/register.html', {'form': form})

class CustomLoginView(LoginView):
    template_name = 'user_auth/login.html'
    next_page = 'home' # Assuming 'home' is the name of the home view URL

class CustomLogoutView(LogoutView):
    next_page = 'home' # Assuming 'home' is the name of the home view URL
