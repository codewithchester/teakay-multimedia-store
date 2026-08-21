from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib import messages


def signup_view(request):
    """Handle user registration"""
    if request.method == 'POST':
        # User submitted the signup form
        form = UserCreationForm(request.POST)
        if form.is_valid():
            # Save the new user
            user = form.save()
            
            # Log them in automatically - specify the backend
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            
            messages.success(request, 'Account created successfully! Welcome!')
            return redirect('product_list')
    else:
        # Show empty signup form
        form = UserCreationForm()
    
    return render(request, 'accounts/signup.html', {'form': form})


def login_view(request):
    """Handle user login"""
    if request.method == 'POST':
        # User submitted the login form
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            # Get the user and log them in
            user = form.get_user()
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            messages.success(request, f'Welcome back, {user.username}!')
            return redirect('product_list')
    else:
        # Show empty login form
        form = AuthenticationForm()
    
    return render(request, 'accounts/login.html', {'form': form})


def logout_view(request):
    """Handle user logout"""
    logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('product_list')