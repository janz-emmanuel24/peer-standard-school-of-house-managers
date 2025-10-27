from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import CreateView, UpdateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import User, BackgroundCheck
from .forms import UserRegistrationForm, UserUpdateForm, BackgroundCheckForm


def login_view(request):
    """Custom login view"""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome back, {user.get_full_name()}!')
            return redirect('dashboard:home')
        else:
            messages.error(request, 'Invalid username or password.')
    
    return render(request, 'accounts/login.html')


def logout_view(request):
    """Custom logout view"""
    logout(request)
    messages.info(request, 'You have been logged out successfully.')
    return redirect('home')


def register_view(request):
    """User registration view"""
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            return redirect('accounts:login')
        else:
            # Provide a general error message alongside field errors
            messages.error(request, 'Registration failed. Please correct the highlighted errors and try again.')
    else:
        form = UserRegistrationForm()
    
    return render(request, 'accounts/register.html', {'form': form})


@login_required
def profile_view(request):
    """User profile view"""
    return render(request, 'accounts/profile.html')


class UserUpdateView(LoginRequiredMixin, UpdateView):
    """Update user profile"""
    model = User
    form_class = UserUpdateForm
    template_name = 'accounts/profile_update.html'
    success_url = reverse_lazy('accounts:profile')
    
    def get_object(self):
        return self.request.user
    
    def form_valid(self, form):
        # Update username to match email if email changed
        if 'email' in form.changed_data:
            form.instance.username = form.cleaned_data['email'].lower().strip()
        
        messages.success(self.request, 'Your profile has been updated successfully!')
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, 'Please correct the errors below and try again.')
        return super().form_invalid(form)


@login_required
def background_check_view(request):
    """Background check management"""
    if request.method == 'POST':
        form = BackgroundCheckForm(request.POST, request.FILES)
        if form.is_valid():
            background_check = form.save(commit=False)
            background_check.user = request.user
            background_check.save()
            messages.success(request, 'Background check submitted successfully.')
            return redirect('accounts:background_check')
    else:
        form = BackgroundCheckForm()
    
    background_checks = BackgroundCheck.objects.filter(user=request.user)
    return render(request, 'accounts/background_check.html', {
        'form': form,
        'background_checks': background_checks
    })