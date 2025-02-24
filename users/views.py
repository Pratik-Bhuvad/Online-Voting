from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import SignUpForm, LoginForm
from .models import CustomUser
from events.models import Event, Vote  # Assuming you have these models for events and votes

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account created successfully! Please log in.')
            return redirect('login')
    else:
        form = SignUpForm()
    return render(request, 'users/signup.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username_or_email = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            # Authenticate by username or email
            user = authenticate(request, username=username_or_email, password=password)
            if user is None:
                try:
                    user_obj = CustomUser.objects.get(email=username_or_email)
                    user = authenticate(request, username=user_obj.username, password=password)
                except CustomUser.DoesNotExist:
                    user = None

            if user is not None:
                login(request, user)
                return redirect('dashboard')  # Redirecting to the dashboard after login
            else:
                messages.error(request, 'Invalid username/email or password.')
    else:
        form = LoginForm()
    return render(request, 'users/login.html', {'form': form})


def user_logout(request):
    logout(request)
    messages.success(request, 'Logged out successfully.')
    return redirect('home')


@login_required(login_url='login')
def user_dashboard(request):
    user = request.user
    events = Event.objects.all()  # Get all events
    user_votes = Vote.objects.filter(user=user)  # Get user votes

    # Identify which events the user has voted in
    voted_event_ids = user_votes.values_list('event_id', flat=True)
    context = {
        'user': user,
        'events': events,
        'voted_event_ids': voted_event_ids
    }
    return render(request, 'users/dashboard.html', context)