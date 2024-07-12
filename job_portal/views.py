from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import CustomUserCreationForm

def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('post_signup')
    else:
        form = CustomUserCreationForm()
    return render(request, 'job_portal/signup.html', {'form': form})

from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('dashboard')
    else:
        form = AuthenticationForm()
    return render(request, 'job_portal/login.html', {'form': form})

def home(request):
    return render(request, 'job_portal/home.html')

def post_signup(request):
    return render(request, 'job_portal/post_signup.html')

def job_finder_dashboard(request):
    return render(request, 'job_portal/job_finder_dashboard.html')

def employer_dashboard(request):
    return render(request, 'job_portal/employer_dashboard.html')

