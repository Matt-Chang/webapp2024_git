from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate,logout
from .form import RegisterForm
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.urls import reverse
from django.views.decorators.csrf import csrf_protect
from payapp.views import Points
from django.contrib.auth.decorators import login_required
from payapp.models import PointsTransfer,PaymentRequest
from timestamp_server.views import get_timestamp

@csrf_protect
def register_user(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Correct the syntax here
            messages.success(request, 'Registration successful. Welcome!')
            return redirect('login')
        else:
            messages.error(request, 'Registration failed. Please correct the errors below.')
    else:
        form = RegisterForm()
    return render(request, 'register/register.html', {'form': form})


@csrf_protect
def login_user(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'You are now logged in.')
                return redirect('home')
            else:
                messages.error(request, 'invalid username or password.')
        else:
            messages.error(request, 'login failed. Please correct the errors below.')
    else:
        form = AuthenticationForm()
    return render(request, 'login/login.html', {'form': form})

@csrf_protect
def logout_user(request):
    logout(request)
    messages.success(request, 'You are now logg out.')
    return redirect('login')

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from payapp.models import Points, PointsTransfer

@login_required
def home(request):
    user_points = None
    transactions_sent = transactions_received = []
    user_points, created = Points.objects.get_or_create(name=request.user)
    # Adjusting queries to use ForeignKey relationships
    transactions_sent = PointsTransfer.objects.filter(sender=request.user).order_by('-timestamp')
    transactions_received = PointsTransfer.objects.filter(receiver=request.user).order_by('-timestamp')
    # Fetch pending payment requests received by the current user
    payment_requests_received = PaymentRequest.objects.filter(recipient=request.user, status='pending').order_by('-created_at')
    # Call get_timestamp to get the current time from the Thrift service
    current_time = get_timestamp()
    context = {
        'user_points': user_points.points if user_points else 0,  # Ensure there's a fallback if user_points is None
        'transactions_sent': transactions_sent,
        'transactions_received': transactions_received,
        'formatted_points': user_points.formatted_points() if user_points else "0",
        'payment_requests_received': payment_requests_received,  # Add pending payment requests to the context
        'current_time': current_time,  # Add the current time to the context
    }

    return render(request, 'webapps2024/home.html', context)